FROM python:3.8

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app/

ENV PYTHONPATH /app/
ENV PYTHONUNBUFFERED 1

CMD python /app/main.py
