from django.db import models


class InputSite(models.Model):
    url = models.URLField(max_length=300)
    query = models.TextField(max_length=100, blank=True, null=True)
    search = models.TextField(max_length=100, blank=True, null=True)
    user_agent = models.TextField(max_length=300)
    context = models.TextField(max_length=100, blank=True, null=True)


class CheckedSite(models.Model):
    url = models.URLField(max_length=300)
    context = models.JSONField()
    ads = models.JSONField()
    name = models.TextField(max_length=100)
    user_agent = models.TextField(max_length=300)
    screenshot_ads = models.TextField(max_length=300)
