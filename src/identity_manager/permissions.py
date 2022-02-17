from rest_framework.permissions import BasePermission,SAFE_METHODS
from identity_manager import constants
from identity_manager.models import Account

class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user==request.user


class IsLibrarianPermission(BasePermission):
    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        print(request.user, account)
        
        if account.role == constants.Account.LIBRARIAN:
            return True 
        return False


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin