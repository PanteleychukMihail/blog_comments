FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/

# Опционально, выполняем миграции и сбор статики
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]