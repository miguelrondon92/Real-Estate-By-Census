from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

etl_dag= DAG("realtor_census_dashboard_etl")

part_1 = BashOperator(
    task_id= "Extract & Transform Data",
    bash_command= 'jupyter nbconvert --execute tranform_dfs.ipynb',
    dag=etl_dag
)