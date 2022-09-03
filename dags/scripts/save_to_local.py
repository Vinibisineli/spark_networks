import json
import os
from tokenize import String

class SaveFile:

    def save_json_to_file(data:json, file_name: String) -> None:
        
        with open(f'/opt/airflow/dags/data/{file_name}', 'w') as f:
            json.dump(data, f)

