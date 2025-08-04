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
    content = RichTextUploadingField(
        config_name='article',
        help_text="文章內文，支援富文本編輯和圖片上傳"
    )
    tags = models.JSONField(
        default=list,
        help_text="標籤列表，JSON 陣列格式，例如 ['焦慮','人際關係']"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="文章作者，關聯 User 模型；若作者被刪除則保留文章"
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        help_text="發佈時間，建立時自動填入"
    )

    def __str__(self):
        # 管理後台顯示用
        return f"{self.title} (by {self.author})"
