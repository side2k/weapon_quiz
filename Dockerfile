FROM python:2.7-slim

RUN apt update && \
    apt install -y git gcc python-dev libmariadb-dev-compat

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN chmod a+x entrypoint.sh
ENTRYPOINT [ "bash", "/app/entrypoint.sh" ]

COPY . .

ENV DJANGO_SETTINGS_MODULE=weapon_quiz.settings

CMD ["gunicorn", "weapon_quiz.wsgi:application"]
