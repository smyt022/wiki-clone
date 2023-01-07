from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryTitle>", views.entry_page, name="getEntry"),
    path("createNewEntry", views.entry_creation_page, name="createNewEntry"),
    path("addEntryFile", views.entry_mdFile_creation,name="createMdFile")
]
