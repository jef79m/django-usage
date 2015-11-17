from datetime import datetime

from .models import UsageSummary, Period
from django.contrib.auth.models import User
from django.db.models import Count
from django.template.response import TemplateResponse
from django.conf import settings


def usage_display(request):
    template_name = 'usage/usage.html'
    context = {
        'title': "User Usage Report"
    }
    usage_data = []

    # Get date from request, otherwise assume Today.
    date = request.GET.get('date', None)
    if date:
        date = datetime.strptime(date, '%Y%m%d').date()
    else:
        date = datetime.now().date()

    # Users who have records for the given date,
    # annotated with number of time periods they were
    # active in.
    users = (User.objects
             .filter(usagesummary__time_period__start__contains=date)
             .values('pk')
             .annotate(total=Count('usagesummary__time_period', distinct=True))
             )

    # for each user, build a record with thier entries
    # as well as converting active periods to minutes
    # period length can be set in settings.USAGE_INTERVAL
    for user in users:
        summaries = (UsageSummary.objects
                     .filter(
                        user_id=user['pk'], time_period__start__contains=date))
        # Sparkline data is initialised with zero values
        # I'm making the assumption that ther will be more
        # periods with 0 activity than actual activity
        spark_data = [0] * (60 * 24 / settings.USAGE_INTERVAL)
        periods = summaries.values('time_period').annotate(hit_total=Count('hits')).values_list('time_period','hit_total')
        for period_id, hits in periods:
            spark_data[Period.objects.get(pk=period_id).index] = hits
        spark_data = ','.join([str(x) for x in spark_data])
        print spark_data
        usage_data.append({
            'user': User.objects.get(pk=user['pk']),
            'time_active': user['total'] * settings.USAGE_INTERVAL,
            'spark_data': spark_data,
            'summaries': summaries,
        })

    if users.exists():
        earliest = (UsageSummary.objects
                    .filter(time_period__start__contains=date)
                    .earliest('time_period__start').time_period.start)
        latest = (UsageSummary.objects
                  .filter(time_period__start__contains=date)
                  .latest('time_period__start').time_period.start)
    else:
        earliest = date
        latest = date
    try:
        previous_day = (UsageSummary.objects
                        .filter(time_period__start__lt=earliest)
                        .latest('time_period__start').time_period.start.date()
                        )
    except UsageSummary.DoesNotExist:
        previous_day = None

    try:
        next_day = (UsageSummary.objects
                    .filter(time_period__start__gt=latest)
                    .earliest('time_period__start').time_period.start.date()
                    )
    except UsageSummary.DoesNotExist:
        next_day = None

    context.update({
        'usage_data': usage_data,
        'previous_day': previous_day,
        'next_day': next_day})
    return TemplateResponse(request, template_name, context)
