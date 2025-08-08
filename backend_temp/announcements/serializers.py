from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AnnouncementCategory, Announcement, AnnouncementImage

User = get_user_model()


class AnnouncementCategorySerializer(serializers.ModelSerializer):
    """公告分類序列化器"""
    announcements_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnouncementCategory
        fields = [
            'id', 'name', 'description', 'color', 'is_active', 
            'order', 'announcements_count', 'created_at'
        ]
    
    def get_announcements_count(self, obj):
        """獲取該分類已發布的公告數量"""
        return obj.announcements.filter(status='published').count()


class AnnouncementImageSerializer(serializers.ModelSerializer):
    """公告圖片序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnouncementImage
        fields = ['id', 'image', 'image_url', 'caption', 'order', 'created_at']
    
    def get_image_url(self, obj):
        """獲取完整的圖片URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AuthorSerializer(serializers.ModelSerializer):
    """作者序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class AnnouncementListSerializer(serializers.ModelSerializer):
    """公告列表序列化器（簡化版本）"""
    category = AnnouncementCategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    can_display = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'summary', 'category', 'featured_image_url',
            'priority', 'priority_display', 'status', 'status_display',
            'is_pinned', 'show_on_homepage', 'publish_date', 'expire_date',
            'author', 'views_count', 'likes_count', 'can_display',
            'created_at', 'updated_at'
        ]
    
    def get_featured_image_url(self, obj):
        """獲取特色圖片完整URL"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    """公告詳細序列化器"""
    category = AnnouncementCategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    additional_images = AnnouncementImageSerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    can_display = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'summary', 'content', 'category', 
            'featured_image_url', 'additional_images',
            'priority', 'priority_display', 'status', 'status_display',
            'is_pinned', 'show_on_homepage', 'publish_date', 'expire_date',
            'author', 'views_count', 'likes_count', 'can_display',
            'created_at', 'updated_at'
        ]
    
    def get_featured_image_url(self, obj):
        """獲取特色圖片完整URL"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class AnnouncementCreateUpdateSerializer(serializers.ModelSerializer):
    """公告創建/更新序列化器"""
    
    class Meta:
        model = Announcement
        fields = [
            'title', 'summary', 'content', 'category',
            'featured_image', 'priority', 'status', 
            'is_pinned', 'show_on_homepage', 
            'publish_date', 'expire_date'
        ]
    
    def validate(self, data):
        """驗證數據"""
        # 如果設定為已發布但沒有發布時間，使用當前時間
        if data.get('status') == 'published' and not data.get('publish_date'):
            from django.utils import timezone
            data['publish_date'] = timezone.now()
        
        # 檢查過期時間不能早於發布時間
        publish_date = data.get('publish_date')
        expire_date = data.get('expire_date')
        if publish_date and expire_date and expire_date <= publish_date:
            raise serializers.ValidationError({
                'expire_date': '過期時間不能早於或等於發布時間'
            })
        
        return data
    
    def create(self, validated_data):
        """創建公告時自動設定作者"""
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)


# 首頁用的簡化序列化器
class AnnouncementHomepageSerializer(serializers.ModelSerializer):
    """首頁公告序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'summary', 'category_name', 'category_color',
            'featured_image_url', 'priority', 'is_pinned', 'publish_date'
        ]
    
    def get_featured_image_url(self, obj):
        """獲取特色圖片完整URL"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None