from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from project.models import ResearchProject


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('researcher', 'Researcher'),
        ('participant', 'Participant')
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="User")
    

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant_info')
    status = models.CharField(max_length=50, choices=[('enrolled', 'Enrolled'), ('inactive', 'Inactive')])
    project = models.ForeignKey(ResearchProject, on_delete=models.SET_NULL, null=True, blank=True, related_name='participants')

    def __str__(self):
        return self.user.username
