from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

from api.permissions import UserPermission
from api.models import Contributor, Project, Issue, Comment
from api.serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        projects = [
            contibutors.project.id
            for contibutors in Contributor.objects.filter(user=self.request.user)
        ]
        queryset = Project.objects.filter(id__in=projects)
        id = self.request.GET.get("id")
        if id is not None:
            queryset = queryset.filter(id=id)
            # ajouter les contributeurs, issues et commentaires ?
        return queryset

    def create(self, request, *args, **kwargs):
        project = super(ProjectViewSet, self).create(request, *args, **kwargs)
        project_contrib = Project.objects.filter(id=project.data["id"])
        Contributor.objects.create(
            user=self.request.user,
            project=project_contrib[0],
            permission="author",
            role="author",
        )
        return project

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return UserPermission.is_project_author(view.kwargs["pk"], request.user)
        return UserPermission.is_project_author_or_contributor(
            request.user, view.kwargs["pk"]
        )


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs["projects_pk"])

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["projects_pk"]
        request.POST._mutable = False
        return super(ContributorViewSet, self).create(request, *args, **kwargs)

    def has_permission(self, request, view):
        if view.action in ("create", "destroy"):
            return UserPermission.is_project_author(view.kwargs["pk"], request.user)
        return UserPermission.is_project_author_or_contributor(
            request.user, view.kwargs["pk"]
        )


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        queryset = Issue.objects.filter(project=self.kwargs["projects_pk"])
        id = self.request.GET.get("id")
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["issue_assignee"] = request.user.id
        request.data["issue_author"] = request.user.id
        request.data["project"] = self.kwargs["projects_pk"]
        request.POST._mutable = False
        return super(IssueViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["issue_author"] = request.user.id
        request.data["project"] = self.kwargs["projects_pk"]
        if not request.data.get("issue_assignee"):
            request.data["issue_assignee"] = request.user.id
        request.POST._mutable = False
        return super(IssueViewSet, self).update(request, *args, **kwargs)

    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            return UserPermission.is_issue_author(view.kwargs["pk"], request.user)
        return UserPermission.is_project_author_or_contributor(
            self.kwargs["projects_pk"], request.user
        )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        print(self.request.user.id)
        queryset = Comment.objects.filter(issue=self.kwargs["issues_pk"])
        id = self.request.GET.get("id")
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["comment_author"] = request.user.id
        request.data["issue"] = self.kwargs["issues_pk"]
        request.POST._mutable = False
        return super(CommentViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["comment_author"] = request.user.id
        request.data["issue"] = self.kwargs["issues_pk"]
        request.POST._mutable = False
        return super(CommentViewSet, self).update(request, *args, **kwargs)

    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            return UserPermission.is_comment_author(view.kwargs["pk"], request.user)
        return UserPermission.is_project_author_or_contributor(
            self.kwargs["projects_pk"], request.user
        )
