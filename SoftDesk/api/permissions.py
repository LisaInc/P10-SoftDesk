from rest_framework.permissions import BasePermission
from .models import Contributor


class UserPermission(BasePermission):
    def is_author(self, project, user):
        return bool(
            len(queryset=Contributor.objects.filter(project=project, user=user))
        )
