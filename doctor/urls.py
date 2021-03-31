from django.urls import path
from . import views

app_name = 'doctor'
urlpatterns = [
	path('', views.DoctorListView.as_view(), name="index"),
	path('star/', views.starAdoctor, name="star"),
	path('notify/', views.sendNotification, name="notify"), 
	path('notification/', views.getNotifications, name="notifications"),
	path('all_notofications/', views.getAllNotifications.as_view(), name="all_notifications"),
	path('compose/', views.ComposeNotification, name="compose"),
	path('mark_as_read/', views.markAllAsRead, name="mark_as_read"),
	path('delete_notification/', views.DeleteEmail, name="delete_notification"),
	path('delete_notification_sent/', views.DeleteEmailSent, name="delete_notification_sent"),
	path('mark_one_as_read/', views.MarkOneAsRead, name="mark_one_as_read"),
	path('submit_reply/<int:id>', views.replySubmit, name="submit_reply"),
	path('delete_reply/<int:id>', views.deleteReply, name="deleteReply"),
	path('notifications/<int:pk>/read', views.NotificationsDetailView.as_view(), name="read_notification"),
]