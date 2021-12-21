from django.contrib import admin
from django.urls import path
from apiapp.views import (view_survey, create_survey, update_survey, delete_survey, create_question,
                          view_survey_solution, update_question, delete_question, create_answer, view_accessible_survey,
                          view_answer)

urlpatterns = [
    path('create-survey/', create_survey),
    path('update-survey/', update_survey),
    path('delete-survey/', delete_survey),
    path('create-question/', create_question),
    path('update-question/', update_question),
    path('delete-question/', delete_question),
    path('create-answer/', create_answer),
    path('view-accessible-surveys/', view_accessible_survey),
    path('view-answers/', view_answer),
    path('view-surveys/', view_survey),
    path('view-survey-solution/', view_survey_solution),
]
