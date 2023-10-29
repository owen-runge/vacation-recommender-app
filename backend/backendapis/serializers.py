from rest_framework import serializers
from .models import SurveyData

class SurveyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyData
        fields = ('choices')