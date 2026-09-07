import json
import os
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from source.predict import predict, predict_dataframe, raw_features

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("BOT_TOKEN")

TMP_DIR = BASE_DIR / "tmp"
TMP_DIR.mkdir(exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я ML-бот для оценки кредитного риска.\n\n"
        "Можно отправить:\n"
        "1. JSON с данными одного клиента.\n"
        "2. CSV-файл с несколькими клиентами.\n\n"
        "Команды:\n"
        "/help — инструкция\n"
        "/features — список признаков"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Формат JSON:\n\n"
        "{\n"
        '  "AMT_INCOME_TOTAL": 202500.0,\n'
        '  "AMT_CREDIT": 406597.5,\n'
        '  "CODE_GENDER": "M"\n'
        "}\n\n"
        "Также можно отправить CSV-файл с исходными признаками клиента.\n"
        "Если в CSV есть колонка TARGET, она будет проигнорирована."
    )


async def features_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Модель ожидает признаки:\n\n" + "\n".join(raw_features)

    if len(text) > 3900:
        text = text[:3900] + "\n..."

    await update.message.reply_text(text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data = json.loads(update.message.text)

        if not isinstance(user_data, dict):
            await update.message.reply_text("Ошибка: нужно отправить JSON-объект.")
            return

        result = predict(user_data)
        await update.message.reply_text(result)

    except json.JSONDecodeError:
        await update.message.reply_text(
            "Не получилось прочитать JSON.\n"
            "Можно отправить данные текстом в JSON-формате или загрузить CSV."
        )

    except Exception as error:
        await update.message.reply_text(
            f"Ошибка при предсказании:\n{error}"
        )


async def handle_csv_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        document = update.message.document

        if not document.file_name.lower().endswith(".csv"):
            await update.message.reply_text("Отправь файл именно в формате CSV.")
            return

        await update.message.reply_text("Файл получен. Считаю риски...")

        tg_file = await document.get_file()

        input_path = TMP_DIR / "input_clients.csv"
        output_path = TMP_DIR / "clients_predictions.csv"

        await tg_file.download_to_drive(str(input_path))

        df_input = pd.read_csv(input_path)
        result_df = predict_dataframe(df_input)

        result_df.to_csv(output_path, index=False)

        total_count = len(result_df)
        high_risk_count = int((result_df["PREDICTION"] == 1).sum())
        low_risk_count = int((result_df["PREDICTION"] == 0).sum())
        avg_probability = result_df["DEFAULT_PROBABILITY"].mean()

        summary = (
            f"Готово. Обработано строк: {total_count}\n"
            f"Низкий риск: {low_risk_count}\n"
            f"Высокий риск: {high_risk_count}\n"
            f"Средняя вероятность дефолта: {avg_probability:.2%}"
        )

        await update.message.reply_text(summary)

        with open(output_path, "rb") as file:
            await update.message.reply_document(
                document=file,
                filename="clients_predictions.csv",
                caption="CSV с предсказаниями",
            )

    except Exception as error:
        await update.message.reply_text(
            f"Ошибка при обработке CSV:\n{error}"
        )


def main():
    if TOKEN is None:
        raise RuntimeError(
            "BOT_TOKEN не найден. Создай .env или задай переменную окружения."
        )

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("features", features_command))

    app.add_handler(MessageHandler(filters.Document.FileExtension("csv"), handle_csv_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()