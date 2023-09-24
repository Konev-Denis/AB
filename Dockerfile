FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ARG APP_PORT=8000
ENV SERVER_PORT=$APP_PORT

EXPOSE $SERVER_PORT

ENTRYPOINT ["sh", "-c","uvicorn app.main:app --host 0.0.0.0 --port ${SERVER_PORT}"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
