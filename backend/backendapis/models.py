from django.db import models

# Create your models here.
class SurveyData(models.Model):
    choices = models.CharField(max_length=1200)