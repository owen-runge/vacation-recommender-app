from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SurveyData
from .serializers import SurveyDataSerializer
import subprocess
from .scripts.test import model_output

# Create your views here.
@api_view(['POST'])
def processData(request):
    survey_response = request.data
    #process = subprocess.run(['python', 'scripts/test.py', 'survey_response'], capture_output=True, text=True)
    #return Response(process.stdout)
    return Response(model_output(survey_response))