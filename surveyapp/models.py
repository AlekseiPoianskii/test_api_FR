from django.db import models
from django.utils.timezone import now
from usersapp.models import User
import datetime


class Survey(models.Model):
    name_survey = models.CharField(max_length=40, verbose_name='Название')
    date_to_start = models.DateTimeField(default=now(), verbose_name='Дата старта')
    date_to_finish = models.DateTimeField(default=now()+datetime.timedelta(days=3), verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Описание')


class Question(models.Model):
    TEXT_RESPONSE = "TR"
    SINGLE_CHOICE = "SC"
    MULTIPLE_CHOICE = "MC"

    TYPE_QUESTION_CHOICE = (
        (TEXT_RESPONSE, 'текстовый ответ'),
        (SINGLE_CHOICE, 'один ответ'),
        (MULTIPLE_CHOICE, 'несколько ответов'),
    )

    text_question = models.CharField(max_length=200, verbose_name='Текст вопроса')
    type_question = models.CharField(max_length=2, choices=TYPE_QUESTION_CHOICE, default=TEXT_RESPONSE,
                                     verbose_name='Тип вопроса')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Опрос')


class AnswerQuestion(models.Model):
    text_answer = models.CharField(max_length=50, verbose_name="Текст варианта ответа")
    is_true = models.BooleanField(default=False, verbose_name="Правильный ответ")


class AnswerUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.ForeignKey(AnswerQuestion, on_delete=models.CASCADE, blank=True, verbose_name="Вариант ответа")
    text_answer = models.CharField(max_length=50, blank=True, verbose_name="Текст ответа")
