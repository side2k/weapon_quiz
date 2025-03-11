FROM python:2.7-slim

RUN apt update && \
    apt install -y git gcc sqlite3

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN chmod a+x entrypoint.sh
ENTRYPOINT [ "bash", "/app/entrypoint.sh" ]

COPY . .

RUN mkdir /var/lib/weapon_quiz/
ENV DJANGO_SETTINGS_MODULE=weapon_quiz.settings

RUN python manage.py syncdb --noinput
RUN python manage.py import_questions quiz_1.txt
RUN python manage.py import_questions quiz_2.txt

CMD ["gunicorn", "weapon_quiz.wsgi:application"]
