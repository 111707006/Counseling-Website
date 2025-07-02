from django.urls import path
from .views import CheckoutView, ECPayNotifyCallback, ECPayReturnCallback

app_name = 'payments'

urlpatterns = [
    # 建立結帳並產生綠界參數
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # 綠界背景通知 (NotifyURL)
    path('callback/notify/', ECPayNotifyCallback.as_view(), name='ecpay_notify'),
    # 使用者付款完成導回 (ReturnURL)
    path('callback/return/', ECPayReturnCallback.as_view(), name='ecpay_return'),
]
