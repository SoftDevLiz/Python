"""
serializers.py – Django REST Framework serializers.

Serializers convert between Python model instances and JSON.  Think of
them like Django forms, but for API input/output.

Serializers defined here
------------------------
  PublisherSerializer   – basic publisher info
  UserSerializer        – safe user representation (no password)
  ArticleSerializer     – article with nested author/publisher names
  NewsletterSerializer  – newsletter with nested articles
  ApprovedArticleLogSerializer – payload shape for POST /api/approved/
  RegisterSerializer    – user registration via the API
"""

from rest_framework import serializers
from news.models import Article, CustomUser, Newsletter, Publisher


# ---------------------------------------------------------------------------
# Publisher
# ---------------------------------------------------------------------------
class PublisherSerializer(serializers.ModelSerializer):
    """Serializes all Publisher fields for read and write."""

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description', 'website', 'created_at']
        read_only_fields = ['id', 'created_at']


# ---------------------------------------------------------------------------
# CustomUser
# ---------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """
    A safe representation of a user.

    Password is excluded from all output.
    subscribed_publishers and subscribed_journalists use PrimaryKeyRelatedField
    so that readers can update their subscriptions by posting IDs.
    """

    subscribed_publishers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Publisher.objects.all(),
        required=False,
    )
    subscribed_journalists = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.filter(role='journalist'),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'publisher',
            'subscribed_publishers', 'subscribed_journalists',
        ]
        read_only_fields = ['id', 'role']


# ---------------------------------------------------------------------------
# Article
# ---------------------------------------------------------------------------
class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializes Article for both read and write operations.

    - author_name : read-only derived field (display name)
    - publisher_name : read-only derived field
    - author is set automatically from request.user in the view; clients
      do not supply it.
    """

    author_name = serializers.SerializerMethodField()
    publisher_name = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content',
            'author', 'author_name',
            'publisher', 'publisher_name',
            'approved', 'approved_by', 'approved_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'author', 'approved', 'approved_by',
            'approved_at', 'created_at', 'updated_at',
        ]

    def get_author_name(self, obj):
        """Return the author's full name or username as a fallback."""
        return obj.author.get_full_name() or obj.author.username

    def get_publisher_name(self, obj):
        """Return the publisher name, or 'Independent' if none."""
        return obj.publisher.name if obj.publisher else 'Independent'

    def create(self, validated_data):
        """
        Automatically assign the authenticated user as the article author.
        The view passes request.user via the serializer context.
        """
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


# ---------------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------------
class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializes Newsletter.

    articles is a writable many-to-many field; clients send a list of
    Article IDs and Django handles the join table.
    """

    author_name = serializers.SerializerMethodField()
    # Return full article objects on read; accept IDs on write
    articles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Article.objects.filter(approved=True),
    )

    class Meta:
        model = Newsletter
        fields = [
            'id', 'title', 'description',
            'author', 'author_name',
            'articles',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username

    def create(self, validated_data):
        """Assign the authenticated user as author when creating."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


# ---------------------------------------------------------------------------
# ApprovedArticleLog – for POST /api/approved/
# ---------------------------------------------------------------------------
class ApprovedArticleLogSerializer(serializers.Serializer):
    """
    Validates the payload that the signal (or approval view) POSTs to
    /api/approved/.  This endpoint is an internal integration point.

    Fields mirror what signals.py sends in _post_to_approved_endpoint().
    """

    article_id = serializers.IntegerField()
    title = serializers.CharField(max_length=300)
    author = serializers.CharField(max_length=150)
    publisher = serializers.CharField(max_length=255, allow_null=True, required=False)
    approved_at = serializers.DateTimeField(allow_null=True, required=False)


# ---------------------------------------------------------------------------
# Register (create account via the API)
# ---------------------------------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    """
    Allows new users to register through the API.

    password is write-only (never returned in responses).
    role is accepted on creation so users self-select Reader / Journalist.
    Editors should be created through the admin panel.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        """Use create_user() so the password is hashed correctly."""
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
