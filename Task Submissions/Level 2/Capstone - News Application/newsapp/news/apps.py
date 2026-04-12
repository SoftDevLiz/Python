"""
apps.py – AppConfig for the 'news' Django application.

The ready() method runs once when Django finishes loading.  We use it to:
  1. Import signals so their @receiver decorators register correctly.
  2. Create the three permission Groups (Reader, Editor, Journalist) and
     assign the correct Django model permissions to each.

Why create groups in ready() instead of a migration?
-----------------------------------------------------
Permissions are created by Django's post_migrate signal from the
contenttypes / auth apps.  By the time ready() runs after the initial
migration, those permissions already exist.  Using a data migration would
work too, but this approach keeps the logic in Python and is easier to
understand.
"""

import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        # Connect signal handlers
        import news.signals  # noqa: F401 – side-effect import

        # Set up groups and permissions after migrations have run
        from django.db.models.signals import post_migrate
        post_migrate.connect(_setup_groups_and_permissions, sender=self)


def _setup_groups_and_permissions(sender, **kwargs):
    """
    Create Reader, Editor, and Journalist groups with correct permissions.

    Django's built-in permission names follow the pattern:
      <action>_<modelname>   e.g. view_article, add_newsletter

    Permissions are created automatically for every model in a migration;
    we simply fetch and assign them here.
    """
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    try:
        from news.models import Article, Newsletter
    except Exception:
        # Models may not be available if migrations haven't run yet
        return

    article_ct = ContentType.objects.get_for_model(Article)
    newsletter_ct = ContentType.objects.get_for_model(Newsletter)

    # ------------------------------------------------------------------
    # Helper: get a permission object safely
    # ------------------------------------------------------------------
    def perm(codename, ct):
        try:
            return Permission.objects.get(codename=codename, content_type=ct)
        except Permission.DoesNotExist:
            logger.warning("Permission '%s' not found – run migrations first.", codename)
            return None

    # Gather permissions for each group
    reader_perms = list(filter(None, [
        perm('view_article', article_ct),
        perm('view_newsletter', newsletter_ct),
    ]))

    editor_perms = list(filter(None, [
        perm('view_article', article_ct),
        perm('change_article', article_ct),
        perm('delete_article', article_ct),
        perm('view_newsletter', newsletter_ct),
        perm('change_newsletter', newsletter_ct),
        perm('delete_newsletter', newsletter_ct),
    ]))

    journalist_perms = list(filter(None, [
        perm('add_article', article_ct),
        perm('view_article', article_ct),
        perm('change_article', article_ct),
        perm('delete_article', article_ct),
        perm('add_newsletter', newsletter_ct),
        perm('view_newsletter', newsletter_ct),
        perm('change_newsletter', newsletter_ct),
        perm('delete_newsletter', newsletter_ct),
    ]))

    # Create (or retrieve) groups and set permissions
    group_definitions = {
        'Reader': reader_perms,
        'Editor': editor_perms,
        'Journalist': journalist_perms,
    }

    for group_name, perms in group_definitions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if perms:
            group.permissions.set(perms)
        if created:
            logger.info("Created permission group: %s", group_name)
