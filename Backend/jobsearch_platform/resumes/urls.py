from django.urls import path
from .views import upload_resume_and_parse

urlpatterns = [
    path('upload/', upload_resume_and_parse, name='upload_resume'),
]