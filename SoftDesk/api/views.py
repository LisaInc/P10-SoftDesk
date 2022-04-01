from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from api.permissions import (
    ProjectPermissions,
    ContributorPermissions,
    IssuePermissions,
    CommentPermissions,
)
from api.models import Project, Contributor, Issue, Comment
from api.serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]
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


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [ContributorPermissions]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs["projects_pk"])

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["projects_pk"]
        request.POST._mutable = False
        return super(ContributorViewSet, self).create(request, *args, **kwargs)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IssuePermissions]
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


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
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
