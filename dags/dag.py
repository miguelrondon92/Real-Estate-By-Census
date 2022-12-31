from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, date

etl_dag= DAG(dag_id= "realtor_census_dashboard_etl",
            start_date= datetime(2022, 1 ,1),
            schedule_interval='@daily')

part_1 = BashOperator(
    task_id= "Extract_n_Transform_Data",
    bash_command= 'python3 transform_dfs.py',
    dag=etl_dag
)

part_2 = BashOperator(
    task_id= "SQL_2_CSV",
    bash_command= 'sh sql2csv.sh',
    dag=etl_dag
)

part_3 = BashOperator(
    task_id= "Run_Shiny_App",
    bash_command="sh ui/run_app.sh"
)

part_1 >> part_2 >> part_3 