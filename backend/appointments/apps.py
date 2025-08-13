from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
    verbose_name = 'Appointments'
    
    def ready(self):
        # 確保 admin 被正確導入
        try:
            import appointments.admin
        except ImportError:
            pass