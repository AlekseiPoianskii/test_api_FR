from django.shortcuts import render
from apiapp.serializers import SurveySerializer, QuestionSerializer, AnswerSerializer
from surveyapp.models import Survey, Question, AnswerUser, AnswerQuestion
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.timezone import now


@api_view(["GET"])
def view_survey(request):
    """
    Функция возвращает все существующие опросы
    :param request:
    :return: surveys
    """
    answers = dict()
    surveys = list(Survey.objects.all())
    for survey in surveys:
        answers[f'{survey.id}'] = {
            'id': survey.id,
            'name_survey': survey.name_survey,
            'date_to_start': survey.date_to_start,
            'date_to_finish': survey.date_to_finish,
            'description': survey.description
        }
    return Response(answers)


@api_view(['POST'])
def create_survey(request):
    """
    Функция вызывает создание экземпляров в моделях опроса, вопросов и вариантов ответов.
    В теле запроса должно отправляться следующий вид json:
    {
      "survey": {
        "name_survey": "Название опроса",
        "date_to_start": "Дата и время начала опроса",
        "date_to_finish": "Дата и время окончания опроса",
        "description": "Описание опроса"
      },
      "questions": {
        "1": {
          "question": {
            "text_question": "Текст вопроса",
            "type_question": "Тип вопроса"
          },
          "answers": {
            "1": {
              "text_answer": "Текст ответа",
              "is_true": Bool true если верный и  false если не верный
            }
          }
        }
      }
    }
    :param request: survey, question
    :return: status
    """
    survey = SurveySerializer()
    try:
        answer = survey.create(validated_data=request.data)
    except Exception:
        answer = {"status": False}
    return Response(answer)


@api_view(['POST'])
def update_survey(request):
    """
    Функция вызывает обновление экземпляра в модели опроса.
    В теле запроса должно отправляться следующий вид json:
    {
      "survey": {
        "id": "id опроса",
        "name_survey": "Новое название опроса",
        "date_to_start": "Новая дата старта опроса",
        "date_to_finish": "новая дата окончания опросо",
        "description": "Новое описание"
      }
    }
    :param request: survey
    :return: status
    """
    survey = Survey.objects.get(id=request.data["survey"]["id"])
    serializer = SurveySerializer()
    try:
        answer = serializer.update(instance=survey, validated_data=request.data)
    except Exception:
        answer = {"status": False}
    return Response(answer)


@api_view(['POST'])
def delete_survey(request):
    """
    Функция вызывает удаление экземпляра модели опроса.
    В теле запроса должно отправляться следующий вид json:
    {
      "survey": {
        "id": "1"
      }
    }
    :param request: survey
    :return: status
    """
    survey = Survey.objects.get(request.data["survey"]["id"])
    serializer = SurveySerializer()
    try:
        answer = serializer.delete(survey)
    except Exception:
        answer = {"status": False}
    return answer


@api_view(['POST'])
def create_question(request):
    """
    Функция вызывает создание экземпляров в моделях вопросов и ответов.
    В теле запроса должно отправляться следующий вид json:
    {
      "survey": {
        "id": "id опроса"
      },
      "questions": {
        "1": {
          "question": {
            "text_question": "Год",
            "type_question": "SC"
          },
          "answers": {
            "1": {
              "text_answer": "2021",
              "is_true": true
            },
            "2": {
              "text_answer": "2020",
              "is_true": false
            }
          }
        }
      }
    }
    :param request: survey, question
    :return: status
    """
    serializer = QuestionSerializer()
    try:
        answer = serializer.create(request.data)
    except Exception:
        answer = {"status": False}
    return Response(answer)


@api_view(['POST'])
def update_question(request):
    """
    Функция вызывает обновление экземпляра модели вопроса.
    В теле запроса должно отправляться следующий вид json:
    {
      "questions": {
        "1": {
          "question": {
            "id": "1",
            "text_question": "Столица России",
            "type_question": "MC",
            "answers": {
              "1": {
                "text_answer": "Москва",
                "is_true": true
              }
            }
          }
        }
      }
    }
    :param request: question
    :return: status
    """
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
    """
    Функция вызывает удаление экземпляра модели вопроса.
    В теле запроса должно отправляться следующий вид json:
    {
      "questions": {
        "1": {
          "question": {
            "id": "1"
          }
        }
      }
    }
    :param request: question
    :return: status
    """
    serializer = QuestionSerializer()
    question_data = request.data["questions"]
    for question in question_data:
        question_db = Question.objects.get(id=question["id"])
        serializer.delete(question_db)
    answer = {"status": True}
    return Response(answer)


@api_view(['POST'])
def create_answer(request):
    """
    Функция вызывает создание экземпляров модели ответов пользователя.
    В теле запроса должно отправляться следующий вид json:
    {
      "user": "Anonymous или информация о пользователе",
      "answers": {
        "1": {
          "question_1": "Вопрос",
          "survey_id": "Опрос",
          "answer_id": "Вариант ответа"
        }
      }
    }

    *answer_id необходимо заменить на text_answer, если на вопрос необходим текстовый ответ
    :param request: user, answers
    :return: status
    """
    serializer = AnswerSerializer()
    answer = serializer.create(request.data)
    return Response(answer)


@api_view(['GET'])
def view_accessible_survey(request):
    """
    Функция возвращает все доступные для прохождения опросы
    :param request:
    :return: survey
    """
    surveys = Survey.objects.filter(date_to_start__gte=now()).exclude(date_to_finish__lte=now())
    return Response(surveys)


@api_view(['POST'])
def view_answer(request):
    """
    Функция возвращает все ответы пользователя на опросы.
    В теле запроса должно отправляться следующий вид json:
    {
      "user": {
        "id": "1"
      }
    }
    :param request: user
    :return: survey
    """
    survey_passed = list()
    answers_response = dict()
    answers_temp = list(AnswerUser.objects.filter(id=request.data["user"]["id"]))
    for answer in answers_temp:
        if answer.survey not in survey_passed:
            survey_passed.append(answer.survey)
    for survey_id in survey_passed:
        answers_response[f'{survey_id}'] = Survey.objects.get(id=survey_id)
        answers_response[f'{survey_id}']['questions'] = dict()
        questions = list(Question.objects.filter(survey_id=survey_id))
        for question in questions:
            answers_response[f'{survey_id}']['questions'][f'{question.id}'] = question
            answers_response[f'{survey_id}']['questions'][f'{question.id}']['answers'] = dict()
            answer = AnswerUser.objects.filter(question=question)
            answers_response[f'{survey_id}']['questions'][f'{question.id}']['answers'][
                answer.id] = answer.text_answer if answer.text_answer != '' else answer.answer_id

    return Response(answers_response)
