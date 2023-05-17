from django.urls import path
from app.views import Notes, NoteDetail

urlpatterns = [
    path('', Notes.as_view()),
    path('<str:pk>', NoteDetail.as_view())
]