from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

dag_parameters = {
    "owner": "4I_team",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}

# Parameters
VEHICLE_TYPES = ["carros", "caminhoes", "motos"]

with DAG(
    dag_id="dag_manager",
    default_args=dag_parameters,
    description="Dag responsable from orchestrate FIPE pipeline.",
    tags=["fipe", "manager"],
    schedule="30 * * * *",
    owner_links={"4I_team": "mailto:j.adelmar@4intelligence.com.br"},
) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    trigger_brand = TriggerDagRunOperator(
        task_id=f"trigger_brand",
        trigger_dag_id="dag_vehicle_brand",
        wait_for_completion=True,
    )

    trigger_model = TriggerDagRunOperator(
        task_id=f"trigger_model",
        trigger_dag_id="dag_vehicle_model",
        wait_for_completion=True,
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> trigger_brand
    trigger_brand >> trigger_model
    trigger_model >> end_pipeline


dag.doc_md = """
# [Vehicle] Manager

Dag responsable to orchestrate other dags to FIPE pipeline.
FIPE pipeline has 3 pass:
 - [LAND] get data from API Rest, send json files to GCS 
 - [RAW] get JSON files, applicate data quality and save in Parquet Files to GCS 
 - [TRUSTED] get parquet files, add some columns and disponibilize in BigQuery.

Manager dag trigger other two dags:
 - Brands = Dag using python classes, functions and operators
 - Models = Dag using notebooks
 
 """
