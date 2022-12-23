from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.feedbacks.serializers import FeedbackSerializer
from api.feedbacks.filters import FeedbackFilter
from feedbacks.models import Feedback


class FeedbacksViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = FeedbackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user')
        return queryset
