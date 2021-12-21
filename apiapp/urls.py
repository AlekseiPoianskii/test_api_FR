from django.contrib import admin
from django.urls import path
from apiapp.views import (create_survey, update_survey, delete_survey, create_question,
                          update_question, delete_question, create_answer, view_survey, view_answer)

urlpatterns = [
    path('create-survey/', create_survey),
    path('update-survey/', update_survey),
    path('delete-survey/', delete_survey),
    path('create-question/', create_question),
    path('update-question/', update_question),
    path('delete-question/', delete_question),
    path('create-answer/', create_answer),
    path('view-surveys/', view_survey),
    path('view-answers/', view_answer),
]
