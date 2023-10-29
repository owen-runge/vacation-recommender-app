#from django.conf.urls import url
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.processData),
]