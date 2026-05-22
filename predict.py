import os
import pickle
from dotenv import load_dotenv
import mlflow
from flask import Flask, request, jsonify
import pandas as pd

load_dotenv()

RUN_ID = os.getenv('RUN_ID')

mlflow.set_tracking_uri("http://localhost:5000")

model_uri = f"runs:/{RUN_ID}/models_mlflow"
artifact_uri = f"mlflow-artifacts:/2/{RUN_ID}/artifacts/preprocessor/preprocessor.b"

# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(model_uri)


local_path = mlflow.artifacts.download_artifacts(artifact_uri=artifact_uri)

with open(local_path, "rb") as f:
    dv = pickle.load(f)


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    X = dv.transform([features])
    preds = model.predict(X)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)