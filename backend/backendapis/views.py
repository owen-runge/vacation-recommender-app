from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SurveyData
from .serializers import SurveyDataSerializer
from .scripts.test import main
from .scripts.reinforcementLearning import main as main_rfl

# Create your views here.
@api_view(['POST'])
def processData(request):
    print(f'request: {request}')
    print(f'request.data: {request.data}')

    if request.data[0] == 'feedback_survey_res':
        user_feedback_ranking = request.data[1]
        user_feedback_values = request.data[2]
        main_rfl(user_feedback_ranking, user_feedback_values)
        return Response('success!')
    if request.data[0] == 'main_survey_res':
        survey_response = request.data[1]
        return Response(main(survey_response))