from django.urls import path
from . import views

app_name = 'account'

#namespace

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
]
