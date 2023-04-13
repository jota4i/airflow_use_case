from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.papermill.operators.papermill import PapermillOperator

dag_parameters = {
    "owner": "4I_team",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}

with DAG(
    dag_id="dag_vehicle_model",
    default_args=dag_parameters,
    description="Dag responsable from get FIPE info and save to datalake",
    tags=["fipe", "notebooks", "spark"],
    schedule=None,
    owner_links={"4I_team": "mailto:j.adelmar@4intelligence.com.br"},
) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    task_get_brands = PapermillOperator(
        task_id=f"get_models_brands",
        input_nb="/opt/airflow/dags/notebooks/get_models.ipynb",
        output_nb="/opt/airflow/dags/notebooks/outputs/get_models.ipynb",
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> task_get_brands
    task_get_brands >> end_pipeline

dag.doc_md = """
# [Vehicle] Models

Dag responsable to get models based in brands.
Models are created executing a notebook in pipeline. 
 """
