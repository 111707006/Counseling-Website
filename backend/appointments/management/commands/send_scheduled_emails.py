"""
Django management command to send scheduled emails
Usage: python manage.py send_scheduled_emails
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from appointments.models import ScheduledEmail
import logging

# 設定日誌記錄
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send all scheduled emails that are ready to be sent'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run in dry-run mode (show what would be sent without actually sending)',
        )
        parser.add_argument(
            '--max-emails',
            type=int,
            default=50,
            help='Maximum number of emails to process in one run (default: 50)',
        )
        parser.add_argument(
            '--max-retries',
            type=int,
            default=3,
            help='Maximum number of retry attempts for failed emails (default: 3)',
        )
    
    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.max_emails = options['max_emails']
        self.max_retries = options['max_retries']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'開始發送排程郵件 (dry-run: {self.dry_run}, max-emails: {self.max_emails})'
            )
        )
        
        # 獲取準備發送的郵件
        ready_emails = ScheduledEmail.objects.filter(
            status='pending',
            scheduled_time__lte=timezone.now()
        ).order_by('scheduled_time')[:self.max_emails]
        
        if not ready_emails:
            self.stdout.write(self.style.WARNING('沒有需要發送的排程郵件'))
            return
        
        self.stdout.write(f'找到 {ready_emails.count()} 封待發送郵件')
        
        success_count = 0
        failed_count = 0
        
        for email in ready_emails:
            try:
                if self.dry_run:
                    self.stdout.write(
                        f'[DRY RUN] 會發送 {email.get_email_type_display()} 到 {email.recipient_email}'
                    )
                    success_count += 1
                else:
                    if self.send_email(email):
                        success_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ 成功發送 {email.get_email_type_display()} 到 {email.recipient_email}'
                            )
                        )
                    else:
                        failed_count += 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'✗ 發送失敗 {email.get_email_type_display()} 到 {email.recipient_email}'
                            )
                        )
            
            except Exception as e:
                failed_count += 1
                logger.error(f'處理郵件時發生錯誤 (ID: {email.id}): {str(e)}')
                self.stdout.write(
                    self.style.ERROR(f'✗ 處理錯誤: {str(e)}')
                )
                
                if not self.dry_run:
                    email.mark_as_failed(f'處理錯誤: {str(e)}')
        
        # 輸出總結
        if self.dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n[DRY RUN 完成] 預計會發送 {success_count} 封郵件'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n發送完成: ✓ {success_count} 成功, ✗ {failed_count} 失敗'
                )
            )
    
    def send_email(self, scheduled_email):
        """發送單封排程郵件"""
        try:
            # 檢查重試次數限制
            if scheduled_email.retry_count >= self.max_retries:
                self.stdout.write(
                    self.style.WARNING(
                        f'郵件 {scheduled_email.id} 已達最大重試次數 ({self.max_retries}), 跳過'
                    )
                )
                scheduled_email.status = 'failed'
                scheduled_email.error_message = '已達最大重試次數'
                scheduled_email.save()
                return False
            
            # 準備郵件內容
            template_name = self.get_template_name(scheduled_email.email_type)
            subject = self.get_email_subject(scheduled_email.email_type)
            
            # 準備模板上下文
            context = {
                'appointment': scheduled_email.appointment,
                'scheduled_email': scheduled_email,
            }
            
            # 渲染HTML模板
            html_content = render_to_string(template_name, context)
            text_content = strip_tags(html_content)
            
            # 創建郵件物件
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                to=[scheduled_email.recipient_email]
            )
            
            # 添加HTML版本
            email.attach_alternative(html_content, "text/html")
            
            # 發送郵件
            email.send(fail_silently=False)
            
            # 標記為已發送
            scheduled_email.mark_as_sent()
            
            return True
            
        except Exception as e:
            error_message = f'發送錯誤: {str(e)}'
            logger.error(f'發送郵件失敗 (ID: {scheduled_email.id}): {error_message}')
            scheduled_email.mark_as_failed(error_message)
            return False
    
    def get_template_name(self, email_type):
        """根據郵件類型獲取模板名稱"""
        template_mapping = {
            'reminder_24h_user': 'emails/appointment_reminder_24h.html',
            'reminder_24h_therapist': 'emails/appointment_reminder_24h_therapist.html',
        }
        
        return template_mapping.get(email_type, 'emails/base_email.html')
    
    def get_email_subject(self, email_type):
        """根據郵件類型獲取郵件主旨"""
        subject_mapping = {
            'reminder_24h_user': '預約提醒 - 明天的諮商時間',
            'reminder_24h_therapist': '預約提醒 - 明天的諮商預約',
        }
        
        return subject_mapping.get(email_type, '預約通知')