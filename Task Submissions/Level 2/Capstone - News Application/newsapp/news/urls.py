"""
urls.py – URL routing for the news application.

Web (HTML) routes
-----------------
  /                            home
  /articles/<pk>/              article_detail
  /articles/create/            article_create
  /articles/<pk>/edit/         article_edit
  /articles/<pk>/delete/       article_delete
  /newsletters/                newsletter_list
  /newsletters/<pk>/           newsletter_detail
  /newsletters/create/         newsletter_create
  /newsletters/<pk>/edit/      newsletter_edit
  /editor/                     editor_dashboard
  /editor/approve/<pk>/        approve_article
  /register/                   register
  /login/                      login_view
  /logout/                     logout_view
  /profile/                    profile

REST API routes
---------------
  /api/register/               RegisterView
  /api/token/                  TokenObtainPairView (JWT login)
  /api/token/refresh/          TokenRefreshView
  /api/articles/               ArticleListCreateView
  /api/articles/subscribed/    SubscribedArticlesView  ← must come before <pk>
  /api/articles/<pk>/          ArticleDetailView
  /api/articles/<pk>/approve/  ArticleApproveView
  /api/newsletters/            NewsletterListCreateView
  /api/newsletters/<pk>/       NewsletterDetailView
  /api/approved/               ApprovedArticleLogView
  /api/publishers/             PublisherListView
  /api/publishers/<pk>/        PublisherDetailView
  /api/profile/                UserProfileView
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from news import api_views, views

urlpatterns = [
    # -----------------------------------------------------------------------
    # Web (HTML) views
    # -----------------------------------------------------------------------
    path('', views.home, name='home'),

    # Articles
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),

    # Newsletters
    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/<int:pk>/', views.newsletter_detail, name='newsletter_detail'),
    path('newsletters/create/', views.newsletter_create, name='newsletter_create'),
    path('newsletters/<int:pk>/edit/', views.newsletter_edit, name='newsletter_edit'),

    # Editor
    path('editor/', views.editor_dashboard, name='editor_dashboard'),
    path('editor/approve/<int:pk>/', views.approve_article, name='approve_article'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    # -----------------------------------------------------------------------
    # REST API
    # -----------------------------------------------------------------------
    # Auth
    path('api/register/', api_views.RegisterView.as_view(), name='api_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='api_token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),

    # Articles – NOTE: 'subscribed' path MUST come before '<int:pk>' path
    path('api/articles/', api_views.ArticleListCreateView.as_view(), name='api_article_list'),
    path('api/articles/subscribed/', api_views.SubscribedArticlesView.as_view(), name='api_subscribed_articles'),
    path('api/articles/<int:pk>/', api_views.ArticleDetailView.as_view(), name='api_article_detail'),
    path('api/articles/<int:pk>/approve/', api_views.ArticleApproveView.as_view(), name='api_article_approve'),

    # Newsletters
    path('api/newsletters/', api_views.NewsletterListCreateView.as_view(), name='api_newsletter_list'),
    path('api/newsletters/<int:pk>/', api_views.NewsletterDetailView.as_view(), name='api_newsletter_detail'),

    # Internal integration log
    path('api/approved/', api_views.ApprovedArticleLogView.as_view(), name='api_approved_log'),

    # Publishers
    path('api/publishers/', api_views.PublisherListView.as_view(), name='api_publisher_list'),
    path('api/publishers/<int:pk>/', api_views.PublisherDetailView.as_view(), name='api_publisher_detail'),

    # Profile
    path('api/profile/', api_views.UserProfileView.as_view(), name='api_profile'),
]
