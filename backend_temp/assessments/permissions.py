from rest_framework.permissions import BasePermission

class AllowAnyButSaveIfAuth(BasePermission):
    """匿名可填，但登入後才將 user 存入紀錄"""
    def has_permission(self, request, view):
        return True
