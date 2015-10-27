from datetime import (timedelta,
                      datetime)

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import resolve, Resolver404

from usage.models import (
    PageHit,
    Period,
    UsageSummary)


def _round_to_interval(time, interval):
    """
    Description:
        Rounds a time to the previous <interval> number
        of minutes.
        eg. input: 10:43:21:12 -> 10:40:00:00
    Args:
        time (DateTime): The time to perform rounding on
        interval (int): The rounding period in minutes.
    """
    delta = timedelta(minutes=time.minute % interval,
                      seconds=time.second,
                      microseconds=time.microsecond)
    return time - delta


class Command(BaseCommand):
    """
    Summarizes individual page hits and calculates time
    spent on site.
    """

    help = "Summarize user usage details"

    def handle(self, *args, **options):
        """
        Run the Command
        """
        # Interval in minutes to break up hits.
        # TODO: make this configurable.
        interval = settings.USAGE_INTERVAL
        delta = timedelta(minutes=interval)
        run_time = datetime.now()

        pagehits = PageHit.objects.not_summarized().order_by('requested_time')
        if pagehits.exists():
            start = _round_to_interval(
                pagehits.earliest('requested_time').requested_time, interval)
            period, created = Period.objects.get_or_create(start=start, end=start + delta)
            for hit in pagehits:
                if not (hit.requested_time >= start and
                        hit.requested_time < start + delta):
                    start = _round_to_interval(hit.requested_time, interval)
                    period, created = Period.objects.get_or_create(
                        start=start, end=start + delta)
                try:
                    namespace = resolve(hit.requested_page).namespace
                    url_name = resolve(hit.requested_page).url_name
                except Resolver404:
                    namespace = url_name = "Unknown"
                summary, created = UsageSummary.objects.get_or_create(
                            time_period=period,
                            namespace=namespace,
                            url_name=url_name,
                            user=hit.user)
                hit.summarized = run_time
                hit.save()
                summary.hits += 1
                summary.save()
        print "Processed %s hits" % pagehits.count()
