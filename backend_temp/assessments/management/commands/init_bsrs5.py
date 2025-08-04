from django.core.management.base import BaseCommand
from assessments.models import Test, Question, Choice


class Command(BaseCommand):
    help = '初始化 BSRS-5 簡式健康量表數據'

    def handle(self, *args, **options):
        # 創建或獲取 BSRS-5 測驗
        test, created = Test.objects.get_or_create(
            code='BSRS5',
            defaults={
                'name': '簡式健康量表（BSRS-5）',
                'description': '回想最近一週，受困擾或苦惱的程度評估量表'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'創建測驗：{test.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'測驗已存在：{test.name}'))
            # 清除舊數據重新創建
            test.questions.all().delete()
            self.stdout.write(self.style.WARNING('清除舊題目數據'))

        # BSRS-5 題目
        questions_data = [
            {
                "order": 1,
                "text": "最近一週以來，您是否有睡眠困難，例如難以入睡、易醒或早醒？"
            },
            {
                "order": 2,
                "text": "最近一週以來，您是否感覺緊張或不安？"
            },
            {
                "order": 3,
                "text": "最近一週以來，您是否覺得容易苦惱或動怒？"
            },
            {
                "order": 4,
                "text": "最近一週以來，您是否感覺憂鬱、心情低落？"
            },
            {
                "order": 5,
                "text": "最近一週以來，您是否覺得比不上別人？"
            },
            {
                "order": 6,
                "text": "最近一週以來，您是否有自殺的想法？"
            }
        ]

        # 選項標籤
        choice_labels = {
            0: "不會",
            1: "輕微", 
            2: "中等程度",
            3: "嚴重",
            4: "非常嚴重"
        }

        # 創建題目和選項
        for q_data in questions_data:
            question = Question.objects.create(
                test=test,
                text=q_data['text'],
                order=q_data['order']
            )
            
            # 為每個題目創建 5 個選項（0-4分）
            for score in range(5):
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
                f'BSRS-5 初始化完成！\n'
                f'測驗代碼：{test.code}\n'
                f'題目數量：{test.questions.count()}\n'
                f'總選項數：{sum(q.choices.count() for q in test.questions.all())}'
            )
        )
        
        # 顯示評分說明
        self.stdout.write(
            self.style.SUCCESS(
                '\n評分說明：\n'
                '0-5分：身心適應狀況良好\n'
                '6-9分：輕度情緒困擾：建議與親友談談，抒發情緒\n'
                '10-14分：中度情緒困擾：建議尋求心理諮商或專業協助\n'
                '15-20分：重度情緒困擾：需高度關懷，建議轉介精神科治療\n'
                '\n特別注意：若前5題總分 < 6 且第6題自殺想法評分 ≥ 2，建議轉介精神科'
            )
        )