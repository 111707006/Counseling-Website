from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

class Article(models.Model):
    """
    心理健康文章模型
    """
    title = models.CharField(
        max_length=200,
        help_text="文章標題，長度上限200字"
    )
    excerpt = models.CharField(
        max_length=300,
        blank=True,
        help_text="文章摘要，用於列表頁顯示，最多300字"
    )
    content = RichTextUploadingField(
        config_name='article',
        help_text="文章內文，支援富文本編輯和圖片上傳"
    )
    featured_image = models.ImageField(
        upload_to='articles/featured/',
        null=True,
        blank=True,
        help_text="特色圖片，顯示在文章列表和詳細頁面頂部"
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="標籤列表，JSON 陣列格式，例如 ['焦慮','人際關係']（選填）"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="文章作者，關聯 User 模型；若作者被刪除則保留文章"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="是否發布，未發布的文章不會在前端顯示"
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        help_text="發佈時間，建立時自動填入"
    )

    class Meta:
        ordering = ['-published_at']
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def __str__(self):
        return f"{self.title} (by {self.author})"

    @property
    def featured_image_url(self):
        """返回特色圖片的完整URL"""
        if self.featured_image:
            return self.featured_image.url
        return None


class ArticleImage(models.Model):
    """
    文章圖片模型 - 支持多張圖片附件
    """
    article = models.ForeignKey(
        Article,
        related_name='images',
        on_delete=models.CASCADE,
        help_text="所屬文章"
    )
    image = models.ImageField(
        upload_to='articles/images/',
        help_text="圖片檔案"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="圖片說明文字"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="排序順序，數字越小越靠前"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="上傳時間"
    )

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "文章圖片"
        verbose_name_plural = "文章圖片"

    def __str__(self):
        return f"{self.article.title} - 圖片 {self.order}"

    @property
    def image_url(self):
        """返回圖片的完整URL"""
        if self.image:
            return self.image.url
        return None
