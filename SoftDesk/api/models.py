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
    PERMISSIONS = [("author", "author"), ("contributor", "Contributor")]
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey("api.Project", on_delete=models.CASCADE)
    permission = models.CharField(max_length=255, choices=PERMISSIONS)
    role = models.CharField(max_length=255)


class Issue(models.Model):
    PRIORITY = [
        ("crit", "critical"),
        ("hight", "hight"),
        ("medium", "medium"),
        ("low", "low"),
    ]
    STATUS = [
        ("todo", "to-do"),
        ("ongoing", "ongoing"),
        ("review", "in review"),
        ("done", "done"),
    ]
    issue_title = models.CharField(max_length=255)
    issue_description = models.TextField(blank=True)
    tag = models.TextField(blank=True)
    priority = models.CharField(max_length=255, choices=PRIORITY)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="project"
    )
    status = models.CharField(max_length=255, choices=STATUS)
    issue_author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="issue_author"
    )
    issue_assignee = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="issue_assignee"
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_description = models.TextField(max_length=255)
    comment_author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comment_author"
    )
    issue = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE, related_name="comment_issue"
    )
