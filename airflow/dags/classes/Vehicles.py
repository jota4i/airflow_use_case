import os

#LOCAL = docker/airflow/airflow
#DOCKER = /opt/airflow/dags

class GetVehicleBrand:
    def __init__(self, vehicle_type):
        local_test = "docker"
        if local_test == "docker":
            temp_path = "/opt/airflow/dags"
        else:
            temp_path = "docker/airflow/airflow"

        self.vehicle_type = vehicle_type
        self.url = f"https://parallelum.com.br/fipe/api/v1/{vehicle_type}/marcas"
        self.file_path = f"{temp_path}/files/land"
        self.bucket = "airflow4i_lake"


    def get_vehicle_list(self):
        from classes.HTTPRequests import HTTPRequester
        request = HTTPRequester(self.url)
        response = request.make_request()
        self.brands = response.json()


    def save_to_file(self):
        import json
        self.file_name = f"land/brand/{self.vehicle_type}.json"
        self.full_path = f"{self.file_path}/{self.file_name}"
        print(self.file_name)
        print(self.full_path)
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        with open(self.full_path, 'w') as f:
            json.dump(self.brands, f)    
        self.__send_to_gcp()


    def __send_to_gcp(self):
        from .Google import GCSUploader
        upload_to_gcs = GCSUploader(self.full_path,self.file_name,self.bucket)
        upload_to_gcs.upload()

    
class GetVehicleModel:


    def __init__(self, vehicle_type, cod_model):
        local_test = "docker"
        if local_test == "docker":
            temp_path = "/opt/airflow/dags"
        else:
            temp_path = "docker/airflow/airflow"

        self.vehicle_type = vehicle_type
        self.cod_model = cod_model
        self.url = f"https://parallelum.com.br/fipe/api/v1/{vehicle_type}/marcas/{cod_model}/modelos"
        self.file_path = f"{temp_path}/files/land"
        self.bucket = "airflow4i_lake"

    def get_model_detail(self):
        from classes.HTTPRequests import HTTPRequester
        request = HTTPRequester(self.url)
        response = request.make_request()
        models = response.json()
        self.models = models["modelos"]


    def save_to_file(self):
        import json
        self.file_name = f"models/{self.vehicle_type}_{self.cod_model}.json"
        self.full_path = f"{self.file_path}/{self.file_name}"
        print(self.file_name)
        print(self.full_path)
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        with open(self.full_path, 'w') as f:
            json.dump(self.models, f)    
        self.__send_to_gcp()


    def __send_to_gcp(self):
        from Google import GCSUploader
        upload_to_gcs = GCSUploader(self.full_path,self.file_name,self.bucket)
        upload_to_gcs.upload()


class GetVehicleModelYear:
    def __init__(self, vehicle_type, cod_model, cod_year):
        local_test = "docker"
        if local_test == "docker":
            temp_path = "/opt/airflow/dags"
        else:
            temp_path = "docker/airflow/airflow"

        self.vehicle_type = vehicle_type
        self.cod_model = cod_model
        self.cod_year = cod_year
        self.url = f"https://parallelum.com.br/fipe/api/v1/{vehicle_type}/marcas/{cod_model}/modelos/{cod_year}/anos"
        self.file_path = f"{temp_path}/files/land/years"
        self.bucket = "airflow4i_lake"

    def get_year_detail(self):
        from classes.HTTPRequests import HTTPRequester
        request = HTTPRequester(self.url)
        response = request.make_request()
        self.years = response.json()


    def save_to_file(self):
        import json
        self.file_name = f"{self.vehicle_type}_{self.cod_model}_{self.cod_year}.json"
        self.full_path = f"{self.file_path}/{self.file_name}"
        print(self.file_name)
        print(self.full_path)
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        with open(self.full_path, 'w') as f:
            json.dump(self.years, f)    
        self.__send_to_gcp()


    def __send_to_gcp(self):
        from Google import GCSUploader
        upload_to_gcs = GCSUploader(self.full_path,self.file_name,self.bucket)
        upload_to_gcs.upload()


class GetVehicleDetails:
    def __init__(self, vehicle_type, cod_model, cod_year, year):
        local_test = "docker"
        if local_test == "docker":
            temp_path = "/opt/airflow/dags"
        else:
            temp_path = "docker/airflow/airflow"

        self.vehicle_type = vehicle_type
        self.cod_model = cod_model
        self.cod_year = cod_year
        self.year = year
        self.url = f"https://parallelum.com.br/fipe/api/v1/{vehicle_type}/marcas/{cod_model}/modelos/{cod_year}/anos/{year}"
        self.file_path = f"{temp_path}/files/land/details"
        self.bucket = "airflo_4i_land"

    def get_detail(self):
        from classes.HTTPRequests import HTTPRequester
        request = HTTPRequester(self.url)
        response = request.make_request()
        self.details = response.json()


    def save_to_file(self):
        import json
        self.file_name = f"{self.vehicle_type}_{self.cod_model}_{self.cod_year}_{self.year}.json"
        self.full_path = f"{self.file_path}/{self.file_name}"
        print(self.file_name)
        print(self.full_path)
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        with open(self.full_path, 'w') as f:
            json.dump(self.details, f)    
        self.__send_to_gcp()


    def __send_to_gcp(self):
        from Google import GCSUploader
        upload_to_gcs = GCSUploader(self.full_path,self.file_name,self.bucket)
        upload_to_gcs.upload()
