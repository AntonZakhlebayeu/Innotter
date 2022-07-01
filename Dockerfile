FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.1.13

COPY . /app/

WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION" && poetry --version

RUN poetry config virtualenvs.create false && poetry install


EXPOSE 8000

CMD python manage.py runserver

