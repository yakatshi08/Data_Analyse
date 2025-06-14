import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AdvancedAnomalyDetector:
    def __init__(self, contamination=0.1, n_estimators=100, max_samples='auto', random_state=42):
        self.contamination = contamination
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            max_samples=max_samples,
            random_state=random_state,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)

    def detect_anomalies(self, data: pd.DataFrame, feature_columns: List[str], timestamp_column: str = 'date') -> Dict[str, Any]:
        features = self._prepare_features(data, feature_columns, timestamp_column)
        features_scaled = self.scaler.fit_transform(features)
        predictions = self.isolation_forest.fit_predict(features_scaled)
        scores = self.isolation_forest.score_samples(features_scaled)
        anomalies = data[predictions == -1].copy()
        anomalies['anomaly_score'] = scores[predictions == -1]
        anomalies['severity'] = self._calculate_severity(scores[predictions == -1])
        visualizations = self._create_visualizations(data, anomalies, scores, feature_columns, timestamp_column)
        return {
            "anomalies": anomalies,
            "anomaly_rate": len(anomalies) / len(data),
            "visualizations": visualizations
        }

    def _prepare_features(self, data: pd.DataFrame, feature_columns: List[str], timestamp_column: str) -> pd.DataFrame:
        df = data[feature_columns].copy()
        if timestamp_column in data.columns:
            date_col = pd.to_datetime(data[timestamp_column])
            df["day_of_week"] = date_col.dt.dayofweek
            df["hour"] = date_col.dt.hour
        return df.fillna(df.median())

    def _calculate_severity(self, scores: np.ndarray) -> List[str]:
        norm_scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
        return ['low' if s < 0.33 else 'medium' if s < 0.66 else 'high' for s in norm_scores]

    def _create_visualizations(self, data, anomalies, scores, feature_columns, timestamp_column) -> Dict[str, str]:
        visualizations = {}
        try:
            if timestamp_column in data.columns and feature_columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data[timestamp_column],
                    y=data[feature_columns[0]],
                    mode='lines',
                    name='Normal Data'
                ))
                fig.add_trace(go.Scatter(
                    x=anomalies[timestamp_column],
                    y=anomalies[feature_columns[0]],
                    mode='markers',
                    name='Anomalies',
                    marker=dict(color='red', size=8, symbol='x')
                ))
                fig.update_layout(title="Anomalies sur la série temporelle")
                visualizations["temporal"] = fig.to_json()
        except Exception as e:
            logger.error(f"Erreur lors de la génération des visualisations: {e}")
        return visualizations
