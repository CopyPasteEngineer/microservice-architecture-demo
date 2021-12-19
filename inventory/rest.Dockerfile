FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./domain.requirements.txt /domain.requirements.txt
RUN pip install -r /domain.requirements.txt
COPY ./infrastructure.requirements.txt /infrastructure.requirements.txt
RUN pip install -r /infrastructure.requirements.txt
COPY ./rest.requirements.txt /rest.requirements.txt
RUN pip install -r /rest.requirements.txt

COPY ./domain /app/domain
COPY ./adapter /app/adapter
COPY ./infrastructure /app/infrastructure
COPY ./rest /app/rest

# change this
ENV PYTHONPATH /app/rest

ENV APP_MODULE rest:app
ENV PORT 8080

CMD sleep 10 && uvicorn $APP_MODULE --host 0.0.0.0 --port $PORT --reload
