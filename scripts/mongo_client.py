from airflow.models import Variable
from dotenv import load_dotenv
import os

def set_variable_airflow():
        
    load_dotenv()
    mongodb_key=os.getenv('MONGO_CLIENT')
    if mongodb_key:
        Variable.set("MONGO_CLIENT",mongodb_key)
    else:
        return f"Error Reading Environment Variable... -> {Exception}"
    
    
set_variable_airflow()