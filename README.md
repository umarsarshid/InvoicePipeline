# Real-Time Data Pipeline with Kafka and MongoDB

## Project Overview

This project implements a real-time data pipeline using Docker to ingest, process, and visualize e-commerce invoice data. It leverages FastAPI for data ingestion, Apache Kafka for data streaming, Apache Spark for stream processing, MongoDB for data storage, and Streamlit for data visualization. This setup is designed to provide insights into e-commerce operations through real-time analytics.

## Architecture

The project architecture consists of the following components:

- **FastAPI:** Serves as the entry point for data ingestion, accepting invoice data through a REST API.
- **Apache Kafka:** Acts as the backbone of the streaming data pipeline, ensuring scalable and reliable data transfer.
- **Apache Spark:** Processes the streaming data for analytics or transformations.
- **MongoDB:** Stores processed data, making it available for querying and visualization.
- **Streamlit:** Offers an interactive dashboard for visualizing the data stored in MongoDB.

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourgithub/repo.git
cd repo
```

### 2. Start the Services

Run the following command to start all services defined in the `docker-compose.yml`:

```sh
docker-compose up -d
```

### 3. Verify Service Status

Ensure all services are up and running:

```sh
docker-compose ps
```

### 4. Access the FastAPI Documentation

Navigate to `http://localhost:8000/docs` to view the FastAPI documentation and test the API endpoints.

### 5. View the Streamlit Dashboard

Open `http://localhost:8501` in your browser to access the real-time data visualization dashboard.

## Usage

### Sending Data to the FastAPI Endpoint

Use the following `curl` command to send invoice data to the FastAPI service:

```sh
curl -X 'POST' \
  'http://localhost:8000/invoices/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "invoice_id": "12345",
  "date": "2024-03-15",
  "customer_id": "501",
  "items": [
    {
      "item_id": "101",
      "name": "Product Name",
      "quantity": 2,
      "price": 9.99
    }
  ],
  "totalPrice": 19.98
}'
```

### Monitoring Kafka

Use Kafka command-line tools within the Kafka container to monitor topics and messages:

```sh
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

## Customizing the Setup

Refer to the `docker-compose.yml` and individual Dockerfiles for customization options, including changing service ports, volume mounts, and environment variables.

## Security Considerations

- Change default passwords and credentials.
- Consider enabling SSL/TLS for Kafka and MongoDB connections.

## Troubleshooting

- Use `docker logs [service_name]` to view logs for individual services.
- Ensure Docker volumes have appropriate permissions.

## Contributing

Contributions to the project are welcome! Please follow the standard fork and pull request workflow.

## License

Specify the project license here.

---
