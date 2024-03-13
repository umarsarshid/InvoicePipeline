# Dockerfile
FROM python:3.9
COPY ./app /app
WORKDIR /app
# Modified part of the Dockerfile
COPY requirements.txt /app/
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]