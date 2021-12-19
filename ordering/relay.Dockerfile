FROM python:3.8

COPY ./domain.requirements.txt /domain.requirements.txt
RUN pip install -r /domain.requirements.txt
COPY ./infrastructure.requirements.txt /infrastructure.requirements.txt
RUN pip install -r /infrastructure.requirements.txt

COPY ./domain /app/domain
COPY ./infrastructure /app/infrastructure
COPY ./adapter /app/adapter
COPY ./relay/ /app/relay

ENV PYTHONPATH /app/
ENV PYTHONUNBUFFERED 1

CMD sleep 10 && python /app/relay/main.py
