from optparse import make_option
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.urlresolvers import resolve, Resolver404

from usage.models import (
    PageHit,
    Period)


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

    option_list = BaseCommand.option_list + (
        make_option('--interval', '-i',
            action='store',
            nargs=1,
            dest='interval',
            default=5,
            help='[minutes] Summarize data in intervals of this much time'),
    )


    def handle(self, *args, **options):
        """
        Run the Command
        """
        interval = options['interval']

        try:
            last_period = Period.objects.latest('end')
        except Period.DoesNotExist:
            # If there are no periods, see when our earliest
            # page hit is and start prior to that.
            time = _round_to_interval(PageHit.objects.earliest('requested_time').requested_time, interval)
            print time



