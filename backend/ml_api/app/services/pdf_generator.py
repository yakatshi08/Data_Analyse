from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
from typing import Dict, Any, Optional
import io
import pandas as pd


class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()

    def generate_anomaly_report(
        self,
        anomaly_results: Dict[str, Any],
        prediction_results: Optional[Dict[str, Any]],
        company_info: Dict[str, str],
        output_path: Optional[str] = None
    ) -> bytes:
        buffer = output_path if output_path else io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        story.append(Paragraph("📄 Rapport d'Analyse d'Anomalies", self.styles['Title']))
        story.append(Spacer(1, 12))

        # Info entreprise
        story.append(Paragraph(f"Entreprise : {company_info.get('name', 'N/A')}", self.styles['Normal']))
        story.append(Paragraph(f"Période : {company_info.get('analysis_period', 'N/A')}", self.styles['Normal']))
        story.append(Paragraph(f"Date du rapport : {datetime.now().strftime('%d/%m/%Y')}", self.styles['Normal']))
        story.append(Spacer(1, 12))

        # Résumé Anomalies
        story.append(Paragraph("🔍 Résumé des anomalies détectées :", self.styles['Heading2']))
        total = anomaly_results.get('anomalies', pd.DataFrame()).shape[0]
        rate = anomaly_results.get('anomaly_rate', 0)
        story.append(Paragraph(f"- Nombre total d'anomalies : <b>{total}</b>", self.styles['Normal']))
        story.append(Paragraph(f"- Taux d'anomalies détectées : <b>{rate*100:.2f}%</b>", self.styles['Normal']))
        story.append(Spacer(1, 12))

        # Tableau des anomalies
        anomalies = anomaly_results.get('anomalies')
        if anomalies is not None and not anomalies.empty:
            story.append(Paragraph("📊 Détail des anomalies :", self.styles['Heading2']))
            table_data = [["Date", "Valeur", "Score", "Sévérité"]]
            for _, row in anomalies.iterrows():
                table_data.append([
                    str(row.get("date", "")),
                    f"{row.get('cashflow', 0):,.2f}",
                    f"{row.get('anomaly_score', 0):.4f}",
                    row.get("severity", "")
                ])

            table = Table(table_data, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("Aucune anomalie détectée.", self.styles['Normal']))

        doc.build(story)

        if output_path:
            return b''
        else:
            return buffer.getvalue()
