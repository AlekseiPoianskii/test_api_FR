from django.shortcuts import render
from apiapp.serializers import SurveySerializer, QuestionSerializer, AnswerSerializer
from surveyapp.models import Survey, Question, AnswerUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.timezone import now


@api_view(['POST'])
def create_survey(request):
    survey = SurveySerializer()
    try:
        answer = survey.create(validated_data=request.data)
    except Exception:
        answer = {"status": False}
    return Response(answer)


@api_view(['POST'])
def update_survey(request):
    survey = Survey.objects.get(id=request.data["survey"]["id"])
    serializer = SurveySerializer()
    try:
        answer = serializer.update(instance=survey, validated_data=request.data)
    except Exception:
        answer = {"status": False}
    return Response(answer)


@api_view(['POST'])
def delete_survey(request):
    survey = Survey.objects.get(request.data["survey"]["id"])
    serializer = SurveySerializer()
    try:
        answer = serializer.delete(survey)
    except Exception:
        answer = {"status": False}
    return answer


@api_view(['POST'])
def create_question(request):
    serializer = QuestionSerializer()
    try:
        answer = serializer.create(request.data)
    except Exception:
        answer = {"status": False}
    return Response(answer)


@api_view(['POST'])
def update_question(request):
    serializer = QuestionSerializer()
    question_data = request.data["questions"]
    answer = {"status": True}
    for question in question_data.values():
        question_db = Question.objects.get(id=question["question"]["id"])
        result = serializer.update(instance=question_db, validated_data=question)
        if not result:
            answer = {"status": False}
            break
    return Response(answer)


@api_view(['POST'])
def delete_question(request):
    serializer = QuestionSerializer()
    question_data = request.data["questions"]
    for question in question_data:
        question_db = Question.objects.get(id=question["id"])
        serializer.delete(question_db)
    answer = {"status": True}
    return Response(answer)


@api_view(['POST'])
def create_answer(request):
    serializer = AnswerSerializer()
    answer = serializer.create(request.data)
    return Response(answer)


@api_view(['GET'])
def view_survey(request):
    surveys = Survey.objects.filter(date_to_start__gte=now()).exclude(date_to_finish__lte=now())
    return Response(surveys)


@api_view(['POST'])
def view_answer(request):
    answers = AnswerUser.objects.filter(id=request.data["user"]["id"])
    return Response(answers)
