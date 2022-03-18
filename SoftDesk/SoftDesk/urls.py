from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers
from rest_framework_nested import routers

from api.views import (
    RegisterView,
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)

router = routers.SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

projects_router = routers.NestedSimpleRouter(router, "projects", lookup="projects")
projects_router.register("users", ContributorViewSet, basename="users")
projects_router.register("issues", IssueViewSet, basename="issues")

issues_router = routers.NestedSimpleRouter(projects_router, "issues", lookup="issues")
issues_router.register("comments", CommentViewSet, basename="comments")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="obtain_tokens"),
    path("signup/", RegisterView.as_view(), name="auth_register"),
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
]
