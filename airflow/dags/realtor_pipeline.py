from airflow import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from datetime import datetime
from airflow.models import Variable
import subprocess
from realtor_checker import get_realtor_update_text


def check_for_update(**context):
    current = get_realtor_update_text()
    previous = Variable.get("realtor_update_text", default_var="")

    if current == previous:
        print(f"No Realtor update (still: {current!r}). Skipping ETL and dbt.")
        return False

    print(f"Realtor update detected: {previous!r} -> {current!r}")
    context["ti"].xcom_push(key="realtor_update_text", value=current)
    return True


def commit_realtor_update(**context):
    current = context["ti"].xcom_pull(
        task_ids="check_realtor_update",
        key="realtor_update_text",
    )
    if not current:
        raise ValueError("Missing realtor_update_text from check_realtor_update")

    Variable.set("realtor_update_text", current)
    print(f"Recorded Realtor update text: {current!r}")


def run_etl():
    result = subprocess.run(
        ["python", "/opt/airflow/etl/etl.py"],
        capture_output=True,
        text=True,
    )

    print("STDOUT:")
    print(result.stdout)

    print("STDERR:")
    print(result.stderr)

    result.check_returncode()


def run_dbt():
    result = subprocess.run(
        ["dbt", "run", "--profiles-dir", "/opt/airflow/dbt"],
        cwd="/opt/airflow/dbt",
        capture_output=True,
        text=True,
    )

    print("STDOUT:")
    print(result.stdout)

    print("STDERR:")
    print(result.stderr)

    result.check_returncode()


with DAG(
    "realtor_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    check = ShortCircuitOperator(
        task_id="check_realtor_update",
        python_callable=check_for_update,
    )

    etl = PythonOperator(task_id="run_etl", python_callable=run_etl)

    dbt = PythonOperator(task_id="run_dbt", python_callable=run_dbt)

    commit = PythonOperator(
        task_id="commit_realtor_update",
        python_callable=commit_realtor_update,
    )

    check >> etl >> dbt >> commit
