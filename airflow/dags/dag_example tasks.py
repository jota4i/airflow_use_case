from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


dag_parameters = {
    "owner": "4I_team",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}

TASK_LIST = Variable.get("TASK_LIST", [], deserialize_json=True)


def print_item(item):
    print(item)


with DAG(
    dag_id="dag_example_task",
    default_args=dag_parameters,
    description="Dag responsable from get FIPE info and save to datalake",
    tags=["example", "python"],
    schedule=None,
    owner_links={"4I_team": "mailto:j.adelmar@4intelligence.com.br"},
) as dag:
    task_list = []

    start_pipeline = EmptyOperator(task_id="start_pipeline")

    for task in TASK_LIST:
        print_task = PythonOperator(
            task_id=f"print_item_{task}", python_callable=print_item, op_args=[task]
        )
        task_list.append(print_task)

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> task_list
    task_list >> end_pipeline

dag.doc_md = """
# Example

Dag example to create a simple dag

"""
