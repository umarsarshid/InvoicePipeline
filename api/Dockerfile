# Dockerfile
FROM python:3.9

# Set environment variables that ensure Python runs in unbuffered mode.
# Recommended when running Python within Docker containers
# It doesn't allow Python to buffer outputs, which is useful for logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the current directory (where the Dockerfile is) into the container at /app
COPY . /app

# Set the working directory in the container to /app
WORKDIR /app/app
# Install any needed packages specified in requirements.txt
RUN pip install fastapi uvicorn kafka-python pydantic

# Run Uvicorn without workers, suitable for development
# For production, consider using multiple workers
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
