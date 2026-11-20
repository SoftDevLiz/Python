"""
signals.py – Django signals for the News Application.

Signals defined here
--------------------
1. assign_user_group   (post_save → CustomUser)
   Automatically places a newly created user into the correct Django Group
   based on their role.  Groups are created with appropriate permissions the
   first time they are referenced (see apps.py → ready()).

2. article_approved    (post_save → Article)
   Fires whenever an Article is saved.  If the article just transitioned to
   approved=True, two things happen:
     a. All subscribers (readers who follow the author or the publisher)
        receive an email notification.
     b. A POST request is sent to /api/approved/ to log the approval
        (simulating an external integration, kept internal to the project).
"""

import logging
import requests

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Import models lazily to avoid circular-import issues at module load time.
# The receiver decorator handles the timing correctly.
# ---------------------------------------------------------------------------


@receiver(post_save, sender='news.CustomUser')
def assign_user_group(sender, instance, created, **kwargs):
    """
    When a new CustomUser is saved, call assign_group() to place them into
    the appropriate Django permission group (Reader / Journalist / Editor).

    We only run on `created=True` to avoid wiping manual admin group changes
    on every profile save.  If an admin wants to reassign a user's role they
    should update the role field, which will trigger a new group assignment.
    """
    if created:
        instance.assign_group()
        logger.info(
            "User '%s' assigned to group '%s'.",
            instance.username,
            instance.role,
        )


@receiver(post_save, sender='news.Article')
def article_approved(sender, instance, created, **kwargs):
    """
    Triggered every time an Article is saved.

    We only act when the article has just been approved, which we detect by
    checking `instance.approved` and comparing with `update_fields`.  To
    avoid repeatedly sending emails if an already-approved article is edited,
    we use a lightweight `_approval_just_set` flag set in the approval view.
    """

    # The approval view stamps this private attribute before calling save().
    # If the flag isn't present the article was saved for another reason.
    if not getattr(instance, '_approval_just_set', False):
        return

    logger.info("Article '%s' (id=%d) approved – running post-approval tasks.", instance.title, instance.pk)

    # ------------------------------------------------------------------
    # 1. Collect subscriber emails
    # ------------------------------------------------------------------
    subscriber_emails = _collect_subscriber_emails(instance)

    # ------------------------------------------------------------------
    # 2. Send email notifications
    # ------------------------------------------------------------------
    if subscriber_emails:
        _send_approval_emails(instance, subscriber_emails)
    else:
        logger.info("No subscribers to notify for article id=%d.", instance.pk)

    # ------------------------------------------------------------------
    # 3. POST to internal /api/approved/ endpoint
    # ------------------------------------------------------------------
    _post_to_approved_endpoint(instance)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _collect_subscriber_emails(article):
    """
    Return a set of email addresses belonging to all readers who subscribe
    to either the article's author (journalist) or its publisher.

    Importing CustomUser here (inside the function) avoids circular imports.
    """
    from news.models import CustomUser  # local import – safe here

    emails = set()

    # Readers who follow the journalist author
    author_followers = CustomUser.objects.filter(
        subscribed_journalists=article.author,
        email__isnull=False,
    ).exclude(email='')
    emails.update(author_followers.values_list('email', flat=True))

    # Readers who subscribe to the publisher (if article belongs to one)
    if article.publisher:
        publisher_subscribers = CustomUser.objects.filter(
            subscribed_publishers=article.publisher,
            email__isnull=False,
        ).exclude(email='')
        emails.update(publisher_subscribers.values_list('email', flat=True))

    return emails


def _send_approval_emails(article, recipient_emails):
    """Send a notification email to each subscriber about the new article."""
    subject = f"New article: {article.title}"
    message = (
        f"Hi,\n\n"
        f"A new article has been published that you subscribed to:\n\n"
        f"Title   : {article.title}\n"
        f"Author  : {article.author.get_full_name() or article.author.username}\n"
        f"Publisher: {article.publisher.name if article.publisher else 'Independent'}\n\n"
        f"--- Article Preview ---\n"
        f"{article.content[:300]}{'...' if len(article.content) > 300 else ''}\n\n"
        f"Thank you for subscribing!\n"
        f"The News App Team"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(recipient_emails),
            fail_silently=False,
        )
        logger.info(
            "Approval email sent to %d subscriber(s) for article id=%d.",
            len(recipient_emails),
            article.pk,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error(
            "Failed to send approval emails for article id=%d: %s",
            article.pk,
            exc,
        )


def _post_to_approved_endpoint(article):
    """
    Send a POST request to the internal /api/approved/ endpoint.

    This simulates the article being shared to an external integration.
    Uses Python's `requests` library.  In production you would replace the
    localhost URL with an environment variable.
    """
    url = "http://127.0.0.1:8000/api/approved/"
    payload = {
        "article_id": article.pk,
        "title": article.title,
        "author": article.author.username,
        "publisher": article.publisher.name if article.publisher else None,
        "approved_at": article.approved_at.isoformat() if article.approved_at else None,
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info(
            "Successfully posted article id=%d to /api/approved/ (status %d).",
            article.pk,
            response.status_code,
        )
    except requests.exceptions.ConnectionError:
        # During tests or early development the server may not be running.
        logger.warning(
            "Could not connect to /api/approved/ for article id=%d. "
            "Is the development server running?",
            article.pk,
        )
    except requests.exceptions.RequestException as exc:
        logger.error(
            "Failed to POST article id=%d to /api/approved/: %s",
            article.pk,
            exc,
        )
