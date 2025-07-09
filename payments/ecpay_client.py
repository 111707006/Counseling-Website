"""簡化版 ECPay 客戶端，僅回傳固定參數以便開發測試。"""

def generate_ecpay_payment_form(payment):
    # 真正整合 ECPay SDK 時，應依照官方文件產生表單參數
    return {
        "MerchantTradeNo": payment.merchant_trade_no,
        "TotalAmount": str(payment.total_amount),
        "TradeDesc": "MindCare payment",
    }
