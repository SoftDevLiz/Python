"""
models.py – Data layer for the News Application.

Models defined here:
  - Publisher   : A media organisation with editors and journalists.
  - CustomUser  : Extends AbstractUser; carries role-specific fields.
  - Article     : A news article written by a journalist.
  - Newsletter  : A curated collection of articles.

Role logic
----------
  Reader     – can subscribe to publishers and journalists; read-only access.
  Journalist – can author articles and newsletters independently.
  Editor     – can approve / update / delete articles and newsletters;
               belongs to a publisher.

Because a single CustomUser table must serve all three roles, role-specific
fields are nullable.  The save() override enforces the "mutually exclusive"
constraint described in the spec: a journalist's reader fields are set to
None, and vice-versa.  (ManyToMany fields are cleared rather than set to
None, which is their "empty" state.)
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# ---------------------------------------------------------------------------
# Role constants – stored as a plain string on CustomUser.role
# ---------------------------------------------------------------------------
class Role(models.TextChoices):
    READER = 'reader', 'Reader'
    JOURNALIST = 'journalist', 'Journalist'
    EDITOR = 'editor', 'Editor'


# ---------------------------------------------------------------------------
# Publisher
# ---------------------------------------------------------------------------
class Publisher(models.Model):
    """
    A media organisation (e.g. "The Daily Bugle").

    Relationships
    -------------
    - editors     : reverse FK from CustomUser (editors who work here)
    - journalists : reverse FK from CustomUser (journalists affiliated here)
    - articles    : reverse FK from Article
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Custom User
# ---------------------------------------------------------------------------
class CustomUser(AbstractUser):
    """
    Extended user model that adds a role field and role-specific data fields.

    Nullable fields by role
    -----------------------
    Reader     : subscribed_publishers, subscribed_journalists  (M2M, clearable)
    Journalist : articles and newsletters via reverse FK (author field)
    Editor     : publisher FK

    The overridden save() method enforces mutual exclusivity between reader
    and journalist fields so the database stays consistent.
    """

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
    )

    # --- Reader fields ---
    # A reader can follow many publishers and many individual journalists.
    subscribed_publishers = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='subscriber_readers',
        help_text="Publishers this reader has subscribed to.",
    )
    subscribed_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='followers',
        limit_choices_to={'role': Role.JOURNALIST},
        help_text="Individual journalists this reader follows.",
    )

    # --- Editor / Journalist field ---
    # Both editors and journalists can be affiliated with a publisher.
    publisher = models.ForeignKey(
        'Publisher',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='staff',
        help_text="The publisher this user works for (editors/journalists).",
    )

    # Override the default M2M to avoid clashes when using a custom user model
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_users',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_users',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # ------------------------------------------------------------------
    # Role helpers
    # ------------------------------------------------------------------

    @property
    def is_reader(self):
        return self.role == Role.READER

    @property
    def is_journalist(self):
        return self.role == Role.JOURNALIST

    @property
    def is_editor(self):
        return self.role == Role.EDITOR

    def save(self, *args, **kwargs):
        """
        Persist the user and then enforce role-field mutual exclusivity.

        After saving we clear any M2M data that doesn't belong to this role:
        - Non-readers have their subscription M2M sets cleared.
        - Non-journalists / non-editors have publisher set to None.
        """
        # Enforce publisher = None for readers
        if self.role == Role.READER:
            self.publisher = None

        super().save(*args, **kwargs)

        # Clear subscription fields for non-readers
        if self.role != Role.READER:
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()

    def assign_group(self):
        """
        Add this user to the Django Group that matches their role.
        Creates the group if it doesn't exist yet.
        Called from the post_save signal in signals.py.
        """
        group, _ = Group.objects.get_or_create(name=self.role.capitalize())
        self.groups.set([group])


# ---------------------------------------------------------------------------
# Article
# ---------------------------------------------------------------------------
class Article(models.Model):
    """
    A news article that may be associated with a journalist and/or a publisher.

    Approval workflow
    -----------------
    approved = False  →  draft; only visible to editors and the author.
    approved = True   →  published; visible to readers and via the API.

    When an editor sets approved = True the post_save signal (signals.py)
    emails all relevant subscribers and POSTs to /api/approved/.
    """

    title = models.CharField(max_length=300)
    content = models.TextField()

    # The journalist who wrote the article
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='authored_articles',
        limit_choices_to={'role': Role.JOURNALIST},
    )

    # Optional: the publisher the article is written for.
    # If NULL the article is "independent" (authored by a solo journalist).
    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Approval state – set by an editor
    approved = models.BooleanField(
        default=False,
        help_text="Set to True by an editor to publish the article.",
    )

    # Track who approved and when (audit trail)
    approved_by = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_articles',
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "✓" if self.approved else "⏳"
        return f"[{status}] {self.title} – {self.author.username}"


# ---------------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------------
class Newsletter(models.Model):
    """
    A curated collection of articles, published by a journalist (or editor).

    The M2M to Article allows a newsletter to reference existing articles.
    """

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # The journalist (or editor) who created this newsletter
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters',
    )

    # A newsletter can contain many articles; an article can appear in many
    # newsletters (true many-to-many).
    articles = models.ManyToManyField(
        Article,
        blank=True,
        related_name='newsletters',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"
