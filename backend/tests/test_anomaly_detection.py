import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from app.ml.anomaly_detector import AdvancedAnomalyDetector

@pytest.fixture
def sample_data():
    """Génère un DataFrame avec des anomalies injectées"""
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    values = 100000 + np.random.normal(0, 5000, size=100)

    # Injecter des anomalies positives et négatives
    values[20] = values[20] * 3
    values[50] = values[50] * 0.2
    values[75] = values[75] * 5

    return pd.DataFrame({
        "date": dates,
        "cashflow": values
    })

def test_detect_anomalies(sample_data):
    """Test de détection basique avec Isolation Forest"""
    detector = AdvancedAnomalyDetector(contamination=0.05)
    results = detector.detect_anomalies(
        data=sample_data,
        feature_columns=["cashflow"],
        timestamp_column="date"
    )

    assert "anomalies" in results
    assert not results["anomalies"].empty
    assert results["anomaly_rate"] > 0
    assert "severity" in results["anomalies"].columns
    assert "visualizations" in results
