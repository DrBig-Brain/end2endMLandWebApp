import os
import pickle
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import pandas as pd

load_dotenv()

# Support a test mode that avoids needing a running MLflow server / artifacts.
TEST_MODE = os.getenv('TEST_MODE', '0') == '1'
RUN_ID = os.getenv('RUN_ID')
LOCAL_MODEL_PATH = os.getenv('LOCAL_MODEL_PATH')
LOCAL_PREPROCESSOR = os.getenv('LOCAL_PREPROCESSOR')

if not TEST_MODE:
    import mlflow

    # If local model path is provided, load model & preprocessor from local files
    if LOCAL_MODEL_PATH:
        model = mlflow.pyfunc.load_model(LOCAL_MODEL_PATH)

        if LOCAL_PREPROCESSOR:
            preproc_path = LOCAL_PREPROCESSOR
        else:
            # Try to find a preprocessor in a sibling path relative to the model
            # (common layout: ../<run_id>/artifacts/preprocessor/preprocessor.b)
            preproc_path = None

        if preproc_path:
            with open(preproc_path, "rb") as f:
                dv = pickle.load(f)
        else:
            dv = None
    else:
        mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', "http://localhost:5000"))

        model_uri = f"runs:/{RUN_ID}/models_mlflow"
        artifact_uri = f"mlflow-artifacts:/2/{RUN_ID}/artifacts/preprocessor/preprocessor.b"

        # Try to load real model/artifacts from MLflow
        model = mlflow.pyfunc.load_model(model_uri)

        local_path = mlflow.artifacts.download_artifacts(artifact_uri=artifact_uri)

        with open(local_path, "rb") as f:
            dv = pickle.load(f)
else:
    # Minimal dummy preprocessor & model for local testing
    class DummyDV:
        def transform(self, rows):
            # Expect a list with single features dict
            r = rows[0]
            # Return a pandas DataFrame with only trip_distance
            return pd.DataFrame({"trip_distance": [r.get('trip_distance', 0)]})

    class DummyModel:
        def predict(self, X):
            # Return trip_distance as the prediction
            return X['trip_distance'].to_numpy()

    dv = DummyDV()
    model = DummyModel()


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