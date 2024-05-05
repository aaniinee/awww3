from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='images'),
    path('<int:image_id>/', views.image_display, name='image_display'),
]