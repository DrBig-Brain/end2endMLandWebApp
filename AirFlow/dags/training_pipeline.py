#export AIRFLOW_HOME=/home/drbigbrain/Desktop/Projects/end2endMLandWebApp/AirFlow
#export PYTHONPATH=/home/drbigbrain/Desktop/Projects/end2endMLandWebApp/AirFlow:$PYTHONPATH
#export PYTHONPATH=/home/drbigbrain/Desktop/Projects/end2endMLandWebApp
from airflow.sdk import dag, task, Param
from datetime import datetime
from durationPrediction import run

@dag (
    dag_id = "training_pipeline",
    schedule = "@monthly",
    start_date = datetime(2026,5,20),
    catchup = False,
    tags = ["NY Taxi","MLOps"],
    params = {
        "year": Param(2024, type="integer"),
        "month": Param(1, type="integer")
    }
)

def training_pipeline():
    @task
    def train_model(year:int, month:int):
        run(year = year, month = int(month))

    train_model("{{ params.year }}","{{ params.month }}")

dag = training_pipeline()