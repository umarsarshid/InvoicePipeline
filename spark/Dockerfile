FROM bitnami/spark:3

# Install Python and PySparkUSER root
USER root
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install pyspark pymongo

# Add your Spark job script
ADD spark_job.py /opt/spark-job/spark_job.py

# MongoDB Spark Connector
ENV PACKAGES="org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
ENV PYSPARK_SUBMIT_ARGS="--packages ${PACKAGES} pyspark-shell"

CMD ["spark-submit", "/opt/spark-job/spark_job.py"]