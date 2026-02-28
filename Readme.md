# 🏠 End-to-End MLOps Project – House Price Prediction System

An industry-style end-to-end Machine Learning system built using:

- 🐍 Python (Anaconda)
- 📊 Scikit-learn
- 📈 MLflow (Experiment Tracking)
- 📉 Evidently AI (Monitoring & Drift Detection)
- ⚡ FastAPI (Model API)
- 🐳 Docker (Containerization)
- ☁️ AWS EC2 (Deployment)
- ⚛️ React (Frontend UI)

This project demonstrates the complete ML lifecycle — from training to production deployment.

---

# 🎯 Problem Statement

Build a production-ready ML system that predicts California house prices based on user-provided features.

---

# 📊 Dataset

California Housing Dataset  
Loaded via: sklearn.datasets.fetch_california_housing

Why this dataset?
- Clean and realistic
- Requires preprocessing
- Suitable for regression
- Perfect intermediate ML project

Target Variable:
- MedHouseVal

Key Features:
- MedInc (Median Income)
- HouseAge
- AveRooms
- AveBedrms
- Population
- AveOccup
- Latitude
- Longitude

---

# 🧠 System Architecture

React Frontend  
        ↓  
FastAPI Backend  
        ↓  
Scikit-learn Model (.pkl)  
        ↓  
Prediction Response  

MLflow → Tracks experiments  
Evidently → Monitors performance  
Docker → Containerizes app  
AWS EC2 → Hosts production API  

---

# 📁 Project Structure

house-price-mlops/
│
├── data/
├── notebooks/
│   └── eda.ipynb
│
├── src/
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── model.pkl
│
├── api/
│   ├── main.py
│   └── schema.py
│
├── monitoring/
│   └── evidently_report.py
│
├── frontend/
│   └── react-app/
│
├── Dockerfile
├── requirements.txt
└── README.md

---

# 🚀 Implementation Guide

---

## 1️⃣ Setup Environment (Anaconda)

conda create -n mlops python=3.10
conda activate mlops
pip install -r requirements.txt

---

## 2️⃣ Dataset Loading & EDA

Inside notebooks/eda.ipynb:

- Load dataset using fetch_california_housing
- Convert to pandas DataFrame
- Check missing values
- Perform correlation analysis
- Visualize distributions

---

## 3️⃣ Train Model (Scikit-learn)

File: src/train.py

Steps:
- Train/Test split
- Feature scaling (StandardScaler)
- Train models:
  - Linear Regression
  - Random Forest
  - Gradient Boosting
- Evaluate using RMSE and R²
- Save best model as model.pkl

Example snippet:

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

joblib.dump(model, "src/model.pkl")

---

## 4️⃣ Track Experiments with MLflow

Inside train.py:

- Log hyperparameters
- Log RMSE
- Log trained model

Run MLflow UI:

mlflow ui

Open:
http://localhost:5000

---

## 5️⃣ Model Monitoring with Evidently AI

File: monitoring/evidently_report.py

Generate:
- Data Drift Report
- Regression Performance Report

Output:
- HTML report stored in monitoring/

---

## 6️⃣ Build FastAPI Backend

File: api/main.py

Endpoints:

GET /
→ Health check

POST /predict
→ Accept JSON input and return prediction

Run locally:

uvicorn api.main:app --reload

Open:
http://127.0.0.1:8000/docs

---

## 7️⃣ Dockerize Application

Build image:

docker build -t house-price-api .

Run container:

docker run -p 8000:8000 house-price-api

---

## 8️⃣ Deploy on AWS EC2

Steps:

1. Launch Ubuntu EC2 instance
2. Install Docker
3. Clone repository
4. Build Docker image
5. Run container
6. Open port 8000 in security group

Access API:
http://<EC2-PUBLIC-IP>:8000/docs

---

## 9️⃣ Build React Frontend

Inside frontend/:

npm create vite@latest
npm install axios

Features:
- Form input fields for housing features
- Submit button
- Display predicted price
- Axios POST request to FastAPI backend

Example API call:

axios.post("http://<EC2-IP>:8000/predict", formData)

Enable CORS in FastAPI for frontend communication.

---

# 📦 Required Dependencies

scikit-learn  
pandas  
numpy  
mlflow  
evidently  
fastapi  
uvicorn  
joblib  

---

# ✅ Final Checklist

[ ] Environment setup complete  
[ ] Dataset explored  
[ ] Model trained  
[ ] MLflow tracking working  
[ ] Evidently reports generated  
[ ] FastAPI API running  
[ ] Docker image built  
[ ] AWS deployed successfully  
[ ] React UI connected  
[ ] End-to-end prediction working  

---

# 🎓 Learning Outcomes

✔ Full ML lifecycle  
✔ MLOps tools integration  
✔ API development  
✔ Docker containerization  
✔ AWS deployment  
✔ Frontend-backend integration  

---

# 🚀 Future Improvements

- CI/CD using GitHub Actions  
- Model versioning  
- Automated retraining pipeline  
- Kubernetes deployment  
- Cloud monitoring dashboard  

---

# 👨‍💻 Author

Built with discipline, curiosity, and controlled chaos.

