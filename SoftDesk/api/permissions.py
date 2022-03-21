from rest_framework.permissions import BasePermission
from .models import Contributor, Issue, Comment


class UserPermission(BasePermission):
    def is_project_author(self, project, user):
        return bool(
            Contributor.objects.filter(project=project, user=user, permission="author")
        )

    def is_project_author_or_contributor(self, project, user):
        return bool(Contributor.objects.filter(project=project, user=user))

    def is_issue_author(self, issue, user):
        return bool(Issue.objects.filter(issue=issue, issue_author=user))

    def is_issue_assigne_or_author(self, issue, user):
        return bool(
            Issue.objects.filter(issue=issue, issue_author=user)
            + Issue.objects.filter(issue=issue, issue_assignee=user)
        )

    def is_comment_author(self, comment, user):
        return bool(Comment.objects.filter(comment=comment, comment_author=user))
