from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path('', views.UserListView.as_view(), name="index"),
    path('<pk>/', views.SingleUser, name="profile_for"),
    path('upload/', views.UpdateProfileImage, name="update_image"),
    path('auth/reset_password/', views.request_code,
         name="reset_password_with_token"),
    path("auth/provide_token/", views.EnterCodeView.as_view(), name="enter_code"),
    path("<int:code>/recover/", views.ResetPassword, name="recover"),
    path('check_expiriration', views.check_expiriration,
         name='check_expiriration'),
]
