from django.db import models

class Subscriptions(models.Model):
    subscription_name = models.CharField(max_length=50)
    subscription_description = models.CharField(max_length=200)
    subscription_price = models.IntegerField()
    subscription_start_date = models.DateField()
    subscription_end_date = models.DateField()