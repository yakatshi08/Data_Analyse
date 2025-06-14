from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import io
import pandas as pd

from app.services.pdf_generator import PDFReportGenerator
from app.ml.anomaly_detector import AdvancedAnomalyDetector

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/generate-pdf")
def generate_pdf_report(data: List[dict]):
    """
    Génère un rapport PDF basé sur les données envoyées (JSON)
    """
    try:
        df = pd.DataFrame(data)

        detector = AdvancedAnomalyDetector()
        anomaly_results = detector.detect_anomalies(
            data=df,
            feature_columns=["cashflow"],
            timestamp_column="date"
        )

        generator = PDFReportGenerator()
        pdf_bytes = generator.generate_anomaly_report(
            anomaly_results=anomaly_results,
            prediction_results=None,
            company_info={
                "name": "Demo Corp",
                "analysis_period": f"{df['date'].min()} - {df['date'].max()}"
            }
        )

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=rapport_anomalie.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération du rapport : {str(e)}")
