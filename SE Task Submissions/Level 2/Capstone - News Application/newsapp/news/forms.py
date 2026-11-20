"""
forms.py – Django forms for the HTML (template-based) frontend.

Forms defined here
------------------
  CustomUserCreationForm – registration form with role selection
  LoginForm              – username + password
  ArticleForm            – journalist writes/edits an article
  NewsletterForm         – journalist/editor creates/edits a newsletter
  SubscriptionForm       – reader updates their publisher/journalist subscriptions
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from news.models import Article, CustomUser, Newsletter, Publisher, Role


class CustomUserCreationForm(UserCreationForm):
    """
    Registration form.

    Extends Django's built-in UserCreationForm (which handles password
    confirmation) to add email and role fields.
    Editors cannot self-register; they must be created by an admin.
    """

    email = forms.EmailField(required=True, help_text="Required. Used for subscription notifications.")
    role = forms.ChoiceField(
        choices=[
            (Role.READER, 'Reader – browse articles and newsletters'),
            (Role.JOURNALIST, 'Journalist – write and publish articles'),
        ],
        initial=Role.READER,
        help_text="Editors are added by administrators only.",
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']

    def save(self, commit=True):
        """Set the role before saving so the post_save signal assigns the group."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Simple login form – username and password."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )


class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing an Article.

    The 'author' field is excluded because it is set automatically in the view
    from request.user.  'approved', 'approved_by', and 'approved_at' are also
    excluded because only editors set those fields through the approval flow.
    """

    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Article headline'}),
            'content': forms.Textarea(attrs={'rows': 15, 'placeholder': 'Write your article here...'}),
        }
        help_texts = {
            'publisher': 'Select a publisher if this article is for a publication. Leave blank for independent articles.',
        }


class NewsletterForm(forms.ModelForm):
    """
    Form for creating and editing a Newsletter.

    The 'author' field is excluded and set in the view.
    The 'articles' many-to-many field lets the user pick approved articles.
    """

    articles = forms.ModelMultipleChoiceField(
        queryset=Article.objects.filter(approved=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select the approved articles to include in this newsletter.",
    )

    class Meta:
        model = Newsletter
        fields = ['title', 'description', 'articles']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Newsletter title'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Brief description of this newsletter...'}),
        }


class SubscriptionForm(forms.ModelForm):
    """
    Allows a Reader to update which publishers and journalists they follow.
    Shown only to users with role='reader'.
    """

    subscribed_publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Receive notifications for new articles from these publishers.",
    )
    subscribed_journalists = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role=Role.JOURNALIST),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Receive notifications for new articles from these journalists.",
    )

    class Meta:
        model = CustomUser
        fields = ['subscribed_publishers', 'subscribed_journalists']
