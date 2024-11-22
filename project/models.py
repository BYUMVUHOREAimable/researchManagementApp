from django.db import models
from django.contrib.auth.models import User


class ResearchProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed'), ('pending', 'Pending')])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')

    def __str__(self):
        return self.title
   
