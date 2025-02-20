# Breast Cancer Prediction System

## 🩺 Overview
The **Breast Cancer Prediction System** is a machine learning-based web application designed to predict whether a breast tumor is **benign** or **malignant**. It provides a user-friendly interface for patients to input their medical parameters and receive predictions based on a trained Logistic Regression model.

## 📌 Features
- **Predict Breast Cancer** using ML model
- **Save Patient Reports** with history tracking
- **Download Reports** as PDF files
- **View and Delete Reports** from the database
- **Probability Distribution Visualization**
- **Beautiful UI with Streamlit**

## 🚀 Tech Stack
### Frontend
- **Streamlit** (for the user interface)
- **Matplotlib** (for probability distribution charts)

### Backend
- **Flask** (REST API for prediction and database handling)
- **Flask-CORS** (to handle cross-origin requests)
- **SQLite** (to store patient reports)
- **Joblib** (for ML model serialization)
- **FPDF** (for generating downloadable reports)

## 🛠️ Installation Guide

### 🔹 Step 1: Clone the Repository
```bash
git clone https://github.com/Smohanty834/Breast-cancer-prediction.git
cd Breast-cancer-prediction
```

### 🔹 Step 2: Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate   # On MacOS/Linux
env\Scripts\activate      # On Windows
```

### 🔹 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 Step 4: Set Up the Database
```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 🔹 Step 5: Run the Backend Server
```bash
python app.py
```
The Flask server will start at **http://127.0.0.1:5000**.

### 🔹 Step 6: Run the Frontend Application
```bash
streamlit run app.py
```

The Streamlit UI will open in your default browser.

## 🎯 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | `POST` | Predicts breast cancer (Benign/Malignant) |
| `/save_report` | `POST` | Saves a patient report |
| `/get_reports` | `GET` | Retrieves all saved reports |
| `/delete_report/<id>` | `DELETE` | Deletes a specific report |
| `/delete_all_reports` | `DELETE` | Deletes all reports |
| `/download_report/<id>` | `GET` | Downloads a report as PDF |

## 📊 Example Usage (Prediction Request)
```json
{
  "features": [14.0, 20.0, 90.0, 600.0, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05, ...]
}
```
## Demo
<img src="https://github.com/user-attachments/assets/439dc0ea-b8bf-4afe-b971-52dc90ccdcc6" alt="Breast Cancer Prediction System" width="750" height="400">
<img src="https://github.com/user-attachments/assets/eb75a5b9-623d-4455-b77d-57dbcb96be65" alt="Breast Cancer Prediction System" width="750" height="400">

## 📄 Future Enhancements
- 🔹 **Doctor Consultation Feature**
- 🔹 **More Detailed Medical Recommendations**
- 🔹 **User Authentication & Admin Panel**
- 🔹 **Deploy on AWS/GCP**

## 🤝 Contributing
Feel free to fork the repository and submit pull requests.

---
⭐ **Star this repo if you find it useful!** ⭐

