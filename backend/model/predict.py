import joblib
import pandas as pd
import numpy as np
import os

model_dir = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(model_dir, 'trained_model.pkl'))
scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
encoder = joblib.load(os.path.join(model_dir, 'label_encoder.pkl'))
feature_columns = joblib.load(os.path.join(model_dir, 'feature_columns.pkl'))

def _prepare_features(features: dict) -> pd.DataFrame:
    row ={col: features.get(col, np.nan) for col in feature_columns}
    return pd.DataFrame([row], columns=feature_columns)

def classify(features: dict)-> dict:
    df_row = _prepare_features(features)
    scaled = scaler.transform(df_row)
    pred_encoded = model.predict(scaled)[0]
    label = encoder.inverse_transform([pred_encoded])[0]
    probabilities = model.predict_proba(scaled)[0]
    confidence = float(np.max(probabilities))
    is_attack = label.strip().upper() not in ('BENIGN', 'NORMAL')
    
    return {
        'label': label,
        'confidence': confidence,
        'is_attack': is_attack
    }
    
def classify_batch(features_rows: list[dict]) -> list[dict]:
    df_rows = pd.concat([_prepare_features(f) for f in features_rows], ignore_index=True)
    scaled = scaler.transform(df_rows)
    preds_encoded = model.predict(scaled)
    labels = encoder.inverse_transform(preds_encoded)
    probabilities = model.predict_proba(scaled)
    results = []
    for label, proba in zip(labels, probabilities):
        results.append({
            "label": label,
            "is_attack": label.strip().upper() not in ("BENIGN", "NORMAL"),
            "confidence": round(float(np.max(proba)), 4),
        })
    return results


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    dummy_batch = [
    {col: float(rng.uniform(0, 1000)) for col in feature_columns}
    for _ in range(5)
]
    result = classify_batch(dummy_batch)
    print(result)