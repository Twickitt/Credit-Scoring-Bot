from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "catboost_model.cbm"
MODEL_FEATURES_PATH = BASE_DIR / "models" / "model_features.joblib"
RAW_FEATURES_PATH = BASE_DIR / "models" / "raw_features.joblib"
THRESHOLD_PATH = BASE_DIR / "models" / "threshold.joblib"

DEFAULT_THRESHOLD = 0.5