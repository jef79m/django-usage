# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from appconf import AppConf


# Default settings using appconf (http://django-appconf.readthedocs.org/en/v1.0.1/usage/)
# Override in your settings.py by prefixing with USAGE_
# eg. USAGE_INTERVAL = 10
class UsageConf(AppConf):
    INTERVAL = 5  # summary interval in minutes


class PageHitQuerySet(models.QuerySet):
    def not_summarized(self):
        return self.filter(summarized__isnull=True)


class PageHit(models.Model):
    requested_page = models.CharField(max_length=255)
    requested_time = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    summarized = models.DateTimeField(null=True)

    objects = PageHitQuerySet.as_manager()

    def __unicode__(self):
        return u"%s: %s, %s" % (self.user.username,
                                self.requested_page,
                                self.requested_time)


class Period(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return u"%s -> %s" % (self.start, self.end)


class UsageSummary(models.Model):
    user = models.ForeignKey(User)
    hits = models.IntegerField(null=False, default=0)
    namespace = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    time_period = models.ForeignKey(Period)

    def __unicode__(self):
        return u"(%s-%s) %s - %s: %s hits" % (
            self.time_period.start, self.time_period.end,
            self.namespace, self.url_name, self.hits)
