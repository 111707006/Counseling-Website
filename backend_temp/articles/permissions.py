from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrTherapist(BasePermission):
    """
    自訂權限：僅當使用者 role 為 admin 或 therapist，
    才允許執行非安全性操作（POST、PUT、PATCH、DELETE）。
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS') 均不受此限制。
    """
    def has_permission(self, request, view):
        # 任何人都可 GET（閱讀）
        if request.method in SAFE_METHODS:
            return True
        # 非安全操作需先驗證登入，再檢查角色
        user = request.user
        return user.is_authenticated and user.is_staff 
