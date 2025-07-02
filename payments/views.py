from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from .models import PaymentRecord
from .ecpay_client import generate_ecpay_payment_form

class CheckoutView(APIView):
    """
    POST /api/payments/checkout/
    建立本地 PaymentRecord 並回傳綠界付款參數給前端
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 從前端接收訂單金額（也可擴充接收商品明細、order_id 等）
        amount = request.data.get('total_amount')
        if not amount:
            return Response({"error": "total_amount 為必填"}, status=status.HTTP_400_BAD_REQUEST)

        # 建立 PaymentRecord，使用 uniq merchant_trade_no
        trade_no = f"{request.user.id}{int(timezone.now().timestamp())}"
        payment = PaymentRecord.objects.create(
            user=request.user,
            merchant_trade_no=trade_no,
            total_amount=amount
        )

        # 取得綠界表單參數
        try:
            ecpay_params = generate_ecpay_payment_form(payment)
        except Exception as e:
            return Response({"error": f"ECPay 參數產生失敗：{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 回傳給前端，由前端組表單自動 submit
        return Response({"ecpay_params": ecpay_params}, status=status.HTTP_201_CREATED)

class ECPayNotifyCallback(APIView):
    """
    POST /api/payments/callback/notify/
    綠界背景通知 (Server-to-Server)，必須回傳 '1|OK'
    """
    permission_classes = [AllowAny]  # 綠界不帶 JWT

    def post(self, request):
        # 取得綠界回傳所有欄位
        data = request.data.dict()
        merchant_trade_no = data.get('MerchantTradeNo')
        rtn_code = data.get('RtnCode')
        trade_no = data.get('TradeNo')

        # 找到對應的 PaymentRecord
        payment = get_object_or_404(PaymentRecord, merchant_trade_no=merchant_trade_no)

        # 驗證交易成功
        if rtn_code == '1':
            payment.status = 'paid'
            payment.trade_no = trade_no
            payment.paid_at = timezone.now()
        else:
            payment.status = 'failed'

        # 儲存原始回傳資料
        payment.raw_data = data
        payment.save()

        # 回傳綠界要求的固定格式
        return Response("1|OK", content_type="text/plain")

class ECPayReturnCallback(APIView):
    """
    GET /api/payments/callback/return/
    使用者付款完成後瀏覽器導回網址，可呈現前端畫面
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 可選擇讀取 query_params 顯示訂單狀態
        merchant_trade_no = request.query_params.get('MerchantTradeNo')
        payment = PaymentRecord.objects.filter(merchant_trade_no=merchant_trade_no).first()
        if payment and payment.status == 'paid':
            return Response({"msg": "付款成功", "order": merchant_trade_no})
        return Response({"msg": "付款處理中或失敗"}, status=status.HTTP_400_BAD_REQUEST)
