from django.db import migrations

def load_bsrs5(apps, schema_editor):
    Test = apps.get_model('assessments', 'Test')
    Question = apps.get_model('assessments', 'Question')
    Choice = apps.get_model('assessments', 'Choice')

    bsrs5 = Test.objects.create(
        code='BSRS5',
        name='BSRS-5 Brief Symptom Rating Scale',
        description='過去一週情緒與心理困擾篩檢'
    )
    texts = [
        '我感到緊張不安',
        '我感到精神不濟或無法集中精神',
        '我易怒或煩躁',
        '我感到憂鬱情緒',
        '我有自殺或自我傷害的想法',
    ]
    labels = [
        '一定沒有', '很少', '有時', '經常', '幾乎一直'
    ]
    # 建立題目與選項（score 0–4）
    for idx, text in enumerate(texts, start=1):
        q = Question.objects.create(test=bsrs5, order=idx, text=text)
        for score, label in enumerate(labels):
            Choice.objects.create(question=q, text=label, score=score)

def unload_bsrs5(apps, schema_editor):
    Test = apps.get_model('assessments', 'Test')
    Test.objects.filter(code='BSRS5').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0002_load_who5'),
    ]

    operations = [
        migrations.RunPython(load_bsrs5, unload_bsrs5),
    ]
