Descrição do Projeto:
Este projeto implementa um pipeline de dados orquestrado com Apache Airflow, responsável por coletar dados de previsão do tempo de uma API pública (Open-Meteo), transformar e armazenar em formato CSV.
A ideia é demonstrar, de forma prática e simples, como estruturar um ETL (Extract, Transform, Load) automatizado, com agendamento e monitoramento via Airflow.


Pipeline de Dados >> Fluxo do pipeline:

Ingestão (Extract):
Consulta a API pública da Open-Meteo para coletar dados de temperatura e precipitação.

Transformação (Transform):
Conversão da resposta em JSON para DataFrame Pandas.
Seleção das colunas mais relevantes (time, temperature, precipitation).

Carga (Load):
Exportação dos dados em formato CSV dentro da pasta /opt/airflow/data/.

Orquestração:
DAG no Apache Airflow agenda a execução de hora em hora.



Estrutura de Pastas
weather_pipeline/
│── dags/
│   └── weather_dag.py        # Definição da DAG no Airflow
│
│── data/
│   └── weather.csv           # Arquivo CSV gerado pelo pipeline
│
│── scripts/ (opcional)
│   └── fetch_weather.py      # Script auxiliar de ingestão
│
│── docker-compose.yaml       # Subida do Airflow via Docker
│── README.md                 # Documentação do projeto



Configuração e Execução: Clonar o repositório
git clone https://github.com/seu-usuario/weather-pipeline-airflow.git
cd weather-pipeline-airflow


Subir o Airflow com Docker
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./data
docker-compose up airflow-init
docker-compose up -d


Adicionar a DAG : Copia o arquivo weather_dag.py para a pasta dags/.
cp dags/weather_dag.py ./dags/



Acessar o Airflow

URL: http://localhost:8080

Usuário padrão: airflow

Senha padrão: airflow

Ative a DAG weather_pipeline e ela será executada de hora em hora.


👩‍💻 Autor

Projeto desenvolvido por Li, com foco em aprendizado de pipelines de dados e orquestração com Airflow.
