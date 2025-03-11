#!/bin/bash
set -e

if [[ $1 == "migrate" ]]; then
    shift
    exec python manage.py migrate "$@"
fi

if [[ $1 == "runserver" ]]; then
    exec python manage.py runserver 0:8000
fi

if [[ $1 == "test" ]]; then
    export DJANGO_SETTINGS_MODULE=tests.test_settings
    shift
    exec pytest tests "$@"
fi

if [[ $1 == "manage" ]]; then
    shift
    exec python manage.py "$@"
fi

if [[ $1 == "gunicorn" ]]; then
    shift
    exec gunicorn weapon_quiz.wsgi:application -b 0.0.0.0:8000 "$@"
fi

exec "$@"
