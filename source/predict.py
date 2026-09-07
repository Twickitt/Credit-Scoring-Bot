import joblib
import pandas as pd
from catboost import CatBoostClassifier

from source.config import (
    MODEL_PATH,
    MODEL_FEATURES_PATH,
    RAW_FEATURES_PATH,
    THRESHOLD_PATH,
    DEFAULT_THRESHOLD,
)


model = CatBoostClassifier()
model.load_model(str(MODEL_PATH))

model_features = joblib.load(MODEL_FEATURES_PATH)
raw_features = joblib.load(RAW_FEATURES_PATH)

if THRESHOLD_PATH.exists():
    threshold = joblib.load(THRESHOLD_PATH)
else:
    threshold = DEFAULT_THRESHOLD


def prepare_dataframe(df_input: pd.DataFrame) -> pd.DataFrame:
    if "TARGET" in df_input.columns:
        df_input = df_input.drop("TARGET", axis=1)

    missing_features = [
        feature for feature in raw_features
        if feature not in df_input.columns
    ]

    if missing_features:
        raise ValueError(
            "В данных не хватает признаков: "
            + ", ".join(missing_features[:20])
        )

    df_input = df_input.reindex(columns=raw_features)

    df_input = pd.get_dummies(df_input, drop_first=True)

    df_input = df_input.reindex(columns=model_features, fill_value=0)

    return df_input


def predict(user_data: dict) -> str:
    df_input = pd.DataFrame([user_data])
    x_input = prepare_dataframe(df_input)

    probability = model.predict_proba(x_input)[0][1]
    prediction = int(probability >= threshold)

    label = (
        "Высокий риск дефолта"
        if prediction == 1
        else "Низкий риск дефолта"
    )

    return (
        f"Предсказание: {label}\n"
        f"Вероятность дефолта: {probability:.2%}\n"
        f"Используемый порог: {threshold:.2f}"
    )


def predict_dataframe(df_input: pd.DataFrame) -> pd.DataFrame:
    result_df = df_input.copy()

    x_input = prepare_dataframe(df_input)

    probabilities = model.predict_proba(x_input)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    result_df["PREDICTION"] = predictions
    result_df["DEFAULT_PROBABILITY"] = probabilities
    result_df["RISK_LABEL"] = result_df["PREDICTION"].map({
        0: "Низкий риск дефолта",
        1: "Высокий риск дефолта",
    })

    return result_df