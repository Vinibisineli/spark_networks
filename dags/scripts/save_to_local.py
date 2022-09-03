import json
import os
from tokenize import String
import requests

class SaveFile:

    def save_json_to_file(http:String, endpoint:String, file_name: String) -> None:
        
        my_request = http+endpoint
        x = requests.get(my_request)
        with open(f'/opt/airflow/dags/data/{file_name}', 'wb') as f:
            f.write(x.content)

