from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("page_submission", views.page_submission, name="page_submission"),
    path("page_creation", views.page_creation, name="page_creation"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("update/<str:title>", views.update, name="update")
]
