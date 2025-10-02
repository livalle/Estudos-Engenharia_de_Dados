import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

#!pip install apache-airflow

#Função para buscar e salvar dados
def fetch_weather():
  url = "https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&hourly=temperature_2m,precipitation"
  r = requests.get(url)
  data = r.json()

  df = pd.DataFrame({
        "time":  data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "precipitation": data["hourly"]["precipitation"]
    })

  df.to_csv("/opt/airflow/data/weather.csv", index=False)

default_args = {
    'owner': 'li',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='weather_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 10, 2),
    schedule='@hourly',
    catchup=False
) as dag:

    task_fetch = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_weather
    )

    task_fetch


#intalação do docker no google colab
!sudo apt-get update && sudo apt-get install docker-compose-v2
!sudo apt-get update
!sudo apt-get install docker-compose-plugin

#rodando na celula
!curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'
!mkdir -p ./dags ./logs ./plugins ./data
!docker-compose up airflow-init
!docker-compose up -d
