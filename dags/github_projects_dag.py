from airflow.decorators import dag,task
from datetime import datetime

@dag("github_data",schedule=datetime(year=2024,month=12,day=31),
     schedule_interval="daily",start_date=datetime(year=2024,month=12,day=31))
def github_dag():
    pass