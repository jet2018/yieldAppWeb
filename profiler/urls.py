from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path('', views.UserListView.as_view(), name="index"),
    path('<pk>/', views.SingleUser, name="profile_for"),
    path('upload/', views.UpdateProfileImage, name="update_image"),
    path('auth/reset_password/', views.ResetCode,
         name="reset_password_with_token"),
    path("auth/provide_token/", views.CheckCode, name="check_code"),
    path("<int:code>/recover/", views.ResetPassword, name="recover"),
    path('check_expiry/', views.CheckCodeExpiry, name='check_expiry'),
]
