from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: чтение для всех, изменение только для владельца.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Разрешаем изменение только владельцу
        return obj.created_by == request.user

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение: только владелец или администратор могут изменять/удалять.
    """
    def has_object_permission(self, request, view, obj):
        # Администратор может всё
        if request.user.is_staff:
            return True
        
        # Проверяем владельца
        return obj.created_by == request.user

class CanEditAllOrOwner(permissions.BasePermission):
    """
    Разрешение: пользователи с особым правом могут редактировать всё,
    остальные - только свои объекты.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Проверяем специальные права
        if request.user.has_perm(f'{obj._meta.app_label}.can_edit_all_{obj._meta.model_name}'):
            return True
        
        # Проверяем владельца
        return obj.created_by == request.user
