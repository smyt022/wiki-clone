from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryTitle>", views.entry_page, name="getEntry"),
    path("createNewEntry", views.entry_creation_page, name="createNewEntry"),
    path("editAnEntry/<str:entryTitle>", views.entry_editing_page, name = "editEntry"),
    path("addEntryFile", views.entry_mdFile_creation,name="createMdFile"),
    path("editEntryFile", views.entry_mdFile_edit, name="editMdFile"),
    path("randomEntry", views.random_entry, name="getRandomEntry")

]
