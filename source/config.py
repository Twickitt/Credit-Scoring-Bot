from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "catboost_model.cbm"
# fallback model for the clients without a known credit history, application data only
APPLICATION_MODEL_PATH = BASE_DIR / "models" / "catboost_model_application.cbm"
MODEL_FEATURES_PATH = BASE_DIR / "models" / "model_features.joblib"
RAW_FEATURES_PATH = BASE_DIR / "models" / "raw_features.joblib"
CAT_FEATURES_PATH = BASE_DIR / "models" / "cat_features.joblib"
THRESHOLD_PATH = BASE_DIR / "models" / "threshold.joblib"

# credit history aggregates of all the clients, saved by the notebook (too big for git)
HISTORY_PATH = BASE_DIR / "data" / "history_features.parquet"

DEFAULT_THRESHOLD = 0.5
