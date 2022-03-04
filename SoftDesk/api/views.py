from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User

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

    def get_queryset(self):

        projects_id = [
            contibutors.project_id
            for contibutors in Contributor.objects.filter(user_id=self.request.user.id)
        ]
        print(self.request.user)
        queryset = Project.objects.all()  # filter(id__in=projects_id)
        id = self.request.GET.get("id")
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        queryset = Contributor.objects.filter(project_id=self.kwargs["projects_id"])
        id = self.request.GET.get("id")
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
