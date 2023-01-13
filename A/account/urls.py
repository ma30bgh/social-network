from django.urls import path
from . import views

app_name = 'account'

#namespace

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='reset_password_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='user_unfollow'),
]
