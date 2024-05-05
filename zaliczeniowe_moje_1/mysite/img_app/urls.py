from django.urls import path

from . import views

urlpatterns = [
    path("", views.ImagesList.as_view(), name="index"),
    path("<int:pk>/", views.ImageDisplay.as_view(), name="image_display"),
    path("<int:pk>/edit/", views.ImageEdit.as_view(), name="edit"),
    path("<int:pk>/rectangle_add/", views.RectangleAdd.as_view(), name="rectangle_add"),
    path("<int:pk>/rectangle_delete/", views.RectangleDelete.as_view(), name="rectangle_delete"),
]