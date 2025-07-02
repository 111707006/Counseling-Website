# articles/serializers.py

from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """
    Article 序列化器
    - fields: 所有模型欄位都可讀寫
    - read_only_fields: 僅將 published_at 設為唯讀，由後端自動填入
    """
    class Meta:
        model = Article
        # 所有欄位都包含
        fields = ['id', 'title', 'content', 'tags', 'author', 'published_at']
        # 僅 published_at 由後端自動處理，不允許前端寫入
        read_only_fields = ['published_at']

    def create(self, validated_data):
        """
        建立文章：
        - 若 validated_data 含 author，則使用該 author
        - 否則預設使用 request.user
        """
        request = self.context.get('request', None)

        # 從 validated_data 取出 author，若無則設為當前使用者
        author = validated_data.pop('author', None)
        if not author and request and hasattr(request, 'user'):
            author = request.user

        # 建立並回傳 Article 實例
        article = Article.objects.create(author=author, **validated_data)
        return article
