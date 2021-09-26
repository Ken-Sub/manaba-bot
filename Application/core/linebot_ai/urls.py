from django.urls import path
from . import views

app_name = "linebot_ai"

urlpatterns = [
    path('callback/', views.callback, name='callback'),
    path('edit/<str:num>/<str:name>/', views.edit, name='edit'),
    path('success/', views.success, name='success')
]