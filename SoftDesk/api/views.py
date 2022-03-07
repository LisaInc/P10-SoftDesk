from venv import create
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User

from api.permissions import UserPermission
from api.models import Contributor, Project
from api.serializers import ProjectSerializer, ContributorSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if view.action == "destroy":
            return UserPermission.is_author(view.kwargs["pk"], request.user)
        return UserPermission.is_contributor(
            request.user, view.kwargs["pk"]
        ) or UserPermission.is_author(view.kwargs["pk"], request.user)

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
        project = super().create(request, *args, **kwargs)
        ContributorSerializer.create(
            self, [self.request.user, project, "author", "author"]
        )
        return project

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if view.action == ("destroy", "put"):
            print(UserPermission.is_author(view.kwargs["pk"], request.user))
            return UserPermission.is_author(view.kwargs["pk"], request.user)
        return UserPermission.is_contributor(
            request.user, view.kwargs["pk"]
        ) or UserPermission.is_author(view.kwargs["pk"], request.user)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        queryset = Contributor.objects.filter(project=self.kwargs["projects_pk"])
        id = self.request.GET.get("id")
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["projects_pk"]
        request.POST._mutable = False
        return super(ContributorViewSet, self).create(request, *args, **kwargs)
