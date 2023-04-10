from datetime import datetime
from classes.Vehicles import GetVehicleBrand, GetVehicleModel, GetVehicleModelYear, GetVehicleDetails

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateExternalTableOperator,
)

dag_parameters = {
    "0wner": "airflow",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}

# Parameters
THIS_PARAM_IS_EXAMPLE = "dag variable"
VEHICLE_TYPES = ["carros","caminhoes","motos"]

def get_brands(vehicle_type):
    vehicles = GetVehicleBrand(vehicle_type)
    vehicles.get_vehicle_list()
    vehicles.save_to_file()


def transform_land_to_raw(vehicle_type):
    from transformations.Operations import land_to_raw
    land_to_raw("airflow4i_lake",f"land/brand/{vehicle_type}.json",f"raw/brand/{vehicle_type}")


def transform_raw_to_trusted(vehicle_type):
    from transformations.Operations import raw_to_trusted
    raw_to_trusted("airflow4i_lake",f"raw/brand/{vehicle_type}/*",f"trusted/brand/{vehicle_type}", vehicle_type)


with DAG(
    dag_id="dag_fipe_table",
    default_args=dag_parameters,
    description="Dag responsable from get FIPE info and save to datalake",
    tags=["fipe"],
    schedule=None,
) as dag:

    land_task_list = []
    raw_task_list = []
    trusted_task_list = []

    start_pipeline = EmptyOperator(task_id="start_pipeline")

    with TaskGroup(
        group_id = "land"
    ) as land_layer:

        for vtype in VEHICLE_TYPES:
            task_get_brands = PythonOperator(
                task_id=f"get_{vtype}_brands",
                python_callable=get_brands,
                op_args=[vtype],
            )
            land_task_list.append(task_get_brands)

        land_task_list

    with TaskGroup(
        group_id = "raw"
    ) as raw_layer:

        for vtype in VEHICLE_TYPES:
            task_get_brands = PythonOperator(
                task_id=f"transform_{vtype}_brands",
                python_callable=transform_land_to_raw,
                op_args=[vtype],
            )
            raw_task_list.append(task_get_brands)

        raw_task_list

    with TaskGroup(
        group_id = "trusted"
    ) as trusted_layer:

        for vtype in VEHICLE_TYPES:
            task_get_brands = PythonOperator(
                task_id=f"trusted_{vtype}_brands",
                python_callable=transform_raw_to_trusted,
                op_args=[vtype],
            )

            task_create_external_table = BigQueryCreateExternalTableOperator(
                task_id=f"bigquery_external_table_{vtype}",
                table_resource={
                    "tableReference": {
                        "projectId": "airflow4i",
                        "datasetId": "trusted_dataset",
                        "tableId": vtype,
                    },
                    "externalDataConfiguration": {
                        "sourceFormat": "PARQUET",
                        "sourceUris": [f"gs://airflow4i_lake/trusted/brand/{vtype}/*.parquet"],
                    },
                },
            )

            task_get_brands >> task_create_external_table

        # trusted_task_list



    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> land_layer
    land_layer >> raw_layer
    raw_layer >> trusted_layer
    trusted_layer >> end_pipeline
