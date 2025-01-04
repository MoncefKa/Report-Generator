from airflow.decorators import dag,task
from airflow.models import Variable
from pymongo import MongoClient
from datetime import datetime
import json



default_args = {
    'owner': 'airflow',
    'retries': 1,
}

FILEPATH="data/github_data.json"

@dag(dag_id="github_data",default_args=default_args,schedule_interval="@daily",
                                                    start_date=datetime(2024, 12, 31))
def github_dag():
    
    @task
    def extract(filepath:str):
        try:
            with open(filepath,'r') as path:
                file=json.load(path)
            return file
        except Exception as e:
            return f"Error handling file reading exception {e}"
    
    @task
    def transform(gitData:dict):
        # Initialize Empty Dictionary Then Retrieve Relevant Data
        new_column={}
        if gitData != None:
            column_elements=gitData.get('organization',{})\
                .get('projectV2',{})\
                .get('items')
                
            for column in column_elements['nodes']:
                for keys,values in column.items():
                    if keys not in new_column:
                        new_column[keys]=[]
                    new_column[keys].append(values)      
                    
        # Retrieve Content [DraftIssues,Issues,PullRequests] From the Json File,Then Separates Each
        for column in new_column.get("content", {}):  
            new_key = column.get("__typename", None)
            if new_key:
                # Initialize the list for this key if not already present
                if new_key not in new_column:
                    new_column[new_key] = []
                # Append a structured entry for the current column
                structured_entry = {k: v for k, v in column.items() if k != "__typename"}
                new_column[new_key].append(structured_entry)
        new_column.pop('content')
        return new_column

    @task.bash
    def initClient():
        return """
            cd /home/cosmo/Report-Generator/scripts/
            python3 mongo_client.py
        """
    
    def mongodb_process():
        uri=Variable.get("MONGO_CLIENT")
        if uri:
            client=MongoClient(uri)
            
            return client
        return "Timed Out"

    @task
    def load(data:dict):
        collections=['DraftIssue','Issue','PullRequest']
        client=mongodb_process()
        
        try:
            db = client['GitData']
            if db.list_collection_names() != collections:
                for collection in collections:
                    collect=db.create_collection(collection)
                    collect.insert_one({
                        collection:[data[collection]
                                    ,data['createdAt']]
                    })
                        
                return "Successfuly inserted"
            
        except Exception as e:
            return f"Exception at {e}"
        
    initClient()
    load(transform(extract(FILEPATH)))

github_workflow=github_dag()