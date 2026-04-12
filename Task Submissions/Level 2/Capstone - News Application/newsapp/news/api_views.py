"""
api_views.py – Django REST Framework API views.

Endpoints
---------
  Authentication
    POST /api/register/                – create a new account
    POST /api/token/                   – obtain JWT access + refresh tokens
    POST /api/token/refresh/           – refresh an access token

  Articles
    GET  /api/articles/                – list all approved articles
    POST /api/articles/                – create article (journalists only)
    GET  /api/articles/<id>/           – retrieve a single article
    PUT  /api/articles/<id>/           – update (editors / journalists)
    DELETE /api/articles/<id>/         – delete (editors / journalists)
    GET  /api/articles/subscribed/     – articles from the reader's subscriptions

  Newsletters
    GET  /api/newsletters/             – list all newsletters
    POST /api/newsletters/             – create (journalists / editors)
    GET  /api/newsletters/<id>/        – single newsletter
    PUT  /api/newsletters/<id>/        – update
    DELETE /api/newsletters/<id>/      – delete

  Approval log (internal)
    POST /api/approved/                – log an approved article (called by signal)

  Publishers
    GET  /api/publishers/              – list all publishers
    GET  /api/publishers/<id>/         – single publisher
"""

import logging

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from news.models import Article, CustomUser, Newsletter, Publisher
from news.permissions import (
    IsEditor,
    IsEditorOrJournalist,
    IsJournalist,
    IsOwnerOrEditor,
)
from news.serializers import (
    ApprovedArticleLogSerializer,
    ArticleSerializer,
    NewsletterSerializer,
    PublisherSerializer,
    RegisterSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


# ===========================================================================
# Authentication
# ===========================================================================

class RegisterView(generics.CreateAPIView):
    """
    POST /api/register/

    Anyone (unauthenticated) can register a new account.
    Returns the created user object (without the password).
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# JWT views are provided by SimpleJWT; we expose them with meaningful names.
# TokenObtainPairView  → POST /api/token/   (returns access + refresh)
# TokenRefreshView     → POST /api/token/refresh/


# ===========================================================================
# Articles
# ===========================================================================

class ArticleListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/articles/ – return all approved articles (any authenticated user)
    POST /api/articles/ – create a new article (journalists only)
    """
    serializer_class = ArticleSerializer

    def get_permissions(self):
        """
        Return different permission classes depending on the HTTP method.
        GET  → any authenticated user
        POST → journalists only
        """
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsJournalist()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Editors see all articles (approved and draft).
        Everyone else sees only approved articles.
        """
        user = self.request.user
        if user.role == 'editor':
            return Article.objects.select_related('author', 'publisher').all()
        return Article.objects.select_related('author', 'publisher').filter(approved=True)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/articles/<id>/ – retrieve a single article
    PUT    /api/articles/<id>/ – update (editors and the original journalist)
    DELETE /api/articles/<id>/ – delete (editors and the original journalist)
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrEditor]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'editor':
            return Article.objects.all()
        return Article.objects.filter(approved=True)


class SubscribedArticlesView(generics.ListAPIView):
    """
    GET /api/articles/subscribed/

    Returns articles authored by journalists or publishers that the
    authenticated reader has subscribed to.

    Only readers have meaningful subscriptions.  If a journalist or editor
    calls this endpoint they receive an empty list.
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role != 'reader':
            return Article.objects.none()

        subscribed_journalist_ids = user.subscribed_journalists.values_list('id', flat=True)
        subscribed_publisher_ids = user.subscribed_publishers.values_list('id', flat=True)

        return (
            Article.objects
            .filter(approved=True)
            .filter(
                # Articles by subscribed journalists OR from subscribed publishers
                models_Q(author_id__in=subscribed_journalist_ids)
                | models_Q(publisher_id__in=subscribed_publisher_ids)
            )
            .select_related('author', 'publisher')
            .distinct()
        )


# We need Django's Q object for OR filtering
from django.db.models import Q as models_Q  # noqa: E402 – placed after class for readability


class ArticleApproveView(APIView):
    """
    POST /api/articles/<id>/approve/

    Allows an editor to approve a draft article.
    Sets approved=True, records who approved it and when, then the post_save
    signal handles emailing subscribers and POSTing to /api/approved/.
    """
    permission_classes = [IsAuthenticated, IsEditor]

    def post(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(
                {'detail': 'Article not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if article.approved:
            return Response(
                {'detail': 'Article is already approved.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Stamp the private flag so the signal knows this is a fresh approval
        article._approval_just_set = True
        article.approved = True
        article.approved_by = request.user
        article.approved_at = timezone.now()
        article.save()

        logger.info(
            "Editor '%s' approved article id=%d ('%s').",
            request.user.username,
            article.pk,
            article.title,
        )

        return Response(
            ArticleSerializer(article, context={'request': request}).data,
            status=status.HTTP_200_OK,
        )


# ===========================================================================
# Newsletters
# ===========================================================================

class NewsletterListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/newsletters/ – list all newsletters (any authenticated user)
    POST /api/newsletters/ – create (journalists and editors)
    """
    serializer_class = NewsletterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsEditorOrJournalist()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Newsletter.objects.select_related('author').prefetch_related('articles').all()


class NewsletterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/newsletters/<id>/
    PUT    /api/newsletters/<id>/
    DELETE /api/newsletters/<id>/
    """
    serializer_class = NewsletterSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrEditor]
    queryset = Newsletter.objects.all()


# ===========================================================================
# Approved article log – internal integration endpoint
# ===========================================================================

class ApprovedArticleLogView(APIView):
    """
    POST /api/approved/

    Receives the payload POSTed by signals.py after an article is approved.
    In a real integration this would forward the data to an external service.
    Here it simply validates the payload, logs it, and returns 201.

    Authentication is intentionally open for internal use; in production
    you would secure this with a service token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ApprovedArticleLogSerializer(data=request.data)

        if serializer.is_valid():
            logger.info(
                "Approved article logged: id=%s title='%s' author='%s'",
                serializer.validated_data.get('article_id'),
                serializer.validated_data.get('title'),
                serializer.validated_data.get('author'),
            )
            return Response(
                {'status': 'logged', 'data': serializer.validated_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===========================================================================
# Publishers
# ===========================================================================

class PublisherListView(generics.ListAPIView):
    """GET /api/publishers/ – list all publishers."""
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticated]
    queryset = Publisher.objects.all()


class PublisherDetailView(generics.RetrieveAPIView):
    """GET /api/publishers/<id>/ – single publisher."""
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticated]
    queryset = Publisher.objects.all()


# ===========================================================================
# User profile
# ===========================================================================

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/profile/ – view your own profile
    PUT  /api/profile/ – update subscriptions (readers) etc.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Always return the currently authenticated user."""
        return self.request.user
