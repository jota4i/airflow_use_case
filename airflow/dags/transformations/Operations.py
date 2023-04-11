import os

from dotenv import load_dotenv

load_dotenv()

def land_to_raw(bucket_name, land_path, raw_path):

    from pyspark.sql import SparkSession

    SPARK_MASTER_ADDRESS = os.getenv("SPARK_MASTER_ADDRESS")

    app_name = raw_path.split("/")
    app_name = app_name[-1]
    spark = SparkSession.builder \
        .master(SPARK_MASTER_ADDRESS) \
        .config("spark.jars", "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar") \
        .appName(f"land_to_raw") \
        .getOrCreate()

    path = f"gs://{bucket_name}/{land_path}"

    df = spark.read.json(path)

    df.write. \
        mode("overwrite"). \
        parquet(f"gs://{bucket_name}/{raw_path}", compression="snappy" )


def raw_to_trusted(bucket_name, raw_path, trusted_path, app_name):

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import lit

    SPARK_MASTER_ADDRESS = os.getenv("SPARK_MASTER_ADDRESS")

    spark = SparkSession.builder \
        .master(SPARK_MASTER_ADDRESS) \
        .config("spark.jars", "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar") \
        .appName(f"raw_to_trusted_{app_name}") \
        .getOrCreate()

    path = f"gs://{bucket_name}/{raw_path}"

    df = spark.read.parquet(path)

    df = df.withColumn("modelo_veiculo", lit(app_name))

    df.write. \
        mode("overwrite"). \
        parquet(f"gs://{bucket_name}/{trusted_path}", compression="snappy" )
