# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV KAFKA_BOOTSTRAP_SERVERS kafka:9092

# Run Uvicorn without workers, suitable for development
# For production, consider using multiple workers
CMD ["uvicorn", "producer:app", "--reload", "--host", "0.0.0.0"]
