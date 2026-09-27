from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

_model = None
_label_encoder = None
_feature_names = None


def _load_artifacts():
    global _model, _label_encoder, _feature_names
    if _model is not None:
        return

    try:
        _model = joblib.load(MODELS / "xgb_burnout_model.pkl")
        _label_encoder = joblib.load(MODELS / "label_encoder.pkl")
        _feature_names = joblib.load(MODELS / "feature_names.pkl")
    except Exception as exc:  # noqa: BLE001 - surface install issues clearly in UI
        message = str(exc)
        if "libomp" in message or "XGBoost" in message or "OpenMP" in message:
            raise RuntimeError(
                "XGBoost could not load because OpenMP (libomp) is missing. "
                "Run: python scripts/setup_libomp.py"
            ) from exc
        raise


def predict_burnout(employee_data):
    _load_artifacts()

    employee_df = pd.DataFrame([employee_data])
    employee_df = employee_df[_feature_names]

    prediction = _model.predict(employee_df)[0]
    probabilities = _model.predict_proba(employee_df)[0]
    burnout_level = _label_encoder.inverse_transform([prediction])[0]
    confidence = float(probabilities.max())

    return burnout_level, confidence, probabilities
