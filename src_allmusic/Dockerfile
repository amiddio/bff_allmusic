FROM python:3.10

COPY src /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

RUN adduser --disabled-password app-user

USER app-user

EXPOSE 8081

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8081 --reload
