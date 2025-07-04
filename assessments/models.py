from decimal import Decimal
from django.db import models
from django.conf import settings

class Test(models.Model):
    """量表模型，用於定義 WHO-5 和 BSRS-5 等測驗"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    """量表題目模型"""
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['test', 'order']

    def __str__(self):
        return f"{self.test.code} Q{self.order}"

class Choice(models.Model):
    """題目選項模型"""
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.question} - {self.text}"

class Response(models.Model):
    """使用者作答紀錄模型"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(null=True, blank=True)
    risk_level = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 計算分數
        total = sum(item.choice.score for item in self.items.all())
        if self.test.code == 'WHO5':
            # WHO-5 raw sum * 4 → 0–100
            self.total_score = total * 4
            if self.total_score >= 50:
                self.risk_level = '良好'
            elif self.total_score >= 29:
                self.risk_level = '中度關注'
            else:
                self.risk_level = '需要關注'
        else:
            # BSRS-5 raw sum → 0–20
            self.total_score = total
            if total <= 5:
                self.risk_level = '正常'
            elif total <= 9:
                self.risk_level = '輕度'
            elif total <= 14:
                self.risk_level = '中度'
            else:
                self.risk_level = '重度'
        # 直接 update，避免再次觸發 save()
        Response.objects.filter(pk=self.pk).update(
            total_score=self.total_score,
            risk_level=self.risk_level
        )

    def __str__(self):
        return f"{self.user if self.user else '匿名'} - {self.test.code} @ {self.created_at}"

class ResponseItem(models.Model):
    """每題作答項目模型"""
    response = models.ForeignKey(Response, related_name='items', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
