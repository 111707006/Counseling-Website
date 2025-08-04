# 導入Django郵件發送功能
from django.core.mail import send_mail
# 導入Django設定檔，用於讀取郵件配置
from django.conf import settings
# 導入模板渲染器（未來可用於HTML郵件模板）
from django.template.loader import render_to_string
# 導入HTML標籤去除功能（用於從HTML模板生成純文字版本）
from django.utils.html import strip_tags
# 導入預約模型
from .models import Appointment

def send_appointment_created_notification(appointment: Appointment):
    """
    預約建立時發送通知給管理員或指定心理師
    參數: appointment - 新建立的預約物件
    回傳: True/False - 發送是否成功
    """
    # 設定郵件主旨，包含申請人Email以便識別
    subject = f'新預約申請 - {appointment.user.email}'
    
    # 決定郵件收件人：優先發送給指定心理師，否則發送給管理員
    if appointment.therapist and appointment.therapist.user and appointment.therapist.user.email:
        # 如果預約有指定心理師且該心理師有綁定用戶帳號和Email
        recipient_list = [appointment.therapist.user.email]  # 收件人列表
        recipient_name = appointment.therapist.name          # 收件人姓名（用於郵件內容）
    else:
        # 如果沒有指定心理師，則發送給系統管理員
        # 使用getattr安全地從settings取得ADMIN_EMAIL，如果沒設定則使用預設值
        recipient_list = [getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')]
        recipient_name = "管理員"  # 管理員的顯示名稱
    
    # 準備偏好時間資料，將資料庫中的時段轉換為易讀格式
    preferred_periods = []  # 儲存處理後的偏好時間列表
    # 遍歷該預約的所有偏好時段
    for period in appointment.preferred_periods.all():
        # 將時段代碼轉換為中文顯示文字
        period_display = {
            'morning': '上午 (09:00-12:00)',     # 上午時段
            'afternoon': '下午 (13:00-17:00)',   # 下午時段
            'evening': '晚上 (18:00-21:00)'      # 晚上時段
        }.get(period.period, period.period)     # 如果找不到對應則使用原始值
        
        # 將處理後的時段資料加入列表
        preferred_periods.append({
            'date': period.date.strftime('%Y-%m-%d'),  # 將日期格式化為字串
            'period': period_display                    # 時段的中文顯示
        })
    
    # 準備郵件模板的上下文變數（目前未使用模板，但保留擴展性）
    context = {
        'appointment': appointment,                    # 預約物件
        'recipient_name': recipient_name,              # 收件人姓名
        'preferred_periods': preferred_periods,        # 偏好時間列表
        # 檢查預約是否有詳細資訊，有則包含，無則為None
        'user_detail': appointment.detail if hasattr(appointment, 'detail') else None,
        # 將諮商類型代碼轉換為中文顯示
        'consultation_type_display': '線上諮商' if appointment.consultation_type == 'online' else '實體諮商'
    }
    
    # 建立郵件內容（純文字格式）
    message = f"""
親愛的 {recipient_name}，

有新的預約申請需要您的處理：

預約編號：{appointment.id}
申請人：{appointment.user.email}
心理師：{appointment.therapist.name if appointment.therapist else '待指定'}
諮商方式：{context['consultation_type_display']}

偏好時間：
{chr(10).join([f"- {p['date']} {p['period']}" for p in preferred_periods])}

請登入後台處理此預約申請。

系統自動發送
    """
    
    # 嘗試發送郵件
    try:
        send_mail(
            subject=subject,      # 郵件主旨
            message=message,      # 郵件內容
            # 從settings安全地取得發件人Email，沒設定則使用預設值
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
            recipient_list=recipient_list,  # 收件人列表
            fail_silently=False,           # 發送失敗時拋出異常而不是靜默失敗
        )
        # 發送成功，印出日誌
        print(f"預約通知郵件已發送給: {', '.join(recipient_list)}")
        return True  # 回傳成功
    except Exception as e:
        # 發送失敗，印出錯誤訊息
        print(f"郵件發送失敗: {e}")
        return False  # 回傳失敗

def send_appointment_confirmed_notification(appointment: Appointment, confirmed_datetime):
    """
    預約確認時發送通知給來談者
    參數: appointment - 預約物件
    參數: confirmed_datetime - 管理員確認的具體時間
    回傳: True/False - 發送是否成功
    """
    # 設定確認通知的郵件主旨，包含預約編號以便識別
    subject = f'預約確認通知 - 預約編號 {appointment.id}'
    
    # 建立確認通知的郵件內容
    message = f"""
親愛的用戶，

您的預約已確認！

預約編號：{appointment.id}
心理師：{appointment.therapist.name if appointment.therapist else '待安排'}
確認時間：{confirmed_datetime.strftime('%Y-%m-%d %H:%M')}
諮商方式：{'線上諮商' if appointment.consultation_type == 'online' else '實體諮商'}

請準時參加諮商，如有任何問題請聯繫我們。

祝您身心健康
    """
    
    # 嘗試發送確認通知給來談者
    try:
        send_mail(
            subject=subject,                    # 郵件主旨
            message=message,                    # 郵件內容
            # 從settings取得發件人Email
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
            recipient_list=[appointment.user.email],  # 收件人：預約申請人
            fail_silently=False,                     # 發送失敗時拋出異常
        )
        # 發送成功日誌
        print(f"預約確認通知已發送給: {appointment.user.email}")
        return True  # 回傳成功
    except Exception as e:
        # 發送失敗日誌
        print(f"確認通知發送失敗: {e}")
        return False  # 回傳失敗

# 以下為向後兼容的函數，保留舊的函數名稱以免破壞現有代碼

def send_mail_to_admin(appt):
    """
    向管理員發送新預約通知（舊函數名稱的兼容版本）
    參數: appt - 預約物件
    回傳: 調用新函數的結果
    """
    return send_appointment_created_notification(appt)

def send_mail_to_client(appt):
    """
    向客戶發送預約更新通知（舊函數名稱的兼容版本）
    參數: appt - 預約物件
    回傳: True/False - 發送是否成功
    """
    # 檢查預約是否有指定的時段和時間
    if appt.slot and appt.slot.slot_time:
        # 如果有，則發送確認通知
        return send_appointment_confirmed_notification(appt, appt.slot.slot_time)
    return False  # 沒有時段資訊則無法發送

def send_appointment_rejected_notification(appointment: Appointment, rejection_reason=""):
    """
    預約被拒絕時發送通知給來談者
    參數: appointment - 預約物件
    參數: rejection_reason - 拒絕原因（可選）
    回傳: True/False - 發送是否成功
    """
    # 設定拒絕通知的郵件主旨
    subject = f'預約申請結果通知 - 預約編號 {appointment.id}'
    
    # 建立拒絕通知的郵件內容
    message = f"""
親愛的用戶，

很抱歉，您的預約申請未能安排成功。

預約編號：{appointment.id}
申請心理師：{appointment.therapist.name if appointment.therapist else '未指定'}
申請時間：{appointment.created_at.strftime('%Y-%m-%d %H:%M')}
諮商方式：{'線上諮商' if appointment.consultation_type == 'online' else '實體諮商'}

{f'拒絕原因：{rejection_reason}' if rejection_reason else ''}

如有任何疑問，歡迎與我們聯繫。我們會盡力為您安排其他合適的時間。

感謝您的理解
    """
    
    # 嘗試發送拒絕通知給來談者
    try:
        send_mail(
            subject=subject,                          # 郵件主旨
            message=message,                          # 郵件內容
            # 從settings取得發件人Email
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
            recipient_list=[appointment.user.email],  # 收件人：預約申請人
            fail_silently=False,                     # 發送失敗時拋出異常
        )
        # 發送成功日誌
        print(f"預約拒絕通知已發送給: {appointment.user.email}")
        return True  # 回傳成功
    except Exception as e:
        # 發送失敗日誌
        print(f"拒絕通知發送失敗: {e}")
        return False  # 回傳失敗

def send_appointment_cancelled_notification(appointment: Appointment):
    """
    預約被取消時發送通知給管理員或心理師
    參數: appointment - 預約物件
    回傳: True/False - 發送是否成功
    """
    # 設定取消通知的郵件主旨
    subject = f'預約取消通知 - 預約編號 {appointment.id}'
    
    # 決定郵件收件人：優先通知指定心理師，否則通知管理員
    if appointment.therapist and appointment.therapist.user and appointment.therapist.user.email:
        # 如果有指定心理師且該心理師有綁定用戶帳號和Email
        recipient_list = [appointment.therapist.user.email]  # 收件人列表
        recipient_name = appointment.therapist.name          # 收件人姓名
    else:
        # 如果沒有指定心理師，則通知系統管理員
        recipient_list = [getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')]
        recipient_name = "管理員"  # 管理員的顯示名稱
    
    # 建立取消通知的郵件內容
    message = f"""
親愛的 {recipient_name}，

有一筆預約已被來談者取消：

預約編號：{appointment.id}
來談者：{appointment.user.email}
心理師：{appointment.therapist.name if appointment.therapist else '待指定'}
原定諮商方式：{'線上諮商' if appointment.consultation_type == 'online' else '實體諮商'}
取消時間：{appointment.updated_at.strftime('%Y-%m-%d %H:%M') if hasattr(appointment, 'updated_at') else '剛剛'}

如果該時段已被確認，請記得釋放相關資源。

系統自動發送
    """
    
    # 嘗試發送取消通知
    try:
        send_mail(
            subject=subject,                    # 郵件主旨
            message=message,                    # 郵件內容
            # 從settings取得發件人Email
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
            recipient_list=recipient_list,      # 收件人列表
            fail_silently=False,               # 發送失敗時拋出異常
        )
        # 發送成功日誌
        print(f"預約取消通知已發送給: {', '.join(recipient_list)}")
        return True  # 回傳成功
    except Exception as e:
        # 發送失敗日誌
        print(f"取消通知發送失敗: {e}")
        return False  # 回傳失敗

def send_mail_final(appt):
    """
    最終確認通知（舊函數名稱的兼容版本）
    參數: appt - 預約物件
    回傳: 調用send_mail_to_client的結果
    """
    # 可以擴展為包含SMS或其他通知方式，目前只調用郵件通知
    return send_mail_to_client(appt)
