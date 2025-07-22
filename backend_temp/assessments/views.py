from rest_framework import generics, permissions
from rest_framework.response import Response as R
from .models import Test, Question, Response
from .serializers import (
    TestSerializer, QuestionSerializer,
    ResponseCreateSerializer, ResponseSerializer
)

class TestListView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny]

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Question.objects.filter(test__code=self.kwargs['code']).order_by('order')

class ResponseCreateView(generics.CreateAPIView):
    serializer_class = ResponseCreateSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['test'] = Test.objects.get(code=self.kwargs['code'])
        return ctx

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        data = ResponseSerializer(response).data
        return R(data)

class ResponseListView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Response.objects.filter(user=self.request.user).order_by('-created_at')
