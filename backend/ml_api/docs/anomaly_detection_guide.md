# 📘 Guide de Détection d'Anomalies & Génération de Rapports

## 🔍 Vue d'ensemble

Ce module fournit une détection avancée des anomalies dans les données chronologiques et la génération automatisée de rapports PDF.

---

## ⚙️ Fonctionnalités principales

- **Détection d’anomalies** avec Isolation Forest
- **Prétraitement automatique** des données temporelles
- **Scoring de sévérité** des anomalies (low, medium, high)
- **Visualisations interactives** via Plotly
- **Rapports PDF** professionnels avec ReportLab
- **API REST** pour la génération à la demande
- **Tests unitaires** avec Pytest

---

## 🧪 Exemple d’utilisation

### 1. Chargement des données

```python
import pandas as pd

df = pd.read_csv("data.csv")  # doit contenir une colonne 'date' et 'cashflow'
