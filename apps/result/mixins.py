from django.core.exceptions import PermissionDenied

class CheckTeacherGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name = "Teacher").exists():
            return super().dispatch(self, request, *args, **kwargs)
        else:
            raise PermissionDenied