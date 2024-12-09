from django.urls import path
from .views import upload_resume_and_parse, get_resume_details

urlpatterns = [
    path('upload/', upload_resume_and_parse, name='upload_resume'),
    path('<int:resume_id>/', get_resume_details, name='get_resume_details'),
]