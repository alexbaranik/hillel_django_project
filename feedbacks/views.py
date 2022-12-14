from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback


@login_required
def feedbacks(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        form = FeedbackModelForm(
            user=user,
            data=request.POST
        )
        if form.is_valid():
            form.save()
    else:
        form = FeedbackModelForm(
            user=user
        )
    context = {
        # 'feedbacks': Feedback.objects.all(),
        'feedbacks': Feedback.get_feedbacks(),
        'form': form
    }
    return render(request, 'feedbacks/index.html', context)
