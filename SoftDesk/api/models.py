from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    TYPES = [
        ("back", "back-end"),
        ("front", "front-end"),
        ("ios", "iOS"),
        ("android", "Android"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=255, choices=TYPES)


class Contributor(models.Model):
    PERMISSIONS = [("autor", "Autor"), ("contributor", "Contributor")]
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_id = models.ForeignKey("api.Project", on_delete=models.CASCADE)
    permission = models.CharField(max_length=255, choices=PERMISSIONS)
    role = models.CharField(max_length=255)
