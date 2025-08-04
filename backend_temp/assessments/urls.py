from django.urls import path
from .views import (
    TestListView, QuestionListView,
    ResponseCreateView, ResponseListView
)

app_name = 'assessments'

urlpatterns = [
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<str:code>/questions/', QuestionListView.as_view(), name='question-list'),
    path('tests/<str:code>/responses/', ResponseCreateView.as_view(), name='response-create'),
    path('results/', ResponseListView.as_view(), name='response-list'),
]
