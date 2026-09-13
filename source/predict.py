import joblib
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

from source.config import (
    MODEL_PATH,
    APPLICATION_MODEL_PATH,
    MODEL_FEATURES_PATH,
    RAW_FEATURES_PATH,
    CAT_FEATURES_PATH,
    THRESHOLD_PATH,
    HISTORY_PATH,
    DEFAULT_THRESHOLD,
)


# the main model: application data + credit history
model = CatBoostClassifier()
model.load_model(str(MODEL_PATH))

# the fallback model: application data only, for the clients that are not in the history table
application_model = CatBoostClassifier()
application_model.load_model(str(APPLICATION_MODEL_PATH))

model_features = joblib.load(MODEL_FEATURES_PATH)
raw_features = joblib.load(RAW_FEATURES_PATH)
cat_features = joblib.load(CAT_FEATURES_PATH)

if THRESHOLD_PATH.exists():
    threshold = joblib.load(THRESHOLD_PATH)
else:
    threshold = DEFAULT_THRESHOLD

# credit history aggregates of all the known clients, indexed by SK_ID_CURR
history_features = pd.read_parquet(HISTORY_PATH)

# a client without records in a history table has zero loans there, not an unknown number
HISTORY_COUNT_COLUMNS = [
    "BUREAU_COUNT",
    "BUREAU_ACTIVE_COUNT",
    "PREV_COUNT",
    "PREV_APPROVED_COUNT",
    "PREV_REFUSED_COUNT",
    "INS_COUNT",
    "INS_1Y_COUNT",
    "POS_MONTHS_COUNT",
    "CC_MONTHS_COUNT",
]


def add_history(x_input: pd.DataFrame, client_ids: pd.Series) -> pd.DataFrame:
    # the same steps as add_bureau / add_previous / add_installments / add_balances in the notebook
    known = client_ids.isin(history_features.index)

    # -1 is never found, so an unknown client gets an empty history
    history_rows = history_features.reindex(client_ids.where(known, -1).astype("int64"))
    history_rows.index = x_input.index

    x_input = x_input.join(history_rows)
    x_input[HISTORY_COUNT_COLUMNS] = x_input[HISTORY_COUNT_COLUMNS].fillna(0)

    x_input["BUREAU_DEBT_TO_INCOME"] = x_input["BUREAU_ACTIVE_DEBT_SUM"] / x_input["AMT_INCOME_TOTAL"]
    x_input["CURRENT_TO_PREV_CREDIT"] = x_input["AMT_CREDIT"] / x_input["PREV_APPROVED_AMT_CREDIT_MEAN"]
    x_input["INS_UNPAID_TO_INCOME"] = x_input["INS_PAYMENT_DIFF_SUM"] / x_input["AMT_INCOME_TOTAL"]

    return x_input.replace([np.inf, -np.inf], np.nan)


def prepare_dataframe(df_input: pd.DataFrame):
    missing_features = [
        feature for feature in raw_features
        if feature not in df_input.columns
    ]

    if missing_features:
        raise ValueError(
            "В данных не хватает признаков: "
            + ", ".join(missing_features[:20])
        )

    x_application = df_input[raw_features].copy()

    # the model gets the same types as in the notebook: text categories and numbers
    for col in raw_features:
        if col in cat_features:
            x_application[col] = x_application[col].fillna("Unknown").astype(str)
        else:
            x_application[col] = pd.to_numeric(x_application[col], errors="coerce")

    # SK_ID_CURR is not a feature, it is only used to find the credit history of the client
    if "SK_ID_CURR" in df_input.columns:
        client_ids = pd.to_numeric(df_input["SK_ID_CURR"], errors="coerce")
    else:
        client_ids = pd.Series(np.nan, index=df_input.index)

    history_found = client_ids.isin(history_features.index).to_numpy()

    x_full = add_history(x_application, client_ids)
    x_full = x_full.reindex(columns=model_features)

    return x_application, x_full, history_found


def predict_probability(x_application, x_full, history_found):
    # clients with a known credit history get the main model, the rest get the fallback model
    probabilities = application_model.predict_proba(x_application)[:, 1]

    if history_found.any():
        probabilities[history_found] = model.predict_proba(x_full[history_found])[:, 1]

    return probabilities


def predict(user_data: dict) -> str:
    df_input = pd.DataFrame([user_data])
    x_application, x_full, history_found = prepare_dataframe(df_input)

    probability = predict_probability(x_application, x_full, history_found)[0]
    prediction = int(probability >= threshold)

    label = (
        "Высокий риск дефолта"
        if prediction == 1
        else "Низкий риск дефолта"
    )

    model_text = (
        "основная, с кредитной историей"
        if history_found[0]
        else "резервная, только по анкете (кредитная история не найдена)"
    )

    return (
        f"Предсказание: {label}\n"
        f"Вероятность дефолта: {probability:.2%}\n"
        f"Порог отказа: {threshold:.1%}\n"
        f"Модель: {model_text}"
    )


def predict_dataframe(df_input: pd.DataFrame) -> pd.DataFrame:
    result_df = df_input.copy()

    x_application, x_full, history_found = prepare_dataframe(df_input)

    probabilities = predict_probability(x_application, x_full, history_found)
    predictions = (probabilities >= threshold).astype(int)

    result_df["PREDICTION"] = predictions
    result_df["DEFAULT_PROBABILITY"] = probabilities
    result_df["HISTORY_FOUND"] = history_found
    result_df["MODEL_USED"] = np.where(history_found, "full", "application")
    result_df["RISK_LABEL"] = result_df["PREDICTION"].map({
        0: "Низкий риск дефолта",
        1: "Высокий риск дефолта",
    })

    return result_df
