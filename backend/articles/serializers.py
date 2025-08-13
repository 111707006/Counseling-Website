# articles/serializers.py

from rest_framework import serializers
from .models import Article, ArticleImage

class ArticleImageSerializer(serializers.ModelSerializer):
    """
    文章圖片序列化器
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ArticleImage
        fields = ['id', 'image', 'image_url', 'caption', 'order', 'created_at']
        read_only_fields = ['created_at']
    
    def get_image_url(self, obj):
        """返回圖片完整URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class ArticleSerializer(serializers.ModelSerializer):
    """
    Article 序列化器
    - 包含所有欄位和關聯的圖片
    - 支援特色圖片URL和作者名稱的動態欄位
    """
    featured_image_url = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    images = ArticleImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'excerpt', 'content', 'featured_image', 'featured_image_url',
            'tags', 'author', 'author_name', 'is_published', 'published_at', 'images'
        ]
        read_only_fields = ['published_at']

    def get_featured_image_url(self, obj):
        """返回特色圖片完整URL"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None

    def get_author_name(self, obj):
        """返回作者用戶名或郵箱"""
        if obj.author:
            return obj.author.username if obj.author.username else obj.author.email
        return None

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
