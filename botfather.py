from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing in your .env file")

# Function to fetch evil advice from your API
def fetch_advice():
    try:
        headers = {"X-API-Key": os.getenv("API_KEY")}
        res = requests.get("http://localhost:8000/evil-advice/random", headers=headers)
        res.raise_for_status()
        data = res.json()
        return data["evil_advice"]["text"]
    except Exception as e:
        print(f"❌ Error fetching advice: {e}")
        return "⚠️ Couldn't reach advice server."

def fetch_categories():
    headers = {"X-API-Key": os.getenv("API_KEY")}
    res = requests.get("http://localhost:8000/categories", headers=headers)
    res.raise_for_status()
    return res.json()["categories"]

def fetch_category_advice(category=None):
    url = "http://localhost:8000/evil-advice/random"
    if category:
        url += f"?category={category}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()["evil_advice"]["text"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👿 Welcome to Evil Advice Bot!\n\n"
        "Type /advice or press the button to get a devilishly bad suggestion!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎲 Get Evil Advice", callback_data="get_advice")]
        ])
    )

async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = fetch_advice()
        await update.message.reply_text(
            f"🧠 Evil Advice:\n{text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎲 Another one!", callback_data="get_advice")]
            ])
        )
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("⚠️ Couldn't fetch advice. Try again later!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_advice":
        try:
            text = fetch_advice()
            await query.edit_message_text(
                f"🧠 Evil Advice:\n{text}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎲 Another one!", callback_data="get_advice")]
                ])
            )
        except Exception as e:
            print(f"Error: {e}")
            await query.edit_message_text("⚠️ Couldn't fetch advice. Try again later!")

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cats = fetch_categories()
        keyboard = [
            [InlineKeyboardButton(cat.title(), callback_data=f"category_{cat}")]
            for cat in cats
        ]
        await update.message.reply_text(
            "🎯 Choose a category:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(e)
        await update.message.reply_text("⚠️ Couldn't load categories.")

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("category_"):
        category = query.data.split("_", 1)[1]
        try:
            text = fetch_category_advice(category)
            await query.edit_message_text(
                f"📂 Category: *{category.title()}*\n\n🧠 Evil Advice:\n{text}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎲 Another one!", callback_data=f"category_{category}")]
                ])
            )
        except Exception as e:
            print(e)
            await query.edit_message_text("⚠️ No advice found for this category.")

import logging
logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("advice", advice))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler("categories", categories))
app.add_handler(CallbackQueryHandler(category_callback, pattern=r"^category_"))

if __name__ == "__main__":
    print("🤖 Evil Advice Bot is running")
    app.run_polling()
