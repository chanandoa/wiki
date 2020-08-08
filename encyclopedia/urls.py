from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("edit/<str:title_edit>", views.edit, name="edit"),
    path("randompage", views.randompage, name="randompage")
]
