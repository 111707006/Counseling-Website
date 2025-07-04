from django.contrib import admin
from .models import Test, Question, Choice, Response, ResponseItem

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'order', 'text')
    list_filter = ('test',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'score')
    list_filter = ('question__test',)

class ResponseItemInline(admin.TabularInline):
    model = ResponseItem
    extra = 0
    readonly_fields = ('question', 'choice')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('test', 'user', 'total_score', 'risk_level', 'created_at')
    list_filter = ('test', 'risk_level')
    readonly_fields = ('test', 'user', 'total_score', 'risk_level', 'created_at')
    inlines = [ResponseItemInline]
