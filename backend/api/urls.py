from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("notes/<int:pk>/", views.NoteRetrieveAPIView.as_view(), name="note-detail"),
    path("courses/", views.CourseListCreate.as_view(), name="course-list"),
]