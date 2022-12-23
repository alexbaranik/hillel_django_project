import django_filters

from feedbacks.models import Feedback


class FeedbackFilter(django_filters.FilterSet):
    class Meta:
        model = Feedback
        fields = {
            'rating': ['exact', 'lt', 'gt'],
        }
