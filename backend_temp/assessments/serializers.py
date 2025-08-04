from rest_framework import serializers
from .models import Test, Question, Choice, Response, ResponseItem

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text', 'score')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'order', 'text', 'choices')

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('code', 'name', 'description')

class ResponseItemCreateSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

    class Meta:
        model = ResponseItem
        fields = ('question', 'choice')

class ResponseCreateSerializer(serializers.ModelSerializer):
    items = ResponseItemCreateSerializer(many=True)

    class Meta:
        model = Response
        fields = ('items',)

    def create(self, validated_data):
        # 匿名可填，但登入後 user 不為 None
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        test = self.context['test']
        response = Response.objects.create(test=test, user=user)
        items_data = validated_data.pop('items')
        objs = [
            ResponseItem(response=response,
                         question=item['question'],
                         choice=item['choice'])
            for item in items_data
        ]
        ResponseItem.objects.bulk_create(objs)
        # 呼叫 save() 計算 total_score、risk_level
        response.save()
        return response

class ResponseSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Response
        fields = ('id', 'test', 'created_at', 'total_score', 'risk_level', 'items')

    def get_items(self, obj):
        return [
            {'question': item.question.id, 'choice': item.choice.id, 'score': item.choice.score}
            for item in obj.items.all()
        ]
