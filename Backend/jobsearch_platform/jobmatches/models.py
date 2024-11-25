from django.db import models
from resumes.models import Resume
from jobs.models import Job

class JobMatch(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    match_percentage = models.FloatField()