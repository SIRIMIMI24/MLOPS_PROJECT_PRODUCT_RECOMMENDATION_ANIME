# MLOS-PRODUCT-RECOMMENDATION-ANIME

A Hybrid Anime Recommendation System built with TensorFlow, Flask, and integrated with MLOps best practices including MLflow, DVC, Jenkins, and Docker.

## 🚀 Overview

This project implements a hybrid recommendation engine that combines collaborative filtering and content-based filtering to provide personalized anime recommendations. It features a complete end-to-end ML pipeline, from data ingestion to a production-ready Flask web application.

## 🛠️ Tech Stack

- **Machine Learning**: TensorFlow, Keras, Scikit-learn, XGBoost, LightGBM
- **Web Framework**: Flask
- **Data Processing**: Pandas, NumPy
- **MLOps & Tracking**: MLflow, DVC, Comet-ML
- **DevOps & CI/CD**: Jenkins, Docker, KaggleHub
- **Visualization**: Matplotlib, Seaborn

## 📂 Project Structure

```text
├── artifacts/             # Data and model artifacts (Raw, Processed, Weights)
├── config/                # Configuration files (YAML, Python configs)
├── custom_jenkins/        # Jenkins Dockerization setup
├── notebook/              # Experimental notebooks
├── pipeline/              # Training and Prediction pipelines
├── src/                   # Core source code (Ingestion, Processing, Training)
├── static/ & templates/   # Flask web assets
├── utils/                 # Helper functions
├── application.py         # Flask entry point
├── requirements.txt       # Project dependencies
└── setup.py               # Packaging configuration
```

## ⚙️ Setup & Installation

### 1. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -e .
```

### 3. Data Ingestion & Training
The project uses a structured pipeline for model training:
```bash
python -m src.model_training
```

### 4. Run the Web Application
```bash
python application.py
```
Visit `http://localhost:5000` in your browser.

## 🐳 Docker & CI/CD Setup

### Jenkins with Docker-in-Docker (DinD)
To set up the CI/CD environment using the provided `custom_jenkins` Dockerfile:

1. **Build the Jenkins image**:
   ```bash
   cd custom_jenkins
   docker build -t jenkins-dind .
   ```

2. **Run the container**:
   ```bash
   docker run -d --name jenkins-dind --privileged -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind
   ```

3. **Configure Python in Jenkins**:
   Exec into the container and install the necessary tools:
   ```bash
   docker exec -u root -it jenkins-dind bash
   apt update -y && apt install -y python3 python3-pip python3-venv
   ```

## 📊 MLOps Integration

- **MLflow**: Used for tracking experiments, parameters, and metrics.
- **DVC**: Handles data versioning for large datasets (`anime.csv`, etc.).
- **Artifacts**: Models and processed data are stored in the `artifacts/` directory for reproducibility.

## 🧪 Testing
Run the testing script to verify the installation:
```bash
python tester.py
```

---
*Developed as part of an MLOps Product Recommendation project.*
