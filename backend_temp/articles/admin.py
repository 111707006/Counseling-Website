from django.contrib import admin
from django.utils.html import format_html
from .models import Article, ArticleImage

class ArticleImageInline(admin.TabularInline):
    """
    文章圖片內嵌管理
    """
    model = ArticleImage
    extra = 1
    fields = ('image', 'caption', 'order', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        """顯示圖片預覽"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "無圖片"
    image_preview.short_description = "圖片預覽"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'excerpt_preview', 'featured_image_preview', 'published_at')
    list_filter = ('is_published', 'published_at', 'author')
    search_fields = ('title', 'excerpt', 'content')
    ordering = ('-published_at',)
    inlines = [ArticleImageInline]
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('title', 'excerpt', 'author', 'is_published')
        }),
        ('內容', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('特色圖片', {
            'fields': ('featured_image', 'featured_image_preview'),
            'classes': ('collapse',)
        }),
        ('分類標籤', {
            'fields': ('tags',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('featured_image_preview',)
    
    def excerpt_preview(self, obj):
        """顯示摘要預覽"""
        if obj.excerpt:
            return obj.excerpt[:50] + "..." if len(obj.excerpt) > 50 else obj.excerpt
        return "無摘要"
    excerpt_preview.short_description = "摘要預覽"
    
    def featured_image_preview(self, obj):
        """顯示特色圖片預覽"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;" />',
                obj.featured_image.url
            )
        return "無特色圖片"
    featured_image_preview.short_description = "特色圖片預覽"

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'caption', 'order', 'image_preview', 'created_at')
    list_filter = ('created_at', 'article')
    search_fields = ('article__title', 'caption')
    ordering = ('article', 'order', 'created_at')
    
    def image_preview(self, obj):
        """顯示圖片預覽"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "無圖片"
    image_preview.short_description = "圖片預覽"
