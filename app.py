
import json
import os
from flask import Flask
from threading import Thread
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '8113432636:AAHFjz9XtWA2Rn9GYjsB6t4z7fbfQmHBQ1c'
OWNER_ID = 262011432

TEAMS_FILE = 'teams.json'
MATCHES_FILE = 'matches.json'
USERS_FILE = 'users.json'
ADMINS_FILE = 'admins.json'

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات فعال است!"

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_admin(user_id):
    admins = load_data(ADMINS_FILE).get("admins", [])
    return user_id == OWNER_ID or user_id in admins

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton("لیست تیم‌ها", callback_data='show_teams')]]
    await update.message.reply_text("سلام! به ربات پیش‌بینی خوش آمدید ⚽️", reply_markup=InlineKeyboardMarkup(buttons))

async def add_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(context.args) != 1:
        await update.message.reply_text("مثال: /addteam استقلال")
        return
    team = context.args[0]
    data = load_data(TEAMS_FILE)
    if team in data:
        await update.message.reply_text("این تیم قبلاً وجود دارد.")
    else:
        data[team] = {"players": []}
        save_data(TEAMS_FILE, data)
        await update.message.reply_text(f"تیم {team} اضافه شد.")

async def show_teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data(TEAMS_FILE)
    teams = '\n'.join(data.keys())
    await update.message.reply_text(f"لیست تیم‌ها:\n{teams}")

def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler('start', start))
    app_telegram.add_handler(CommandHandler('addteam', add_team))
    app_telegram.add_handler(CommandHandler('teams', show_teams))
    app_telegram.run_polling()

if __name__ == '__main__':
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
