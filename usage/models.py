# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


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


class Period(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()


class UsageSummary(models.Model):
    user = models.ForeignKey(User)
    time = models.IntegerField(null=False, default=0)
    namespace = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    time_period = models.ForeignKey(Period)

