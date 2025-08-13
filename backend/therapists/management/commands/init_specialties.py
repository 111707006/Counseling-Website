from django.core.management.base import BaseCommand
from therapists.models import Specialty


class Command(BaseCommand):
    help = '初始化專業領域資料'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清除所有現有專業領域',
        )

    def handle(self, *args, **options):
        # 新的專業領域列表
        new_specialties = [
            {'name': '自我探索', 'description': '協助個案深入了解自己的內在世界、價值觀和人生方向'},
            {'name': '壓力調適', 'description': '學習有效的壓力管理技巧和調節方法'},
            {'name': '人際關係', 'description': '改善社交技巧，建立健康的人際互動模式'},
            {'name': '親密關係', 'description': '處理伴侶關係、溝通問題和情感連結'},
            {'name': '生涯諮商', 'description': '職涯規劃、工作選擇和職業發展諮詢'},
            {'name': '情緒調節', 'description': '學習認識和管理情緒的技巧'},
            {'name': '親子溝通', 'description': '改善親子關係和溝通品質'},
            {'name': '家庭關係', 'description': '處理家庭衝突，促進家庭和諧'},
            {'name': '創傷與失落', 'description': '陪伴處理創傷經驗和失落哀傷'},
            {'name': '憂鬱與焦慮適應', 'description': '協助面對憂鬱、焦慮等情緒困擾'},
        ]

        # 如果指定了 --clear 參數，清除現有的專業領域
        if options['clear']:
            current_count = Specialty.objects.count()
            Specialty.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'已清除 {current_count} 個現有專業領域'))

        # 創建新的專業領域
        created_count = 0
        for specialty_data in new_specialties:
            specialty, created = Specialty.objects.get_or_create(
                name=specialty_data['name'],
                defaults={
                    'description': specialty_data['description'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'已創建專業領域: {specialty.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'專業領域已存在: {specialty.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n初始化完成！共創建了 {created_count} 個專業領域')
        )
        self.stdout.write(
            self.style.SUCCESS(f'目前系統中共有 {Specialty.objects.count()} 個專業領域')
        )