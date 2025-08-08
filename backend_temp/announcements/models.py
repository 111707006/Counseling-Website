from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
import os

User = get_user_model()

class AnnouncementCategory(models.Model):
    """最新消息分類"""
    name = models.CharField(max_length=50, verbose_name="分類名稱")
    description = models.TextField(blank=True, verbose_name="分類說明")
    color = models.CharField(
        max_length=7, 
        default="#007bff", 
        help_text="分類標籤顏色，例如: #007bff",
        verbose_name="標籤顏色"
    )
    is_active = models.BooleanField(default=True, verbose_name="啟用狀態")
    order = models.IntegerField(default=0, help_text="排序權重，數字越小排序越前", verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "公告分類"
        verbose_name_plural = "公告分類"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Announcement(models.Model):
    """最新消息/公告"""
    
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已發布'),
        ('archived', '已封存'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '一般'),
        ('medium', '重要'),
        ('high', '緊急'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="標題")
    summary = models.CharField(
        max_length=300, 
        blank=True, 
        help_text="簡短摘要，將顯示在列表頁面",
        verbose_name="摘要"
    )
    content = RichTextUploadingField(
        verbose_name="內容",
        help_text="支援富文本編輯，可插入圖片和連結"
    )
    category = models.ForeignKey(
        AnnouncementCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='announcements',
        verbose_name="分類"
    )
    featured_image = models.ImageField(
        upload_to='announcements/featured/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="特色圖片，建議尺寸: 800x400px",
        verbose_name="特色圖片"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='low',
        verbose_name="重要程度"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="狀態"
    )
    is_pinned = models.BooleanField(
        default=False,
        help_text="置頂的公告會優先顯示",
        verbose_name="置頂"
    )
    show_on_homepage = models.BooleanField(
        default=False,
        help_text="是否在首頁顯示",
        verbose_name="首頁顯示"
    )
    publish_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="排程發布時間，留空則立即發布",
        verbose_name="發布時間"
    )
    expire_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="過期時間，過期後自動隱藏",
        verbose_name="過期時間"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='announcements',
        verbose_name="作者"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="瀏覽次數"
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        verbose_name="按讚數"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    
    class Meta:
        verbose_name = "最新消息"
        verbose_name_plural = "最新消息"
        ordering = ['-is_pinned', '-publish_date', '-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # 自動設定發布時間
        if self.status == 'published' and not self.publish_date:
            from django.utils import timezone
            self.publish_date = timezone.now()
            
        super().save(*args, **kwargs)
        
        # 壓縮特色圖片
        if self.featured_image:
            self.compress_image()
    
    def compress_image(self):
        """壓縮特色圖片"""
        try:
            img_path = self.featured_image.path
            img = Image.open(img_path)
            
            # 限制圖片最大尺寸
            max_size = (1200, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 優化品質
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            img.save(img_path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            print(f"圖片壓縮失敗: {e}")
    
    @property
    def is_published(self):
        """是否已發布"""
        return self.status == 'published'
    
    @property
    def is_expired(self):
        """是否已過期"""
        if not self.expire_date:
            return False
        from django.utils import timezone
        return timezone.now() > self.expire_date
    
    @property
    def can_display(self):
        """是否可以顯示"""
        from django.utils import timezone
        now = timezone.now()
        
        # 檢查發布狀態
        if self.status != 'published':
            return False
            
        # 檢查發布時間
        if self.publish_date and now < self.publish_date:
            return False
            
        # 檢查過期時間
        if self.expire_date and now > self.expire_date:
            return False
            
        return True
    
    def increment_views(self):
        """增加瀏覽次數"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

class AnnouncementImage(models.Model):
    """最新消息附加圖片"""
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="所屬公告"
    )
    image = models.ImageField(
        upload_to='announcements/images/%Y/%m/%d/',
        verbose_name="圖片"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="圖片說明"
    )
    order = models.IntegerField(
        default=0,
        help_text="顯示順序",
        verbose_name="排序"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上傳時間")
    
    class Meta:
        verbose_name = "公告圖片"
        verbose_name_plural = "公告圖片"
        ordering = ['order', 'created_at']
        
    def __str__(self):
        return f"{self.announcement.title} - 圖片 {self.order}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.compress_image()
    
    def compress_image(self):
        """壓縮圖片"""
        try:
            img_path = self.image.path
            img = Image.open(img_path)
            
            # 限制圖片最大尺寸
            max_size = (1000, 1000)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 優化品質
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            img.save(img_path, 'JPEG', quality=80, optimize=True)
        except Exception as e:
            print(f"圖片壓縮失敗: {e}")
