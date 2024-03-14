# Dockerfile
FROM python:3.9
COPY ./app /app
WORKDIR /app
RUN pip install fastapi uvicorn kafka-python
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]