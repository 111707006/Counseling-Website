from django.core.management.base import BaseCommand
from assessments.models import Test, Question, Choice


class Command(BaseCommand):
    help = '初始化 WHO-5 幸福感量表數據'

    def handle(self, *args, **options):
        # 創建或獲取 WHO-5 測驗
        test, created = Test.objects.get_or_create(
            code='WHO5',
            defaults={
                'name': 'WHO-5 幸福感量表',
                'description': '請回想過去兩週的情況，評估您的整體幸福感和心理健康狀況'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'創建測驗：{test.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'測驗已存在：{test.name}'))
            # 清除舊數據重新創建
            test.questions.all().delete()
            self.stdout.write(self.style.WARNING('清除舊題目數據'))

        # WHO-5 題目（過去兩週）
        questions_data = [
            {
                "order": 1,
                "text": "在過去兩週內，您是否感到愉快且心情好？"
            },
            {
                "order": 2,
                "text": "在過去兩週內，您是否感到冷靜且放鬆？"
            },
            {
                "order": 3,
                "text": "在過去兩週內，您是否感到有活力且充滿活力？"
            },
            {
                "order": 4,
                "text": "在過去兩週內，您醒來時是否感到清新且休息充足？"
            },
            {
                "order": 5,
                "text": "在過去兩週內，您的日常生活是否充滿了讓您感興趣的事物？"
            }
        ]

        # 選項標籤（0-5分量表）
        choice_labels = {
            0: "完全沒有",
            1: "很少時候", 
            2: "不到一半的時間",
            3: "一半以上的時間",
            4: "大部分時間",
            5: "一直都是"
        }

        # 創建題目和選項
        for q_data in questions_data:
            question = Question.objects.create(
                test=test,
                text=q_data['text'],
                order=q_data['order']
            )
            
            # 為每個題目創建 6 個選項（0-5分）
            for score in range(6):
                Choice.objects.create(
                    question=question,
                    text=choice_labels[score],
                    score=score
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'創建題目 {q_data["order"]}: {q_data["text"][:30]}...')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'WHO-5 初始化完成！\n'
                f'測驗代碼：{test.code}\n'
                f'題目數量：{test.questions.count()}\n'
                f'總選項數：{sum(q.choices.count() for q in test.questions.all())}'
            )
        )
        
        # 顯示評分說明
        self.stdout.write(
            self.style.SUCCESS(
                '\n評分說明：\n'
                '原始分數範圍：0-25分\n'
                '轉換後分數：原始分 × 4 = 0-100分\n'
                '≥50分：良好的幸福感\n'
                '29-49分：中度關注\n'
                '<29分：需要關注（可能有憂鬱症狀）'
            )
        )