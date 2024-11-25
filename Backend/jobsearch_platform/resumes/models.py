from django.db import models
from users.models import UserProfile

class Resume(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    skills = models.TextField()
    experience = models.TextField()
    education = models.TextField()