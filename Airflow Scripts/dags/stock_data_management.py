from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['nanda.shr@northeastern.edu'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
}

with DAG(
    'stock_data_management',
    default_args=default_args,
    description='A DAG to run Python scripts for stock data management',
    schedule_interval='0 2 * * *',  # Runs at 2 AM every day
    catchup=False,
    tags=['example'],
) as dag:

    # Task to run update_stock_data.py script
    run_update_stock_data = BashOperator(
        task_id='run_update_stock_data',
        bash_command='python /Airflow Scripts/Scripts/convert_xlsx_pdf.py ',
    )

    # Sensor to wait for 2 minutes after the first task
    delay_task1 = TimeDeltaSensor(
        task_id='wait_for_2_minutes_after_update_stock_data',
        delta=timedelta(minutes=2),
    )

    # Task to convert XLSX to PDF
    convert_to_pdf = BashOperator(
        task_id='convert_to_pdf',
        bash_command='python /Airflow Scripts/Scripts/convert_xlsx_pdf.py ',
    )

    # Sensor to wait for 2 minutes after converting XLSX to PDF
    delay_task2 = TimeDeltaSensor(
        task_id='wait_for_2_minutes_after_convert_to_pdf',
        delta=timedelta(minutes=2),
    )

    # Task to run upload_to_s3.py script
    run_upload_to_s3 = BashOperator(
        task_id='run_upload_to_s3',
        bash_command='python /Airflow Scripts/Scripts/upload_to_s3.py ',
    )

    # Define the order of task execution
    run_update_stock_data >> delay_task1 >> convert_to_pdf >> delay_task2 >> run_upload_to_s3
