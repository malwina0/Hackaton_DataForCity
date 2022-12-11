from django.db import models


# Create your models here.
class Event(models.Model):
    image = models.JSONField(blank=True, null=True)
    url = models.TextField(max_length=500, blank=True, null=True)
    map = models.JSONField(blank=True, null=True)
    category = models.JSONField(blank=True, null=True)
    occurrence = models.JSONField(blank=True, null=True)
    lead = models.TextField(max_length=500, blank=True, null=True)
    title = models.TextField(max_length=500, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    language = models.TextField(max_length=200, blank=True, null=True)
    text = models.TextField(max_length=500, blank=True, null=True)
    availableLanguages = models.JSONField(blank=True, null=True)
    localization = models.JSONField(blank=True, null=True)