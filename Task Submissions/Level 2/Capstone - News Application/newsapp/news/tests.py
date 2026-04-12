"""
tests.py – Automated unit tests for the News Application REST API.

Test classes
------------
  SetUpMixin            – shared helper that creates all test users/data
  AuthenticationTests   – register, token obtain, token refresh
  ArticleListTests      – GET /api/articles/ (role-based queryset)
  SubscribedArticleTests– GET /api/articles/subscribed/
  ArticleCreateTests    – POST /api/articles/ (journalist only)
  ArticleDetailTests    – GET /api/articles/<id>/
  ArticleUpdateTests    – PUT /api/articles/<id>/
  ArticleDeleteTests    – DELETE /api/articles/<id>/
  ArticleApproveTests   – POST /api/articles/<id>/approve/ (editor only)
  NewsletterTests       – CRUD on newsletters
  ApprovedLogTests      – POST /api/approved/ (internal endpoint)
  SignalTests           – email + POST triggered on approval (mocked)
  PermissionTests       – role boundary checks across endpoints
"""

from unittest.mock import MagicMock, patch

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from news.models import Article, CustomUser, Newsletter, Publisher


# ---------------------------------------------------------------------------
# Shared test setup helper
# ---------------------------------------------------------------------------

class SetUpMixin(TestCase):
    """
    Creates a standard set of objects used across most test cases.

    Users created
    -------------
      self.reader      – role='reader'
      self.journalist  – role='journalist'
      self.journalist2 – role='journalist' (second, for ownership tests)
      self.editor      – role='editor'

    Other fixtures
    --------------
      self.publisher   – Publisher instance
      self.article     – approved Article by self.journalist
      self.draft       – unapproved Article by self.journalist
      self.newsletter  – Newsletter by self.journalist containing self.article
      self.client      – DRF APIClient (unauthenticated by default)
    """

    def setUp(self):
        self.client = APIClient()

        # Create permission groups (normally done by AppConfig.ready())
        for name in ('Reader', 'Journalist', 'Editor'):
            Group.objects.get_or_create(name=name)

        # Publisher
        self.publisher = Publisher.objects.create(
            name="Test Gazette",
            description="A test publication",
        )

        # Users
        self.reader = CustomUser.objects.create_user(
            username='reader1',
            password='testpass123',
            email='reader1@test.com',
            role='reader',
        )

        self.journalist = CustomUser.objects.create_user(
            username='journalist1',
            password='testpass123',
            email='journalist1@test.com',
            role='journalist',
        )

        self.journalist2 = CustomUser.objects.create_user(
            username='journalist2',
            password='testpass123',
            email='journalist2@test.com',
            role='journalist',
        )

        self.editor = CustomUser.objects.create_user(
            username='editor1',
            password='testpass123',
            email='editor1@test.com',
            role='editor',
        )

        # Articles
        self.article = Article.objects.create(
            title="Approved Test Article",
            content="This is approved content.",
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
            approved_by=self.editor,
            approved_at=timezone.now(),
        )

        self.draft = Article.objects.create(
            title="Draft Article",
            content="This is draft content.",
            author=self.journalist,
            approved=False,
        )

        # Newsletter
        self.newsletter = Newsletter.objects.create(
            title="Test Newsletter",
            description="A newsletter for tests.",
            author=self.journalist,
        )
        self.newsletter.articles.add(self.article)

    # ------------------------------------------------------------------
    # Convenience: authenticate the client as a given user via JWT
    # ------------------------------------------------------------------

    def _auth(self, user):
        """Obtain a JWT token for the given user and set it on self.client."""
        url = reverse('api_token_obtain')
        response = self.client.post(url, {
            'username': user.username,
            'password': 'testpass123',
        }, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return token


# ===========================================================================
# 1. Authentication tests
# ===========================================================================

class AuthenticationTests(SetUpMixin):
    """Tests for user registration and JWT token endpoints."""

    def test_register_new_user_success(self):
        """A new user can register with valid data."""
        url = reverse('api_register')
        data = {
            'username': 'newreader',
            'email': 'new@test.com',
            'password': 'SecurePass99',
            'role': 'reader',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newreader')
        # Password must NOT be in the response
        self.assertNotIn('password', response.data)

    def test_register_duplicate_username_fails(self):
        """Registration with an existing username returns 400."""
        url = reverse('api_register')
        data = {
            'username': 'reader1',  # already exists
            'email': 'other@test.com',
            'password': 'SecurePass99',
            'role': 'reader',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_success(self):
        """Valid credentials return access and refresh tokens."""
        url = reverse('api_token_obtain')
        response = self.client.post(url, {
            'username': 'reader1',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_wrong_password_fails(self):
        """Wrong password returns 401."""
        url = reverse('api_token_obtain')
        response = self.client.post(url, {
            'username': 'reader1',
            'password': 'wrongpassword',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_success(self):
        """A valid refresh token returns a new access token."""
        obtain_url = reverse('api_token_obtain')
        obtain_resp = self.client.post(obtain_url, {
            'username': 'reader1',
            'password': 'testpass123',
        }, format='json')
        refresh_token = obtain_resp.data['refresh']

        refresh_url = reverse('api_token_refresh')
        response = self.client.post(refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_unauthenticated_request_denied(self):
        """Unauthenticated requests to protected endpoints return 401."""
        url = reverse('api_article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ===========================================================================
# 2. Article list tests
# ===========================================================================

class ArticleListTests(SetUpMixin):
    """GET /api/articles/ – role-based visibility."""

    def test_reader_sees_only_approved_articles(self):
        """Readers should only receive approved articles."""
        self._auth(self.reader)
        url = reverse('api_article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a['title'] for a in response.data['results']]
        self.assertIn("Approved Test Article", titles)
        self.assertNotIn("Draft Article", titles)

    def test_editor_sees_all_articles_including_drafts(self):
        """Editors can see both approved and draft articles."""
        self._auth(self.editor)
        url = reverse('api_article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a['title'] for a in response.data['results']]
        self.assertIn("Approved Test Article", titles)
        self.assertIn("Draft Article", titles)

    def test_journalist_sees_only_approved_articles(self):
        """Journalists also see only approved articles via the list endpoint."""
        self._auth(self.journalist)
        url = reverse('api_article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a['title'] for a in response.data['results']]
        self.assertIn("Approved Test Article", titles)
        self.assertNotIn("Draft Article", titles)


# ===========================================================================
# 3. Subscribed articles tests
# ===========================================================================

class SubscribedArticleTests(SetUpMixin):
    """GET /api/articles/subscribed/ – reader subscription filtering."""

    def test_reader_subscribed_to_journalist_sees_their_articles(self):
        """A reader who follows journalist1 gets journalist1's approved articles."""
        self.reader.subscribed_journalists.add(self.journalist)
        self._auth(self.reader)
        url = reverse('api_subscribed_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a['title'] for a in response.data['results']]
        self.assertIn("Approved Test Article", titles)

    def test_reader_subscribed_to_publisher_sees_their_articles(self):
        """A reader who subscribes to a publisher gets that publisher's approved articles."""
        self.reader.subscribed_publishers.add(self.publisher)
        self._auth(self.reader)
        url = reverse('api_subscribed_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a['title'] for a in response.data['results']]
        self.assertIn("Approved Test Article", titles)

    def test_reader_with_no_subscriptions_gets_empty_list(self):
        """A reader with no subscriptions receives an empty result set."""
        # Ensure no subscriptions
        self.reader.subscribed_journalists.clear()
        self.reader.subscribed_publishers.clear()
        self._auth(self.reader)
        url = reverse('api_subscribed_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_reader_does_not_see_unsubscribed_articles(self):
        """Reader subscribed to journalist2 does NOT see journalist1's articles."""
        # Subscribe only to journalist2 (who has no articles in our fixtures)
        self.reader.subscribed_journalists.set([self.journalist2])
        self._auth(self.reader)
        url = reverse('api_subscribed_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a['title'] for a in response.data['results']]
        self.assertNotIn("Approved Test Article", titles)

    def test_journalist_gets_empty_subscribed_list(self):
        """Journalists calling /subscribed/ get an empty list (they have no subs)."""
        self._auth(self.journalist)
        url = reverse('api_subscribed_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


# ===========================================================================
# 4. Article create tests
# ===========================================================================

class ArticleCreateTests(SetUpMixin):
    """POST /api/articles/ – only journalists can create articles."""

    def _article_payload(self):
        return {
            'title': 'A Brand New Article',
            'content': 'This is great content for a brand new article.',
        }

    def test_journalist_can_create_article(self):
        """Journalists can POST a new article successfully."""
        self._auth(self.journalist)
        url = reverse('api_article_list')
        response = self.client.post(url, self._article_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'A Brand New Article')
        # New articles should default to unapproved
        self.assertFalse(response.data['approved'])

    def test_new_article_author_set_to_request_user(self):
        """The author field is automatically set to the authenticated journalist."""
        self._auth(self.journalist)
        url = reverse('api_article_list')
        response = self.client.post(url, self._article_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], self.journalist.pk)

    def test_reader_cannot_create_article(self):
        """Readers are forbidden from creating articles."""
        self._auth(self.reader)
        url = reverse('api_article_list')
        response = self.client.post(url, self._article_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_cannot_create_article(self):
        """Editors are also forbidden from creating articles (journalists only)."""
        self._auth(self.editor)
        url = reverse('api_article_list')
        response = self.client.post(url, self._article_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_article_missing_title_fails(self):
        """Submitting an article without a title returns 400."""
        self._auth(self.journalist)
        url = reverse('api_article_list')
        response = self.client.post(url, {'content': 'No title here.'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)


# ===========================================================================
# 5. Article detail tests
# ===========================================================================

class ArticleDetailTests(SetUpMixin):
    """GET /api/articles/<id>/ – retrieve a single article."""

    def test_reader_can_retrieve_approved_article(self):
        """Any authenticated user can retrieve an approved article."""
        self._auth(self.reader)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Approved Test Article")

    def test_reader_cannot_retrieve_draft_article(self):
        """Readers get 404 when requesting a draft (unapproved) article."""
        self._auth(self.reader)
        url = reverse('api_article_detail', args=[self.draft.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_editor_can_retrieve_draft_article(self):
        """Editors can retrieve draft articles for review."""
        self._auth(self.editor)
        url = reverse('api_article_detail', args=[self.draft.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nonexistent_article_returns_404(self):
        """Requesting an article that doesn't exist returns 404."""
        self._auth(self.reader)
        url = reverse('api_article_detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ===========================================================================
# 6. Article update tests
# ===========================================================================

class ArticleUpdateTests(SetUpMixin):
    """PUT /api/articles/<id>/ – update an existing article."""

    def test_journalist_can_update_own_article(self):
        """A journalist can update their own (approved) article."""
        self._auth(self.journalist)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.put(url, {
            'title': 'Updated Title',
            'content': 'Updated content here.',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_journalist_cannot_update_another_journalists_article(self):
        """Journalist2 cannot modify journalist1's article."""
        self._auth(self.journalist2)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.put(url, {
            'title': 'Stolen Edit',
            'content': 'Content.',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_update_any_article(self):
        """Editors can update any article regardless of authorship."""
        self._auth(self.editor)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.put(url, {
            'title': 'Editor-Corrected Title',
            'content': 'Editor-corrected content.',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reader_cannot_update_article(self):
        """Readers are forbidden from updating articles."""
        self._auth(self.reader)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.put(url, {
            'title': 'Reader Hack',
            'content': 'Content.',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ===========================================================================
# 7. Article delete tests
# ===========================================================================

class ArticleDeleteTests(SetUpMixin):
    """DELETE /api/articles/<id>/"""

    def test_journalist_can_delete_own_article(self):
        """A journalist can delete their own article."""
        self._auth(self.journalist)
        url = reverse('api_article_detail', args=[self.draft.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(pk=self.draft.pk).exists())

    def test_editor_can_delete_any_article(self):
        """Editors can delete any article."""
        self._auth(self.editor)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reader_cannot_delete_article(self):
        """Readers cannot delete articles."""
        self._auth(self.reader)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_journalist_cannot_delete_another_journalists_article(self):
        """Journalist2 cannot delete journalist1's article."""
        self._auth(self.journalist2)
        url = reverse('api_article_detail', args=[self.article.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ===========================================================================
# 8. Article approval tests
# ===========================================================================

class ArticleApproveTests(SetUpMixin):
    """POST /api/articles/<id>/approve/ – editor-only approval."""

    def test_editor_can_approve_draft_article(self):
        """An editor can approve a pending article."""
        self._auth(self.editor)
        url = reverse('api_article_approve', args=[self.draft.pk])
        with patch('news.signals._send_approval_emails'), \
             patch('news.signals._post_to_approved_endpoint'):
            response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.draft.refresh_from_db()
        self.assertTrue(self.draft.approved)
        self.assertEqual(self.draft.approved_by, self.editor)

    def test_journalist_cannot_approve_article(self):
        """Journalists cannot approve articles – that's the editor's job."""
        self._auth(self.journalist)
        url = reverse('api_article_approve', args=[self.draft.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_cannot_approve_article(self):
        """Readers cannot approve articles."""
        self._auth(self.reader)
        url = reverse('api_article_approve', args=[self.draft.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approving_already_approved_article_returns_400(self):
        """Approving an already-approved article returns a 400 error."""
        self._auth(self.editor)
        url = reverse('api_article_approve', args=[self.article.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_approval_sets_approved_at_timestamp(self):
        """Approval sets the approved_at timestamp."""
        self._auth(self.editor)
        url = reverse('api_article_approve', args=[self.draft.pk])
        with patch('news.signals._send_approval_emails'), \
             patch('news.signals._post_to_approved_endpoint'):
            self.client.post(url)
        self.draft.refresh_from_db()
        self.assertIsNotNone(self.draft.approved_at)


# ===========================================================================
# 9. Newsletter tests
# ===========================================================================

class NewsletterTests(SetUpMixin):
    """CRUD operations on newsletters."""

    def test_reader_can_list_newsletters(self):
        """All authenticated users can list newsletters."""
        self._auth(self.reader)
        url = reverse('api_newsletter_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_journalist_can_create_newsletter(self):
        """Journalists can create newsletters."""
        self._auth(self.journalist)
        url = reverse('api_newsletter_list')
        response = self.client.post(url, {
            'title': 'My New Newsletter',
            'description': 'A fresh newsletter.',
            'articles': [self.article.pk],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'My New Newsletter')

    def test_editor_can_create_newsletter(self):
        """Editors can also create newsletters."""
        self._auth(self.editor)
        url = reverse('api_newsletter_list')
        response = self.client.post(url, {
            'title': 'Editor Newsletter',
            'description': 'An editor-curated newsletter.',
            'articles': [],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reader_cannot_create_newsletter(self):
        """Readers cannot create newsletters."""
        self._auth(self.reader)
        url = reverse('api_newsletter_list')
        response = self.client.post(url, {
            'title': 'Reader Hack',
            'articles': [],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_journalist_can_update_own_newsletter(self):
        """A journalist can update their own newsletter."""
        self._auth(self.journalist)
        url = reverse('api_newsletter_detail', args=[self.newsletter.pk])
        response = self.client.put(url, {
            'title': 'Updated Newsletter Title',
            'description': 'Updated description.',
            'articles': [self.article.pk],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Newsletter Title')

    def test_journalist2_cannot_update_journalist1_newsletter(self):
        """Journalist2 cannot modify journalist1's newsletter."""
        self._auth(self.journalist2)
        url = reverse('api_newsletter_detail', args=[self.newsletter.pk])
        response = self.client.put(url, {
            'title': 'Stolen Edit',
            'articles': [],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_can_retrieve_newsletter(self):
        """Readers can view a specific newsletter."""
        self._auth(self.reader)
        url = reverse('api_newsletter_detail', args=[self.newsletter.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Newsletter')


# ===========================================================================
# 10. Approved article log endpoint tests
# ===========================================================================

class ApprovedLogTests(SetUpMixin):
    """POST /api/approved/ – internal integration endpoint."""

    def _valid_payload(self):
        return {
            'article_id': self.article.pk,
            'title': self.article.title,
            'author': self.journalist.username,
            'publisher': self.publisher.name,
            'approved_at': timezone.now().isoformat(),
        }

    def test_valid_payload_returns_201(self):
        """A correctly formed payload is accepted and returns 201."""
        url = reverse('api_approved_log')
        response = self.client.post(url, self._valid_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'logged')

    def test_missing_article_id_returns_400(self):
        """Payload without article_id is rejected."""
        url = reverse('api_approved_log')
        payload = self._valid_payload()
        del payload['article_id']
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_title_returns_400(self):
        """Payload without title is rejected."""
        url = reverse('api_approved_log')
        payload = self._valid_payload()
        del payload['title']
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_publisher_is_accepted(self):
        """Independent articles (no publisher) are logged without error."""
        url = reverse('api_approved_log')
        payload = self._valid_payload()
        payload['publisher'] = None
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# ===========================================================================
# 11. Signal tests (mocked)
# ===========================================================================

class SignalTests(SetUpMixin):
    """
    Tests that the post-approval side effects (email + API POST) are triggered.

    We use unittest.mock.patch to avoid actually sending emails or making
    HTTP requests during tests.  We only verify the functions were called.
    """

    def test_approval_triggers_email_to_subscribers(self):
        """
        When an editor approves a draft, _send_approval_emails should be called
        with the article and the set of subscriber emails.
        """
        # Give the reader a subscription to journalist1
        self.reader.subscribed_journalists.add(self.journalist)

        with patch('news.signals._send_approval_emails') as mock_email, \
             patch('news.signals._post_to_approved_endpoint'):

            # Simulate what the approval view does
            self.draft._approval_just_set = True
            self.draft.approved = True
            self.draft.approved_by = self.editor
            self.draft.approved_at = timezone.now()
            self.draft.save()

        # The email helper should have been called once
        mock_email.assert_called_once()
        # The article passed to it should be self.draft
        called_article = mock_email.call_args[0][0]
        self.assertEqual(called_article.pk, self.draft.pk)

    def test_approval_triggers_post_to_approved_endpoint(self):
        """When approved, _post_to_approved_endpoint should be called."""
        with patch('news.signals._send_approval_emails'), \
             patch('news.signals._post_to_approved_endpoint') as mock_post:

            self.draft._approval_just_set = True
            self.draft.approved = True
            self.draft.approved_by = self.editor
            self.draft.approved_at = timezone.now()
            self.draft.save()

        mock_post.assert_called_once()

    def test_no_signal_fired_on_non_approval_save(self):
        """
        Saving an article without setting _approval_just_set should NOT
        trigger the email or POST helpers.
        """
        with patch('news.signals._send_approval_emails') as mock_email, \
             patch('news.signals._post_to_approved_endpoint') as mock_post:

            # Save without the flag
            self.draft.content = "Updated content only."
            self.draft.save()

        mock_email.assert_not_called()
        mock_post.assert_not_called()

    def test_email_sent_to_publisher_subscribers(self):
        """
        Readers subscribed to a publisher receive email when that publisher's
        article is approved.
        """
        # Subscribe reader to the publisher
        self.reader.subscribed_publishers.add(self.publisher)

        # Create a draft that belongs to this publisher
        draft_for_publisher = Article.objects.create(
            title="Publisher Draft",
            content="Content.",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )

        with patch('news.signals._send_approval_emails') as mock_email, \
             patch('news.signals._post_to_approved_endpoint'):

            draft_for_publisher._approval_just_set = True
            draft_for_publisher.approved = True
            draft_for_publisher.approved_by = self.editor
            draft_for_publisher.approved_at = timezone.now()
            draft_for_publisher.save()

        mock_email.assert_called_once()
        # Verify the recipient set includes the reader's email
        recipient_emails = mock_email.call_args[0][1]
        self.assertIn(self.reader.email, recipient_emails)


# ===========================================================================
# 12. Permission boundary tests
# ===========================================================================

class PermissionTests(SetUpMixin):
    """Additional boundary tests to ensure role separation is complete."""

    def test_unauthenticated_cannot_access_any_api_endpoint(self):
        """No JWT token → all API endpoints return 401."""
        endpoints = [
            reverse('api_article_list'),
            reverse('api_newsletter_list'),
            reverse('api_publisher_list'),
            reverse('api_profile'),
        ]
        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                msg=f"Expected 401 at {url}, got {response.status_code}",
            )

    def test_reader_cannot_access_profile_of_another_user(self):
        """The profile endpoint always returns the authenticated user's own data."""
        self._auth(self.reader)
        url = reverse('api_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Must return OUR user, not someone else's
        self.assertEqual(response.data['username'], self.reader.username)

    def test_all_roles_can_list_publishers(self):
        """Any authenticated user can list publishers."""
        url = reverse('api_publisher_list')
        for user in [self.reader, self.journalist, self.editor]:
            self._auth(user)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
                msg=f"Expected 200 for {user.role}",
            )
