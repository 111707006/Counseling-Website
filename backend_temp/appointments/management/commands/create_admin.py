from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = '創建管理員用戶'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='管理員Email', default='admin@mindcare.com')
        parser.add_argument('--password', type=str, help='管理員密碼', default='admin123456')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        try:
            with transaction.atomic():
                # 檢查是否已存在
                if User.objects.filter(email=email).exists():
                    self.stdout.write(
                        self.style.WARNING(f'管理員 {email} 已存在')
                    )
                    return

                # 創建管理員用戶
                admin_user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_staff=True,
                    is_superuser=True
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'成功創建管理員:\n'
                        f'Email: {email}\n'
                        f'密碼: {password}\n'
                        f'請登入 /admin/ 管理後台'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'創建管理員失敗: {e}')
            )