from django.db import models
from django.db.models.manager import BaseManager
from django.utils.timezone import now
from usersapp.models import User
import datetime


class Survey(models.Model):
    '''
    Модель опроса.
    Имеет стандартное поле "id" и созданные поля:
    name_survey - название опроса
    date_to_start - дата и время начала опроса
    date_to_finish - дата и время окончания опроса
    description - описание опроса
    '''
    name_survey = models.CharField(max_length=40, verbose_name='Название')
    date_to_start = models.DateTimeField(default=now(), verbose_name='Дата старта')
    date_to_finish = models.DateTimeField(default=now()+datetime.timedelta(days=3), verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Описание')


class Question(models.Model):
    '''
    Модель вопросов.
    Имеет стандартное поле "id" и созданные поля:
    text_question - текст вопроса
    type_question - тип вопроса (один из TR, SC или MC)
    survey - опрос к которому принадлежит вопрос
    '''
    # Создание переменных для типов вопроса
    TEXT_RESPONSE = "TR" # вариант в виде текста
    SINGLE_CHOICE = "SC" # вариант с одним ответом
    MULTIPLE_CHOICE = "MC" # вариант с несколькими ответами

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
    '''
    Модель вариантов ответа.
    Имеет стандартное поле "id" и созданные поля:
    text_answer - текст ответа
    is_true - является ли правильным ответ
    question - вопрос к которому относится ответ
    '''
    text_answer = models.CharField(max_length=50, verbose_name="Текст варианта ответа")
    is_true = models.BooleanField(default=False, verbose_name="Правильный ответ")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос", default=0)


class AnswerUser(models.Model):
    '''
    Модель ответов пользователей.
    Имеет стандартное поле "id" и созданные поля:
    user - пользователь
    survey - опрос
    question - вопрос
    answer - вариант ответа
    text_answer - текст ответа
    последние два поля записываются одно из двух в зависимости от типа вопроса
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="Опрос", default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.ForeignKey(AnswerQuestion, on_delete=models.CASCADE, blank=True, verbose_name="Вариант ответа",
                               default=0)
    text_answer = models.CharField(max_length=50, blank=True, verbose_name="Текст ответа")
