from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from appointments.models import Appointment
from therapists.models import TherapistProfile

User = get_user_model()

class Command(BaseCommand):
    help = '檢查預約管理系統狀態'

    def handle(self, *args, **options):
        self.stdout.write("檢查預約管理系統狀態...")
        
        # 檢查預約數量
        total_appointments = Appointment.objects.count()
        pending_appointments = Appointment.objects.filter(status='pending').count()
        confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
        
        # 檢查心理師數量
        total_therapists = TherapistProfile.objects.count()
        
        # 檢查管理員數量
        admin_users = User.objects.filter(is_staff=True).count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n系統狀態報告:\n"
                f"總預約數: {total_appointments}\n"
                f"待確認預約: {pending_appointments}\n"
                f"已確認預約: {confirmed_appointments}\n"
                f"心理師數量: {total_therapists}\n"
                f"管理員數量: {admin_users}\n"
            )
        )
        
        if pending_appointments > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"警告: 有 {pending_appointments} 筆預約待處理"
                )
            )
        
        if admin_users == 0:
            self.stdout.write(
                self.style.ERROR(
                    "錯誤: 未找到管理員用戶，請執行: python manage.py create_admin"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "成功: 管理員設定完成，可以登入 http://localhost:8000/admin/"
                )
            )