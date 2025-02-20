from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import joblib
import numpy as np
from flask_cors import CORS
from fpdf import FPDF
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
CORS(app)

# Models
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    features = db.Column(db.String(500), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    probability = db.Column(db.String(100), nullable=False)

# Create all tables inside an application context
with app.app_context():
    db.create_all()

# Load model
loaded_model = joblib.load('LR_model.joblib')
feature_names = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
       'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se',
       'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst']

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = loaded_model.predict(features)[0]
    probability = loaded_model.predict_proba(features)[0].tolist()
    return jsonify({"prediction": "Malignant" if prediction == 1 else "Benign", "probability": probability}), 200

# Save report route
@app.route('/save_report', methods=['POST'])
def save_report():
    data = request.get_json()
    new_report = Report(
        name=data['name'],
        age=data['age'],
        features=str(data['features']),
        prediction=data['prediction'],
        probability=str(data['probability'])
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify({"message": "Report saved successfully"}), 200

# Get reports route
@app.route('/get_reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    reports_data = [[r.id, r.name, r.age, r.features, r.prediction, r.probability] for r in reports]
    return jsonify({"reports": reports_data}), 200

# Delete specific report route
@app.route('/delete_report/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    report = Report.query.get(report_id)
    if report:
        try:
            db.session.delete(report)
            db.session.commit()
            return jsonify({"message": "Report deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()  # FIX: Rollback in case of failure
            return jsonify({"message": f"Error deleting report: {str(e)}"}), 500
    return jsonify({"message": "Report not found"}), 404

# Delete all reports route
@app.route('/delete_all_reports', methods=['DELETE'])
def delete_all_reports():
    try:
        num_deleted = Report.query.delete()  # FIX: Use .query.delete() directly
        db.session.commit()
        return jsonify({"message": f"Deleted {num_deleted} reports successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500
@app.route('/download_report/<int:report_id>', methods=['GET'])
def generate_pdf(report_id):
    report = Report.query.get(report_id)
    if not report:
        return jsonify({"message": "Report not found"}), 404
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Breast Cancer Diagnosis Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Patient Information", ln=True, align='L')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 8, f"Name: {report.name}", ln=True)
    pdf.cell(200, 8, f"Age: {report.age}", ln=True)
    pdf.cell(200, 8, f"Prediction: {report.prediction}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Feature Analysis", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(200, 200, 200)  # Light gray background for header
    pdf.cell(100, 8, "Feature Name", border=1, align='C', fill=True)
    pdf.cell(80, 8, "Value", border=1, align='C', fill=True)
    pdf.ln()
    
    features = eval(report.features)  
    for i in range(len(feature_names)):
        pdf.cell(100, 8, f"{feature_names[i].replace('_', ' ').title()}", border=1)
        pdf.cell(80, 8, f"{float(features[i]):.4f}", border=1, align='C')
        pdf.ln()
    
    pdf_path = f"report_{report.id}.pdf"
    pdf.output(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)