from django.contrib import admin
from django.urls import path
from shop import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.reg_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('create-store/', views.create_store, name='create_store'),
    path('dashboard/', views.store_dashboard, name='dashboard'),
    path('dashboard/add-product/', views.add_product, name='add_product'),
    path('product/edit/<int:product_id>/',
         views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/',
         views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/',
         views.leave_review, name='leave_review'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('store/delete/', views.delete_store, name='delete_store'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
