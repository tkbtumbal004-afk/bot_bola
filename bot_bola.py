import os
import telebot
from google import genai  # Library baru sesuai requirements
from flask import Flask
from threading import Thread

# --- SERVER UNTUK RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- KONFIGURASI ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def load_prompt():
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        return file.read()

# Client SDK Baru
client = genai.Client(api_key=GEMINI_API_KEY)
PROMPT_MASTER = load_prompt()

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ *Bot Online & Logika v7.5 Dimuat*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_prediction(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Pemanggilan Model SDK v2
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            config={'system_instruction': PROMPT_MASTER},
            contents=message.text
        )
        
        bot.reply_to(message, response.text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
