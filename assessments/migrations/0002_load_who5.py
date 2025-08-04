from django.db import migrations

def load_who5(apps, schema_editor):
    Test = apps.get_model('assessments', 'Test')
    Question = apps.get_model('assessments', 'Question')
    Choice = apps.get_model('assessments', 'Choice')

    who5 = Test.objects.create(
        code='WHO5',
        name='WHO-5 Well-Being Index',
        description='過去兩週主觀幸福感量表'
    )
    texts = [
        '我感到快樂、心情舒暢',
        '我感覺寧靜和放鬆',
        '我感覺充滿活力、精力充沛',
        '我睡醒時感到清新、得到了足夠休息',
        '我每天生活充滿了有趣的事情',
    ]
    labels = [
        '從未有過', '有時候', '少於一半時間',
        '超過一半時間', '大部分時間', '所有時間'
    ]
    # 建立題目與選項（score 0–5）
    for idx, text in enumerate(texts, start=1):
        q = Question.objects.create(test=who5, order=idx, text=text)
        for score, label in enumerate(labels):
            Choice.objects.create(question=q, text=label, score=score)

def unload_who5(apps, schema_editor):
    Test = apps.get_model('assessments', 'Test')
    Test.objects.filter(code='WHO5').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_who5, unload_who5),
    ]
