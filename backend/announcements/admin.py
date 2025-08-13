from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from .models import AnnouncementCategory, Announcement, AnnouncementImage


class AnnouncementImageInline(admin.TabularInline):
    """公告附加圖片內聯編輯"""
    model = AnnouncementImage
    extra = 1
    fields = ['image', 'caption', 'order']
    ordering = ['order']


@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'is_active', 'order', 'announcements_count', 'created_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    def color_display(self, obj):
        """顯示顏色標籤"""
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = '顏色'
    
    def announcements_count(self, obj):
        """顯示該分類的公告數量"""
        count = obj.announcements.filter(status='published').count()
        if count > 0:
            url = reverse('admin:announcements_announcement_changelist')
            return format_html(
                '<a href="{}?category__id={}">{} 篇</a>',
                url, obj.id, count
            )
        return '0 篇'
    announcements_count.short_description = '已發布公告'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 
        'is_pinned', 'show_on_homepage', 'author', 'views_count', 
        'publish_date', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'is_pinned', 
        'show_on_homepage', 'publish_date', 'created_at'
    ]
    search_fields = ['title', 'summary', 'content']
    list_editable = ['status', 'is_pinned', 'show_on_homepage']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('title', 'summary', 'category', 'author')
        }),
        ('內容', {
            'fields': ('content', 'featured_image'),
            'classes': ['wide']
        }),
        ('發布設定', {
            'fields': (
                'status', 'is_pinned', 'show_on_homepage',
                'publish_date', 'expire_date'
            ),
            'classes': ['collapse']
        }),
        ('統計資訊', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ['collapse']
        })
    )
    
    inlines = [AnnouncementImageInline]
    
    # 批量操作
    actions = ['make_published', 'make_draft', 'make_pinned', 'make_unpinned']
    
    def status_display(self, obj):
        """狀態顯示"""
        colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'archived': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = '狀態'
    
    
    def save_model(self, request, obj, form, change):
        """保存時自動設定作者"""
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def make_published(self, request, queryset):
        """批量發布"""
        updated = queryset.update(status='published')
        # 為沒有發布時間的項目設定發布時間
        for obj in queryset.filter(publish_date__isnull=True):
            obj.publish_date = timezone.now()
            obj.save(update_fields=['publish_date'])
        self.message_user(request, f'已發布 {updated} 篇公告')
    make_published.short_description = '發布選中的公告'
    
    def make_draft(self, request, queryset):
        """批量設為草稿"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'已設為草稿 {updated} 篇公告')
    make_draft.short_description = '設為草稿'
    
    def make_pinned(self, request, queryset):
        """批量置頂"""
        updated = queryset.update(is_pinned=True)
        self.message_user(request, f'已置頂 {updated} 篇公告')
    make_pinned.short_description = '置頂選中的公告'
    
    def make_unpinned(self, request, queryset):
        """批量取消置頂"""
        updated = queryset.update(is_pinned=False)
        self.message_user(request, f'已取消置頂 {updated} 篇公告')
    make_unpinned.short_description = '取消置頂'
    
    def get_queryset(self, request):
        """優化查詢"""
        return super().get_queryset(request).select_related('category', 'author')


@admin.register(AnnouncementImage)
class AnnouncementImageAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'image', 'caption', 'order', 'created_at']
    list_filter = ['announcement__category', 'created_at']
    search_fields = ['announcement__title', 'caption']
    list_editable = ['caption', 'order']
    ordering = ['announcement', 'order']
    
    def get_queryset(self, request):
        """優化查詢"""
        return super().get_queryset(request).select_related('announcement')
