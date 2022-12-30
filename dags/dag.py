from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

etl_dag= DAG(dag_id= "realtor_census_dashboard_etl",
            start_date= datetime(2022, 1 ,1),
            schedule_interval='@daily')

part_1 = BashOperator(
    task_id= "Extract_n_Transform_Data",
    bash_command= 'jupyter nbconvert --execute tranform_dfs.ipynb',
    dag=etl_dag
)