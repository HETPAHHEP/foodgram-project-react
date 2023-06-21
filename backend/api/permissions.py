from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerAdminOrReadOnly(BasePermission):
    """
    Разрешает владельцу взаимодействовать
    полностью или только читать
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and

            (obj.author == request.user or
             request.user.is_staff)
        )
