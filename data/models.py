from django.db import models

from project.models import ResearchProject
from users.models import Participant

class DataCollection(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='data_collections')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='data_collections')
    data_submission_date = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to='media/')  # Store survey data, responses, etc. 