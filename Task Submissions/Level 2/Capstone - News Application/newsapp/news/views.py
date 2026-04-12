"""
views.py – Django template-based (HTML) views for the News Application.

These views render HTML templates for the browser-facing part of the site.
The REST API has its own views in api_views.py.

Views defined here
------------------
  home                – public landing page; lists approved articles
  article_detail      – read a single article
  article_create      – journalist: write a new article
  article_edit        – journalist/editor: edit an article
  article_delete      – journalist/editor: delete an article
  editor_dashboard    – editor: see all pending articles, approve them
  approve_article     – editor: POST to approve a single article (web flow)
  newsletter_list     – list all newsletters
  newsletter_detail   – view a newsletter and its articles
  newsletter_create   – journalist/editor: create a newsletter
  newsletter_edit     – journalist/editor: edit a newsletter
  register            – public: create a new account
  login_view          – public: log in
  logout_view         – log out
  profile             – reader: manage subscriptions
"""

import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from news.forms import (
    ArticleForm,
    CustomUserCreationForm,
    LoginForm,
    NewsletterForm,
    SubscriptionForm,
)
from news.models import Article, CustomUser, Newsletter, Publisher

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Role-check helpers for @user_passes_test
# ---------------------------------------------------------------------------
def _is_editor(user):
    return user.is_authenticated and user.role == 'editor'


def _is_journalist(user):
    return user.is_authenticated and user.role == 'journalist'


def _is_editor_or_journalist(user):
    return user.is_authenticated and user.role in ('editor', 'journalist')


# ---------------------------------------------------------------------------
# Public / reader views
# ---------------------------------------------------------------------------

def home(request):
    """
    Landing page.  Shows all approved articles, newest first.
    Any visitor (including unauthenticated) can see this page.
    """
    articles = Article.objects.filter(approved=True).select_related('author', 'publisher')
    return render(request, 'news/home.html', {'articles': articles})


def article_detail(request, pk):
    """Show a single approved article.  Editors also see draft articles."""
    if request.user.is_authenticated and request.user.role == 'editor':
        article = get_object_or_404(Article, pk=pk)
    else:
        article = get_object_or_404(Article, pk=pk, approved=True)

    return render(request, 'news/article_detail.html', {'article': article})


def newsletter_list(request):
    """Display all newsletters.  Open to all authenticated users."""
    newsletters = Newsletter.objects.select_related('author').all()
    return render(request, 'news/newsletter_list.html', {'newsletters': newsletters})


def newsletter_detail(request, pk):
    """Display a single newsletter with its articles."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'news/newsletter_detail.html', {'newsletter': newsletter})


# ---------------------------------------------------------------------------
# Journalist views
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_journalist, login_url='/login/')
def article_create(request):
    """
    Journalists create new articles here.

    GET  → render a blank ArticleForm
    POST → validate, save, redirect to the new article
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Set author to logged-in journalist
            article.save()
            messages.success(request, "Article submitted for editor review.")
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()

    return render(request, 'news/article_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(_is_editor_or_journalist, login_url='/login/')
def article_edit(request, pk):
    """
    Editors and the original journalist can edit an article.
    Editors can edit any article; journalists can only edit their own.
    """
    article = get_object_or_404(Article, pk=pk)

    # Journalists can only edit their own articles
    if request.user.role == 'journalist' and article.author != request.user:
        messages.error(request, "You can only edit your own articles.")
        return redirect('home')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully.")
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'news/article_form.html', {'form': form, 'action': 'Edit', 'article': article})


@login_required
@user_passes_test(_is_editor_or_journalist, login_url='/login/')
def article_delete(request, pk):
    """
    Confirm and delete an article.
    GET  → confirmation page
    POST → delete and redirect home
    """
    article = get_object_or_404(Article, pk=pk)

    # Journalists can only delete their own articles
    if request.user.role == 'journalist' and article.author != request.user:
        messages.error(request, "You can only delete your own articles.")
        return redirect('home')

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article deleted.")
        return redirect('home')

    return render(request, 'news/article_confirm_delete.html', {'article': article})


# ---------------------------------------------------------------------------
# Editor views
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_editor, login_url='/login/')
def editor_dashboard(request):
    """
    Editor-only dashboard.  Shows pending (unapproved) articles that need
    review, as well as all approved articles for reference.
    """
    pending = Article.objects.filter(approved=False).select_related('author', 'publisher')
    approved = Article.objects.filter(approved=True).select_related('author', 'publisher')
    return render(request, 'news/editor_dashboard.html', {
        'pending_articles': pending,
        'approved_articles': approved,
    })


@login_required
@user_passes_test(_is_editor, login_url='/login/')
def approve_article(request, pk):
    """
    POST-only view.  The editor clicks "Approve" on the dashboard and this
    view sets the article to approved, triggering the post_save signal.
    """
    if request.method != 'POST':
        return redirect('editor_dashboard')

    article = get_object_or_404(Article, pk=pk)

    if article.approved:
        messages.info(request, "That article is already approved.")
        return redirect('editor_dashboard')

    # Stamp the private flag so signals.py knows this is a fresh approval
    article._approval_just_set = True
    article.approved = True
    article.approved_by = request.user
    article.approved_at = timezone.now()
    article.save()

    messages.success(request, f"Article '{article.title}' has been approved and subscribers notified.")
    logger.info("Editor '%s' approved article id=%d.", request.user.username, article.pk)

    return redirect('editor_dashboard')


# ---------------------------------------------------------------------------
# Newsletter management (journalists and editors)
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_editor_or_journalist, login_url='/login/')
def newsletter_create(request):
    """Create a new newsletter."""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            # M2M must be saved after the instance exists
            form.save_m2m()
            messages.success(request, "Newsletter created successfully.")
            return redirect('newsletter_detail', pk=newsletter.pk)
    else:
        form = NewsletterForm()

    return render(request, 'news/newsletter_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(_is_editor_or_journalist, login_url='/login/')
def newsletter_edit(request, pk):
    """Edit an existing newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)

    # Journalists can only edit their own newsletters
    if request.user.role == 'journalist' and newsletter.author != request.user:
        messages.error(request, "You can only edit your own newsletters.")
        return redirect('newsletter_list')

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated.")
            return redirect('newsletter_detail', pk=newsletter.pk)
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, 'news/newsletter_form.html', {
        'form': form,
        'action': 'Edit',
        'newsletter': newsletter,
    })


# ---------------------------------------------------------------------------
# Authentication views
# ---------------------------------------------------------------------------

def register(request):
    """Allow new users to register with a role (Reader or Journalist)."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'news/register.html', {'form': form})


def login_view(request):
    """Log in an existing user."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                # Redirect editors to their dashboard, others to home
                next_url = request.GET.get('next', 'editor_dashboard' if user.role == 'editor' else 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'news/login.html', {'form': form})


def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def profile(request):
    """
    Reader profile page where readers manage their subscriptions.
    Journalists and editors see their authored content instead.
    """
    user = request.user

    if request.method == 'POST' and user.role == 'reader':
        form = SubscriptionForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscriptions updated.")
            return redirect('profile')
    else:
        form = SubscriptionForm(instance=user) if user.role == 'reader' else None

    context = {
        'user': user,
        'subscription_form': form,
    }

    if user.role == 'journalist':
        context['my_articles'] = Article.objects.filter(author=user)
        context['my_newsletters'] = Newsletter.objects.filter(author=user)

    return render(request, 'news/profile.html', context)
