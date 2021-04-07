from django.urls import path
from posts import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('forgot_password/', views.forgot, name="forgot"),
    path('recover_password/', views.recover, name="recover"),
    path("posts/like/", views.likeapost, name="likeapost"),
    path("comments/like/", views.likeacomment, name="likeacomment"),
    path("comments/delete/", views.deleteacomment, name="deleteacomment"),
    path("posts/delete/", views.deletepost, name="deletepost"),
    path("posts/add", views.post_a_Post, name="addpost"),
    path("posts/<slug>/details", views.PostDetailView.as_view(), name="single_post"),
    path("posts/<pk>/details/comment", views.AddComment, name="comment_post"),
]
