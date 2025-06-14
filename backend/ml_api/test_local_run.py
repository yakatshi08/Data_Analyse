import pandas as pd
from app.ml.anomaly_detector import AdvancedAnomalyDetector
from app.services.pdf_generator import PDFReportGenerator

# Exemple de données simulées
df = pd.DataFrame([
    {"date": "2024-01-01", "cashflow": 105000},
    {"date": "2024-01-02", "cashflow": 98000},
    {"date": "2024-01-03", "cashflow": 250000},  # anomalie
])

# Détection d'anomalies
detector = AdvancedAnomalyDetector(contamination=0.05)
results = detector.detect_anomalies(
    data=df,
    feature_columns=["cashflow"],
    timestamp_column="date"
)

# Génération du rapport PDF
generator = PDFReportGenerator()
pdf = generator.generate_anomaly_report(
    anomaly_results=results,
    prediction_results=None,
    company_info={
        "name": "Ma société",
        "analysis_period": "2024-01-01 à 2024-01-03"
    }
)

# Sauvegarde du fichier
with open("rapport_anomalies.pdf", "wb") as f:
    f.write(pdf)

print("✅ Rapport généré : rapport_anomalies.pdf")

