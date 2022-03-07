from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers
from rest_framework_nested import routers

from api.views import RegisterView, ProjectViewSet, ContributorViewSet

router = routers.SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

projects_router = routers.NestedSimpleRouter(router, "projects", lookup="projects")
projects_router.register("users", ContributorViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="obtain_tokens"),
    path("signup/", RegisterView.as_view(), name="auth_register"),
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
]
