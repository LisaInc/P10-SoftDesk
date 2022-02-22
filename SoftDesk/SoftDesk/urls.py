from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from api.views import RegisterView, ProjectViewSet

router = routers.SimpleRouter()
router.register("project", ProjectViewSet, basename="project")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="obtain_tokens"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("api/", include(router.urls)),
