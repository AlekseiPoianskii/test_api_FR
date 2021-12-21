Для запуска сервера локально необходимо:

git clone https://github.com/AlekseiPoianskii/test_api_FR.git
pip install -r requirements.txt

Для запуска сервера:

python manage.py runserver

Примеры запросов и адреса:




http://localhost:8000/api/create-survey/

POST-запросы

json: 

{
  "survey": {
    "name_survey": "Опрос",
    "date_to_start": "2021-12-01 12:12:21.000",
    "date_to_finish": "2021-12-31 12:12:21.000",
    "description": "Первый опрос"
  },
  "questions": {
    "1": {
      "question": {
        "text_question": "Страна",
        "type_question": "SC"
      },
      "answers": {
        "1": {
          "text_answer": "Россия",
          "is_true": true
        },
        "2": {
          "text_answer": "Германия",
          "is_true": false
        }
      }
    },
    "2": {
      "question": {
        "text_question": "Время года",
        "type_question": "MC"
      },
      "answers": {
        "1": {
          "text_answer": "зима",
          "is_true": true
        },
        "2": {
          "text_answer": "лето",
          "is_true": true
        }
      }
    },
    "3": {
      "question": {
        "text_question": "Город",
        "type_question": "TR"
      },
      "answers": "NaN"
    }
  }
}



http://localhost:8000/api/update-survey/

{
  "survey": {
    "id": "1",
    "name_survey": "Опрос 2",
    "date_to_start": "2021-12-03 15:30:00.00",
    "date_to_finish": "2021-12-31 18:30:00.00",
    "description": "новое описание"
  }
}

http://localhost:8000/api/delete-survey/


{
  "survey": {
    "id": "1"
  }
}


http://localhost:8000/api/create-question/

{
  "survey": {
    "id": "1"
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
    },
    "2": {
      "question": {
        "text_question": "Месяц",
        "type_question": "MC"
      },
      "answers": {
        "1": {
          "text_answer": "март",
          "is_true": true
        },
        "2": {
          "text_answer": "февраль",
          "is_true": true
        }
      }
    },
    "3": {
      "question": {
        "text_question": "время",
        "type_question": "TR"
      },
      "answers": "NaN"
    }
  }
}

http://localhost:8000/api/update-question/


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
          },
          "2": {
            "text_answer": "Новосибирск",
            "is_true": false
          }
        }
      }
    }
  }
}


http://localhost:8000/api/delete-question/


{
  "questions": {
    "1": {
      "question": {
        "id": "1"
      }
    },
    "2": {
      "question": {
        "id": "2"
      }
    },
    "3": {
      "question": {
        "id": "3"
      }
    }
  }
}


http://localhost:8000/api/create-answer/


{
  "user": "Anonymous",
  "answers": {
    "1": {
      "question_1": "1",
      "survey_id": "12",
      "answer_id": "1"
    },
    "2": {
      "question_1": "5",
      "survey_id": "12",
      "text_answer": "Привет"
    }
  }
}

http://localhost:8000/api/view-answers/

{
  "user": {
    "id": "1"
  }
}

GET-запросы

http://localhost:8000/api/view-surveys/

