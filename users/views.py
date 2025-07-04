from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

class RegisterView(APIView):
    """
    使用者註冊接口（POST /api/users/register/）
    - 允許匿名存取（AllowAny）
    - 接收：username, email, password
    - 驗證資料、建立 User，並回傳 JWT tokens
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. 反序列化並驗證輸入資料
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. 建立新使用者
        user = serializer.save()

        # 3. 產生 JWT (access + refresh)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # 4. 組裝回應資料（不含 role）
        response_data = {
            "msg": "註冊成功",
            "user": {
                "username": user.username,
                "email": user.email
            },
            "token": {
                "access": access_token,
                "refresh": str(refresh)
            }
        }
        response = Response(response_data, status=status.HTTP_201_CREATED)

        # 5. 同時在 Header 裡回傳 access token
        response['Authorization'] = f"Bearer {access_token}"

        return response
