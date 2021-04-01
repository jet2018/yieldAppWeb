from django.urls import path
from diagnosis import views

app_name = 'diagonise'
urlpatterns = [
	path('', views.DiagoniseView.as_view(), name="index"),
	path('test_response/', views.analyse, name="analyse"),
	path('responses/', views.resultsPage, name="results"),
]