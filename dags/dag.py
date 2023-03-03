from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, date

path = "/Users/miguelrondon/Desktop/CODE/data\ projects/Real-Estate-By-Census/"

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'schedule_interval': '@monthly',
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}


etl_dag= DAG(dag_id= "realtor_census_dashboard_etl",
            start_date=datetime(2022, 12, 30),
            default_args= default_args, 
            dagrun_timeout=timedelta(minutes=1)
            )

check_path = BashOperator(
    task_id= "check_path",
    bash_command="pwd",
    dag=etl_dag 
)

check_path2 = BashOperator(
    task_id="check_path2", 
    bash_command="pwd",
    dag=etl_dag
)

part_1 = BashOperator(
    task_id= "Extract_n_Transform_Data",
    bash_command= f'cd {path} && python3 transform_dfs.py',
    dag=etl_dag
)

part_2 = BashOperator(
    task_id= "SQL_2_CSV",
    bash_command= f'cd {path} && sh sql2csv.sh ',
    dag=etl_dag
)

part_3 = BashOperator(
    task_id= "Run_Shiny_App",
    bash_command=f'cd {path} && sh real_estate_ui/run_app.sh '
)

check_path >> part_1 >> check_path2 >> part_2