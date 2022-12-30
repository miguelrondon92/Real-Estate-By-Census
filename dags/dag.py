from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, date

etl_dag= DAG(dag_id= "realtor_census_dashboard_etl",
            start_date= datetime(2022, 1 ,1),
            schedule_interval='@daily')

part_1 = BashOperator(
    task_id= "Extract_n_Transform_Data",
    bash_command= 'jupyter nbconvert --execute tranform_dfs.ipynb',
    dag=etl_dag
)

test_dag = DAG(dag_id= "test_dag",
                start_date=date.today(),
                schedule_interval='@daily')

test_task = BashOperator(
    task_id= "Test_Task",
    bash_command= 'echo "Hello World" > hello.txt',
    dag=test_dag
)