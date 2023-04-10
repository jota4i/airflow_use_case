from google.cloud import storage

class GCSUploader:
    def __init__(self, local_path, blob_path, bucket):
        self.local_path = local_path
        self.blob_name = blob_path
        self.bucket_name = bucket
        
        # Configuração do cliente GCS
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)
        print("Instanciou")

    def upload(self):
        # Envio do arquivo para o GCS
        blob = self.bucket.blob(self.blob_name)
        blob.upload_from_filename(self.local_path)

        print(f'O arquivo {self.local_path} foi enviado para {self.blob_name} no GCS')
