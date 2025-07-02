from django.db import models
from django.conf import settings

class PaymentRecord(models.Model):
    """
    紀錄每筆 ECPay 金流交易資料
    """
    STATUS_CHOICES = [
        ('unpaid', '待付款'),
        ('paid', '已付款'),
        ('failed', '付款失敗'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text='對應的使用者'
    )
    merchant_trade_no = models.CharField(
        max_length=30,
        unique=True,
        help_text='綠界平台訂單編號（MerchantTradeNo）'
    )
    trade_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='綠界平台交易編號（TradeNo），付款成功後回傳'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        help_text='訂單金額（整數，單位新台幣）'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unpaid',
        help_text='本地訂單狀態'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='建立時間'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='付款完成時間'
    )
    raw_data = models.JSONField(
        null=True,
        blank=True,
        help_text='綠界回傳的原始資料 JSON，便於日後查核'
    )

    def __str__(self):
        return f"PaymentRecord {self.merchant_trade_no} ({self.user.username})"
