from django.urls import path
from .views import upload_resume, list_resumes

urlpatterns = [
    path('upload/', upload_resume, name='upload_resume'),
    path('list/', list_resumes, name='list_resumes'),
]