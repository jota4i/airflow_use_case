from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

dag_parameters = {
    "owner": "4I_team",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}

with DAG(
    dag_id="dag_science",
    default_args=dag_parameters,
    description="Dag responsable from run R scripts",
    tags=["fipe", "RScript"],
    schedule=None,
    owner_links={"4I_team": "mailto:j.adelmar@4intelligence.com.br"},
) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    run_science_model = BashOperator(
        task_id="run_science_model",
        bash_command="Rscript /opt/airflow/dags/R/hello_world.R",
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> run_science_model
    run_science_model >> end_pipeline

dag.doc_md = """
# [Vehicle] Science model

Run R script to execute Science analysis.
 """
