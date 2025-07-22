from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsAdminOrTherapist

class ArticleViewSet(viewsets.ModelViewSet):
    """
    文章 API：
    - list / retrieve (GET) : 公開，任何人可讀
    - create / update / delete : 僅限 admin 或 therapist
    """
    queryset = Article.objects.all().order_by('-published_at')
    serializer_class = ArticleSerializer
    # 先檢查是否登入，GET 可匿名，其他需登入；接著檢查角色
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrTherapist]

    def perform_create(self, serializer):
        """
        覆寫 create 行為，自動把 author 設為 request.user
        """
        serializer.save(author=self.request.user)
