from django.urls import path
from . import views

app_name = 'quest'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('requestform/', views.RequestForm.as_view(), name = 'requestform'),
]
