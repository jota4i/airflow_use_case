# dags/branch_without_trigger.py
from datetime import datetime

from airflow.decorators import task
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator

dag_parameters = {
    "owner": "4I_team",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}

with DAG(
    dag_id="branch_without_trigger",
    schedule=None,
    description="Dag example to using logical flows.",
    default_args=dag_parameters,
    tags=["example", "python", "flow"],
) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline", dag=dag)

    @task.branch(task_id="random_flow")
    def do_branching():
        import random

        number = random.randint(0, 100)

        if number % 2 == 0:
            print(f"O número {number} é par. Seguir fluxo A.")
            return "flow_a_1"

        else:
            print(f"O número {number} é ímpar. Seguir fluxo B.")
            return "flow_b"

    random_flow = do_branching()

    flow_a_1 = EmptyOperator(task_id="flow_a_1", dag=dag)
    flow_a_2 = EmptyOperator(task_id="flow_a_2", dag=dag)

    flow_b = EmptyOperator(task_id="flow_b", dag=dag)

    end_pipeline = EmptyOperator(
        task_id="end_pipeline", dag=dag, trigger_rule="none_failed_min_one_success"
    )

    start_pipeline >> random_flow
    random_flow >> flow_a_1
    flow_a_1 >> flow_a_2
    random_flow >> flow_b
    flow_a_2 >> end_pipeline
    flow_b >> end_pipeline

dag.doc_md = """
# Example

Dag example to create a simple dag with multiple available flows. 

"""
