from rest_framework import permissions

class EhSuperUsuario(permissions.BasePermission):
    """
    Permite acesso para exclusão somente a superusuários.
    """
    def has_permission(self, request, view):
      if request.method == 'DELETE':
         if request.user.is_superuser:
            return True
         return False
      return True