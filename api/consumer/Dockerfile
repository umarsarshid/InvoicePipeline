# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV KAFKA_BOOTSTRAP_SERVERS kafka:9092
ENV MONGO_URI mongodb://mongodb:27017/

# Command to run the consumer script
CMD ["python", "consumer.py"]