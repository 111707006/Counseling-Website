from django.core.management.base import BaseCommand
from assessments.models import Test, Question, Choice


class Command(BaseCommand):
    help = '重新初始化 BSRS-5 簡式健康量表資料'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清除現有 BSRS-5 資料',
        )

    def handle(self, *args, **options):
        # 如果指定了 --clear 參數，清除現有資料
        if options['clear']:
            try:
                test = Test.objects.get(code='BSRS5')
                test.delete()
                self.stdout.write(self.style.WARNING('已清除現有 BSRS-5 資料'))
            except Test.DoesNotExist:
                self.stdout.write(self.style.WARNING('未找到現有 BSRS-5 資料'))

        # 創建 BSRS-5 測驗
        test, created = Test.objects.get_or_create(
            code='BSRS5',
            defaults={
                'name': 'BSRS-5 簡式健康量表',
                'description': (
                    '簡式健康量表是讓您回想最近一星期（包含評估當天），'
                    '感到困擾或苦惱的程度。請根據您的真實感受作答。'
                )
            }
        )

        if not created:
            self.stdout.write(self.style.WARNING('BSRS-5 測驗已存在，跳過創建'))
            return

        self.stdout.write(self.style.SUCCESS(f'已創建測驗: {test.name}'))

        # 題目資料
        questions_data = [
            {
                'order': 1,
                'text': '睡眠困難，譬如難以入睡、易醒或早醒'
            },
            {
                'order': 2,
                'text': '感覺緊張或不安'
            },
            {
                'order': 3,
                'text': '覺得容易苦惱或動怒'
            },
            {
                'order': 4,
                'text': '感覺憂鬱、心情低落'
            },
            {
                'order': 5,
                'text': '覺得比不上別人'
            },
            {
                'order': 6,
                'text': '★有自殺的想法'
            }
        ]

        # 選項資料（每題都是相同的選項）
        choices_data = [
            {'text': '不會', 'score': 0},
            {'text': '輕微', 'score': 1},
            {'text': '中等程度', 'score': 2},
            {'text': '嚴重', 'score': 3},
            {'text': '非常嚴重', 'score': 4}
        ]

        # 創建題目和選項
        for q_data in questions_data:
            question = Question.objects.create(
                test=test,
                text=q_data['text'],
                order=q_data['order']
            )

            # 為每題創建選項
            for choice_data in choices_data:
                Choice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    score=choice_data['score']
                )

            self.stdout.write(
                self.style.SUCCESS(f'已創建題目 {q_data["order"]}: {q_data["text"]}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\nBSRS-5 初始化完成！')
        )
        self.stdout.write(
            self.style.SUCCESS(f'共創建了 {len(questions_data)} 道題目')
        )
        self.stdout.write(
            self.style.SUCCESS(f'每題有 {len(choices_data)} 個選項')
        )