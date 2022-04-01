from rest_framework.permissions import BasePermission
from .models import Contributor, Issue, Comment


class UserPermission:
    def is_project_author(project, user):
        return bool(
            Contributor.objects.filter(project=project, user=user, permission="author")
        )

    def is_project_author_or_contributor(project, user):
        return bool(Contributor.objects.filter(project=project, user=user))

    def is_issue_author(issue, user):
        return bool(Issue.objects.filter(id=issue, issue_author=user))

    def is_issue_assigne_or_author(issue, user):
        return bool(
            Issue.objects.filter(id=issue, issue_author=user)
            + Issue.objects.filter(id=issue, issue_assignee=user)
        )

    def is_comment_author(comment, user):
        return bool(Comment.objects.filter(id=comment, comment_author=user))


class ProjectPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("create", "list"):
            return True
        if view.action in ("destroy", "update"):
            return UserPermission.is_project_author(view.kwargs["pk"], request.user)
        return UserPermission.is_project_author_or_contributor(
            view.kwargs["pk"], request.user
        )


class ContributorPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("list"):
            return True
        return UserPermission.is_project_author(
            view.kwargs["projects_pk"], request.user
        )


class IssuePermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            return UserPermission.is_issue_author(view.kwargs["pk"], request.user)
        return UserPermission.is_project_author_or_contributor(
            view.kwargs["projects_pk"], request.user
        )


class CommentPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            return UserPermission.is_comment_author(view.kwargs["pk"], request.user)
        return UserPermission.is_project_author_or_contributor(
            view.kwargs["projects_pk"], request.user
        )
