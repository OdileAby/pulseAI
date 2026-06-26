import pandas as pd
from scipy import stats
import numpy as np

def load_csv(filepath):
    """Load CSV and return dataframe."""
    df = pd.read_csv(filepath)
    return df

def get_numeric_columns(df):
    """Auto-detect numeric columns worth analyzing."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Filter out columns that look like IDs (all unique values)
    useful_cols = [
        col for col in numeric_cols
        if df[col].nunique() > 1 and not col.lower().endswith('id')
    ]
    return useful_cols

def detect_anomalies(df, columns, z_threshold=2.5):
    """Detect anomalies using z-score and % change."""
    anomalies = []

    for col in columns:
        series = df[col].dropna()

        # Z-score detection
        z_scores = np.abs(stats.zscore(series))
        z_anomaly_indices = series.index[z_scores > z_threshold].tolist()

        # % change detection (flags sudden spikes/drops)
        pct_change = series.pct_change().abs()
        pct_anomaly_indices = pct_change.index[pct_change > 0.5].tolist()

        # Combine both
        all_indices = list(set(z_anomaly_indices + pct_anomaly_indices))

        for idx in all_indices:
            z = round(float(np.abs(stats.zscore(series))[series.index.get_loc(idx)]), 2)
            pct = round(float(pct_change.get(idx, 0) * 100), 2)

            # Severity score: weighted combo of z-score and % change
            severity = round((z * 0.6) + (min(pct, 500) / 500 * 10 * 0.4), 2)

            anomalies.append({
                "column": col,
                "row": idx,
                "value": df[col][idx],
                "z_score": z,
                "pct_change": pct,
                "reason": "z-score" if idx in z_anomaly_indices else "sudden change",
                "severity": severity
            })

    # Sort by severity descending
    anomalies.sort(key=lambda x: x["severity"], reverse=True)

    return anomalies

def get_most_critical(anomalies):
    """Return the single most critical anomaly."""
    if not anomalies:
        return None
    return anomalies[0]