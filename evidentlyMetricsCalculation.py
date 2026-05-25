"""
ML Monitoring with Evidently AI — Batch Backfill

Computes prediction drift, column drift, and missing-value metrics
day-by-day on Feb 2021 taxi data vs. the Jan 2021 reference set,
then stores them in PostgreSQL for Grafana dashboards.

Prerequisites:
  1. Run  python data/prepare_reference_data.py  to generate reference + current data
  2. Start infrastructure:  docker compose up -d  (Postgres, Grafana, Adminer)
"""
import datetime
import time
import pickle
import logging

import pandas as pd
import xgboost as xgb
import psycopg

from prefect import task, flow

from evidently import Report, DataDefinition, Dataset
from evidently.metrics import ValueDrift, DriftedColumnsCount, MissingValueCount

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10

# ── SQL ───────────────────────────────────────────────────────────────────────
create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
    timestamp timestamp,
    prediction_drift float,
    num_drifted_columns integer,
    share_missing_values float
)
"""

# ── Model & preprocessor (same artifacts used by durationPrediction.py) ──────
MODEL_PATH = 'mlartifacts/2/models/m-0193aed2bece416aa9be6d8d704cc430/artifacts/model.ubj'
DV_PATH = 'mlartifacts/2/a6992f0cca6540daab18330a522b4441/artifacts/preprocessor/preprocessor.b'

logging.info("Loading XGBoost model and DictVectorizer …")
xgb_model = xgb.Booster()
xgb_model.load_model(MODEL_PATH)

with open(DV_PATH, 'rb') as f:
    dv = pickle.load(f)


def preprocess(df):
    """Apply the same preprocessing as the training pipeline."""
    df = df.copy()
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df['duration'] = df.duration.apply(lambda td: td.total_seconds() / 60)
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    return df


def add_predictions(df):
    """Generate predictions with the XGBoost model via the DictVectorizer."""
    cat_feats = ['PU_DO']
    num_feats = ['trip_distance']
    dicts = df[cat_feats + num_feats].to_dict(orient='records')
    X = dv.transform(dicts)
    dmatrix = xgb.DMatrix(X)
    df = df.copy()
    df['prediction'] = xgb_model.predict(dmatrix)
    return df


# ── Load data ────────────────────────────────────────────────────────────────
reference_data = pd.read_parquet('data/reference.parquet')

raw_data = pd.read_parquet('data/green_tripdata_2021-02.parquet')
raw_data = preprocess(raw_data)

begin = datetime.datetime(2021, 2, 1, 0, 0)

# Features to monitor for drift
num_features = ['passenger_count', 'trip_distance', 'fare_amount', 'total_amount']
cat_features = ['PULocationID', 'DOLocationID']

data_definition = DataDefinition(
    numerical_columns=num_features + ['prediction'],
    categorical_columns=cat_features,
)

report = Report(metrics=[
    ValueDrift(column='prediction'),
    DriftedColumnsCount(),
    MissingValueCount(column='prediction'),
])

# ── Database ─────────────────────────────────────────────────────────────────
CONNECTION_STRING = "host=localhost port=5432 user=postgres password=example"
CONNECTION_STRING_DB = CONNECTION_STRING + " dbname=test"


@task
def prep_db():
    with psycopg.connect(CONNECTION_STRING, autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("create database test;")
    with psycopg.connect(CONNECTION_STRING_DB) as conn:
        conn.execute(create_table_statement)


@task
def calculate_metrics_postgresql(i):
    current_data = raw_data[
        (raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
        (raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))
    ]

    if current_data.empty:
        logging.warning(f"No data for day offset {i}, skipping")
        return

    current_data = add_predictions(current_data)

    current_dataset = Dataset.from_pandas(current_data, data_definition=data_definition)
    reference_dataset = Dataset.from_pandas(reference_data, data_definition=data_definition)

    result = report.run(reference_data=reference_dataset, current_data=current_dataset)
    result_dict = result.dict()

    # Metric 0: ValueDrift(column='prediction') → value is the drift score (float)
    prediction_drift = result_dict['metrics'][0]['value']
    # Metric 1: DriftedColumnsCount() → value is {'count': N, 'share': S}
    num_drifted_columns = result_dict['metrics'][1]['value']['count']
    # Metric 2: MissingValueCount(column='prediction') → value is {'count': N, 'share': S}
    share_missing_values = result_dict['metrics'][2]['value']['share']

    logging.info(
        f"Day {i}: drift={prediction_drift:.4f}, "
        f"drifted_cols={num_drifted_columns}, "
        f"missing={share_missing_values:.4f}"
    )

    with psycopg.connect(CONNECTION_STRING_DB, autocommit=True) as conn:
        with conn.cursor() as curr:
            curr.execute(
                "insert into dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
                (begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values)
            )


@flow
def batch_monitoring_backfill():
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    for i in range(0, 27):
        calculate_metrics_postgresql(i)

        new_send = datetime.datetime.now()
        seconds_elapsed = (new_send - last_send).total_seconds()
        if seconds_elapsed < SEND_TIMEOUT:
            time.sleep(SEND_TIMEOUT - seconds_elapsed)
        while last_send < new_send:
            last_send = last_send + datetime.timedelta(seconds=10)
        logging.info("data sent")


if __name__ == '__main__':
    batch_monitoring_backfill()