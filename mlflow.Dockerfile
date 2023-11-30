FROM akraradets/ait-ml-base:2023

RUN apt update && apt upgrade -y

RUN pip3 install --upgrade pip3
RUN pip3 install mlflow

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /mlflow
CMD mlflow server --backend-store-uri mlflow_db --default-artifact-root ./mlflowruns --host 0.0.0.0 --port 5000