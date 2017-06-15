from django.db import models

class upload(models.Model):
    username = models.CharField(max_length = 100)
    datetime = models.DateTimeField("Datetime", auto_now = True)
    action = models.CharField(max_length = 100)
