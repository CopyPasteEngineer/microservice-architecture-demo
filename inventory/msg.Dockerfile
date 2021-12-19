FROM python:3.8

COPY ./domain.requirements.txt /domain.requirements.txt
RUN pip install -r /domain.requirements.txt
COPY ./infrastructure.requirements.txt /infrastructure.requirements.txt
RUN pip install -r /infrastructure.requirements.txt

COPY ./domain /app/domain
COPY ./adapter /app/adapter
COPY ./infrastructure /app/infrastructure
COPY ./message-handler /app/message-handler

ENV PYTHONPATH /app/
ENV PYTHONUNBUFFERED 1

CMD sleep 10 && python /app/message-handler/main.py
