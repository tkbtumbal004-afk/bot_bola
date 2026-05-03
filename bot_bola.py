import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- SERVER MINI UNTUK RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Lucky and Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --------------------------------

# KONFIGURASI API
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def load_prompt():
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        return file.read()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=load_prompt()
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "📊 *Predictive Edge Ultra v5.1 Aktif*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_prediction(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        chat = model.start_chat(history=[])
        response = chat.send_message(message.text)
        bot.reply_to(message, response.text, parse_mode='Markdown')
    except Exception as e:
        # Menampilkan detail error asli ke Telegram untuk debug
        bot.reply_to(message, f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    keep_alive() # Menjalankan server mini agar Render senang
    bot.infinity_polling()
