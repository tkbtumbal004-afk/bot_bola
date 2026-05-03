import os
import telebot
from google import genai
from flask import Flask
from threading import Thread

# --- SERVER MINI UNTUK RENDER (ANTI-SLEEP) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Active!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- KONFIGURASI API ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def load_prompt():
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        return file.read()

# Inisialisasi Client Baru (Library google-genai)
client = genai.Client(api_key=GEMINI_API_KEY)
PROMPT_MASTER = load_prompt()

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "📊 *Predictive Edge Ultra v7.5 Universal Aktif*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_prediction(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Menggunakan model gemini-2.0-flash (terbaru & tercepat)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            config={'system_instruction': PROMPT_MASTER},
            contents=message.text
        )
        
        bot.reply_to(message, response.text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ *Error Detail:* {str(e)}", parse_mode='Markdown')

if __name__ == "__main__":
    keep_alive()
    print("Bot is polling...")
    bot.infinity_polling()
