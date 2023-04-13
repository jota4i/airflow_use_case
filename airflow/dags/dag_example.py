from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

dag_parameters = {
    "owner": "4I_team",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}


def get_csv_with_pandas():
    import pandas as pd

    print("# Iniciado a checagem de variaveis #")
    ## Podemos desenvolver a lógica da ETL diretamente aqui

    df = pd.read_csv("/opt/airflow/dags/example.csv")

    print(df)


with DAG(
    dag_id="dag_example",
    default_args=dag_parameters,
    description="Dag responsable from get FIPE info and save to datalake",
    tags=["example", "python"],
    schedule=None,
    owner_links={"4I_team": "mailto:j.adelmar@4intelligence.com.br"},
) as dag:
    land_task_list = []
    raw_task_list = []
    trusted_task_list = []

    start_pipeline = EmptyOperator(task_id="start_pipeline")

    get_csv_with_pandas = PythonOperator(
        task_id=f"get_csv_with_pandas",
        python_callable=get_csv_with_pandas,
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> get_csv_with_pandas
    get_csv_with_pandas >> end_pipeline

dag.doc_md = """
# Example

Dag example to create a simple dag

"""
