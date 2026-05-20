# Airflow + MLOps Setup Notes

## 1. Project Goal

Build a first MLOps training pipeline using Apache Airflow to orchestrate an MLflow + XGBoost NYC Taxi duration prediction workflow.

## 2. Airflow Setup

### Installation

```bash
pip install apache-airflow
```

### Airflow 3 startup

```bash
airflow standalone
```

This initializes the DB, starts scheduler/webserver/triggerer, and creates admin credentials.

## 3. Moving Airflow into Project Directory

```bash
export AIRFLOW_HOME=/home/drbigbrain/Desktop/Projects/end2endMLandWebApp/AirFlow
export PYTHONPATH=/home/drbigbrain/Desktop/Projects/end2endMLandWebApp:$PYTHONPATH
airflow db migrate
airflow standalone
```

Why:

* `AIRFLOW_HOME`: controls config/db/logs/dags root
* `PYTHONPATH`: allows importing project modules like `durationPrediction`

## 4. Problems Faced + Fixes

### CLI mismatch

Old `airflow users` flow failed because Airflow 3 changed CLI.

### DAG not appearing

Causes:

* wrong DAG folder
* wrong AIRFLOW_HOME
* stale Airflow process
  Fix:

```bash
airflow dags list
airflow config get-value core dags_folder
```

### No module named durationPrediction

Fix:

```bash
export PYTHONPATH=/project/root:$PYTHONPATH
```

### Airflow import mismatch

Wrong:

```python
from airflow.models.param import Param
```

Correct:

```python
from airflow.sdk import dag, task, Param
```

### MLflow crash during DAG parsing

Cause: network calls at module import.
Fix: move MLflow setup inside runtime function.

### Jinja typo

Wrong:

```python
{{ param.year }}
```

Correct:

```python
{{ params.year }}
```

### String/int bug

Jinja params are strings.
Fix:

```python
run(year=int(year), month=int(month))
```

### MLflow connection refused

Fix:

```bash
mlflow ui
```

## 5. Final Pipeline

```python
from airflow.sdk import dag, task, Param
from datetime import datetime
from durationPrediction import run

@dag(
    dag_id="training_pipeline",
    schedule="@monthly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["NY Taxi", "MLOps"],
    params={
        "year": Param(2024, type="integer"),
        "month": Param(1, type="integer"),
    },
)
def training_pipeline():
    @task
    def train_model(year, month):
        run(year=int(year), month=int(month))

    train_model("{{ params.year }}", "{{ params.month }}")

dag = training_pipeline()
```

## 6. Detailed Parameter Notes

### `@dag`

Defines workflow container.

### `dag_id`

Unique DAG identifier shown in UI.

### `schedule`

Execution frequency.
Examples: `@daily`, `@monthly`, cron.

### `start_date`

Anchor for scheduling.

### `catchup`

If True: backfills missed runs.
If False: only future/manual runs.

### `tags`

UI categorization labels.

### `params`

Runtime config injected into templates.

### `Param`

Typed DAG parameter.
Example:

```python
Param(2024, type="integer")
```

### `@task`

Turns Python function into schedulable Airflow task.
Provides:

* logging
* retries
* monitoring
* execution state tracking

### `datetime`

Used for scheduler timestamps.

### `run()`

Business logic entrypoint:

* fetch data
* preprocess
* train XGBoost
* compute RMSE
* log MLflow artifacts

### Jinja templates

```python
{{ params.year }}
```

Inject trigger-time values.

## 7. Airflow Lifecycle

```text
scan DAG folder
→ parse DAG files
→ register DAG
→ schedule/trigger
→ queue task
→ execute task
→ write logs
→ update state
```

## 8. MLOps Lessons

* orchestration != ML logic
* avoid top-level side effects
* use env vars over hardcoded infra
* tasks are isolated
* logs are essential

## 9. Next Steps

1. successful DAG run
2. verify MLflow
3. Dockerize Airflow + MLflow + Postgres
4. build FastAPI inference service
5. split monolithic run into multiple tasks
6. CI/CD
7. monitoring
