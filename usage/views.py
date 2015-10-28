from django.contrib.auth.models import User
from django.db.models import Count
from django.template.response import TemplateResponse


def usage_display(request):
    template_name = 'usage/usage.html'
    context = {
        'title': "User Usage Report"
    }

    users = (
        User.objects.all()
        .annotate(active_periods=Count('usagesummary__time_period', distinct=True))
        .filter(active_periods__gt=0)
        )
    context.update({'users': users})
    return TemplateResponse(request, template_name, context)
