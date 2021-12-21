from rest_framework import serializers
from django.utils.timezone import now
from usersapp.models import User
from surveyapp.models import Survey, Question, AnswerQuestion, AnswerUser
import json


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

    def create(self, validated_data):
        survey_data = validated_data['survey']
        survey = Survey.objects.create(**survey_data)
        for question in validated_data['questions'].values():
            question_temp = Question.objects.create(**question['question'], survey=survey)
            if question['answers'] != "NaN":
                for answer in question['answers'].values():
                    AnswerQuestion.objects.create(**answer, question=question_temp)
            else:
                continue
        return {"status": True}

    def update(self, instance: Survey, validated_data):
        data = validated_data["survey"]
        if now() >= instance.date_to_start:
            return {"status": False, "message": "Опрос уже запущен"}
        else:
            instance.objects.update(**data)
            return {"status": True}

    @staticmethod
    def delete(survey: Survey):
        survey.delete()
        return {"status": True}


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        if validated_data["survey"]:
            survey = Survey.objects.get(id=validated_data['survey']['id'])
            for question in validated_data["questions"].values():
                answers_data = question.pop("answers")
                Question.objects.create(**question, survey=survey)
                if answers_data != "NaN":
                    for answer in answers_data.velues():
                        AnswerQuestion.objects.create(**answer, question=question)
            return {"status": True}
        else:
            return {"status": False, "message": "Не указан опрос"}

    def update(self, instance: Question, validated_data):
        data_answers = validated_data.pop("answers")

        if instance.type_question != "TR" and validated_data["question"]["type_question"] != "TR":
            answers = list(AnswerQuestion.objects.filter(question=instance))
            for answer in data_answers.values():
                if answer["id"] == 0:
                    AnswerQuestion.objects.create(**answer, question=instance)
                else:
                    answer_db = AnswerQuestion.objects.get(id=answer['id'])
                    answers.remove(answer_db)
                    answer_db.text_answer = answer["text_answer"]
                    answer_db.is_true = answer["is_true"]
                    answer_db.save()
            if len(answers) != 0:
                for answer in answers:
                    answer.delete()

        elif instance.type_question != "TR" and validated_data["type_question"] == "TR":
            answers = list(AnswerQuestion.objects.filter(question=instance))
            for answer in answers:
                answer.delete()

        elif instance.type_question == "TR" and validated_data["type_question"] != "TR":
            for answer in data_answers.values():
                AnswerQuestion.objects.create(**answer, question=instance)

        instance.text_question = validated_data["question"]["text_question"]
        instance.type_question = validated_data["question"]["type_question"]

        instance.save()
        return True

    @staticmethod
    def delete(question: Question):
        question.delete()
        return True


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerUser
        fields = "__all__"

    def create(self, validated_data):
        if validated_data["user"] == "Anonymous":

            user = User.objects.create(first_name="anonymous", username=f'{now().minute+now().microsecond}')
        else:
            user = User.objects.get(**validated_data['user'])
        answers = validated_data["answers"]
        for answer in answers.values():
            question = Question.objects.get(id=answer["question_1"])
            survey = Survey.objects.get(id=answer["survey_id"])
            if answer["answer_id"]:
                answer_question = AnswerQuestion.objects.get(id=answer['answer_id'])
                AnswerUser.objects.create(question=question, survey=survey, answer=answer_question, user=user)
            else:
                AnswerUser.objects.create(question=question, survey=survey, text_answer=answer["text_answer"])
        return {'status': True}

