# 🚕 End-to-End Streaming MLOps System – NYC Taxi Fare Prediction

A production-grade Machine Learning system that predicts taxi fares using real-world streaming data.

This project demonstrates:
- Batch + Streaming pipelines
- Automated retraining
- Model monitoring
- Cloud-native deployment

---

# 🧠 Tech Stack

## Machine Learning
- Python
- Scikit-learn
- Pandas, NumPy
- MLflow (Experiment Tracking)
- Evidently AI (Monitoring & Drift Detection)

## Backend & APIs
- FastAPI
- Pydantic

## Streaming & Cloud
- AWS Kinesis (Data Streaming)
- AWS Lambda (Real-time processing)
- AWS S3 (Data + Model Storage)

## Infrastructure
- Terraform (Infrastructure as Code)
- Docker (Containerization)

## Frontend
- React + Axios

---

# 🎯 Problem Statement

Predict **NYC taxi fare amount** based on:

- Pickup & Drop coordinates
- Passenger count
- Time features (hour, day, month)

---

# 📊 Dataset

NYC Taxi Trip Records  
(Updated monthly)

Why this dataset?
- Real-world streaming data
- Time-dependent patterns
- Ideal for drift detection & retraining pipelines

---

# 🧠 System Architecture

## 🔹 Real-Time Prediction Flow

User (React)
   ↓
FastAPI (AWS EC2)
   ↓
ML Model (latest version)
   ↓
Prediction Response

---

## 🔹 Streaming Data Pipeline

Taxi Data Stream
   ↓
AWS Kinesis
   ↓
AWS Lambda (preprocessing)
   ↓
S3 Bucket (raw + processed data)

---

## 🔹 Training Pipeline

S3 (new data)
   ↓
Training Script (EC2 / Scheduled)
   ↓
MLflow (experiment tracking)
   ↓
Model Registry
   ↓
Deploy new model

---

## 🔹 Monitoring

Evidently AI:
- Data Drift Detection
- Model Performance Monitoring

---

# 📁 Project Structure

taxi-mlops/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── pipeline/
│   ├── ingest.py
│   ├── preprocess.py
│   ├── train.py
│   ├── retrain_pipeline.py
│
├── api/
│   └── main.py
│
├── lambda/
│   └── handler.py
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── monitoring/
│   └── evidently_report.py
│
├── models/
│   └── latest_model.pkl
│
├── frontend/
│   └── react-app/
│
├── Dockerfile
├── requirements.txt
└── README.md

---

# 🚀 Step-by-Step Implementation

---

## 1️⃣ Setup Environment

conda create -n mlops python=3.10  
conda activate mlops  
pip install -r requirements.txt  

---

## 2️⃣ Data Ingestion (Batch)

- Download NYC taxi dataset (monthly)
- Store in local or S3 bucket

---

## 3️⃣ Streaming Setup (AWS Kinesis)

- Create Kinesis Data Stream
- Configure shard count
- Send taxi events (JSON format)

---

## 4️⃣ Lambda Processing

- Trigger Lambda from Kinesis
- Parse incoming data
- Clean & transform features
- Store processed data in S3

File: lambda/handler.py

---

## 5️⃣ Data Storage (S3)

Buckets:
- raw-data/
- processed-data/
- models/

---

## 6️⃣ Model Training

File: pipeline/train.py

Steps:
- Load processed data
- Feature engineering
- Train model (Random Forest / XGBoost)
- Evaluate (RMSE)
- Save model

---

## 7️⃣ MLflow Integration

- Track parameters
- Track metrics
- Store model artifacts

Run:
mlflow ui

---

## 8️⃣ Retraining Pipeline

File: pipeline/retrain_pipeline.py

Steps:
1. Load new monthly data from S3
2. Merge with historical data
3. Train new model
4. Compare with old model
5. Replace if improved

---

## 9️⃣ Model Monitoring (Evidently AI)

File: monitoring/evidently_report.py

Generate:
- Data drift report
- Prediction performance report

Output:
HTML reports

---

## 🔟 FastAPI Backend

File: api/main.py

Endpoints:

GET /
→ Health check

POST /predict
→ Returns taxi fare prediction

Run:
uvicorn api.main:app --reload

---

## 1️⃣1️⃣ Dockerization

Build image:
docker build -t taxi-ml-api .

Run container:
docker run -p 8000:8000 taxi-ml-api

---

## 1️⃣2️⃣ Terraform Infrastructure

Inside terraform/:

Initialize:
terraform init

Plan:
terraform plan

Apply:
terraform apply

Resources created:
- Kinesis Stream
- Lambda Function
- S3 Buckets
- IAM Roles

---

## 1️⃣3️⃣ AWS Deployment

- Launch EC2 instance
- Install Docker
- Pull project repo
- Run container
- Open port 8000

---

## 1️⃣4️⃣ React Frontend

Setup:
npm create vite@latest  
npm install axios  

Features:
- Input form (trip details)
- API call to FastAPI
- Display predicted fare

Example:
axios.post("http://<EC2-IP>:8000/predict", data)

---

# 🔁 Automation (Monthly Retraining)

Use cron job:

crontab -e

0 0 1 * * python pipeline/retrain_pipeline.py

---

# 📦 Required Dependencies

scikit-learn  
pandas  
numpy  
mlflow  
evidently  
fastapi  
uvicorn  
boto3  
joblib  

---

# ✅ Final Checklist

[ ] Kinesis stream working  
[ ] Lambda processing data  
[ ] Data stored in S3  
[ ] Model trained  
[ ] MLflow tracking enabled  
[ ] Evidently reports generated  
[ ] FastAPI API deployed  
[ ] Docker container running  
[ ] Terraform infra created  
[ ] React frontend connected  
[ ] End-to-end pipeline working  

---

# 🎓 Learning Outcomes

✔ Streaming ML pipelines  
✔ MLOps with AWS  
✔ Infrastructure as Code (Terraform)  
✔ Real-time + batch processing  
✔ Model monitoring & retraining  
✔ Full-stack ML deployment  

---

# 🚀 Future Improvements

- CI/CD pipeline (GitHub Actions)
- Kubernetes deployment
- Feature store integration
- Real-time inference via Lambda
- Model version rollback

---

# 👨‍💻 Author

Built with ambition, curiosity, and late-night debugging.
