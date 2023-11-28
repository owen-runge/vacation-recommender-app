from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SurveyData
from .serializers import SurveyDataSerializer
from .scripts.test import main

# Create your views here.
@api_view(['POST'])
def processData(request):
    survey_response = request.data
    return Response(main(survey_response))