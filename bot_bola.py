import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# --- SERVER UNTUK RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Bot Groq is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- KONFIGURASI ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY') # Pastikan nama variabel di Render diupdate

def load_prompt():
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        return file.read()

# Inisialisasi Groq
client = Groq(api_key=GROQ_API_KEY)
PROMPT_MASTER = load_prompt()

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "⚡ *Bot Groq Aktif & Logika v7.5 Dimuat*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_prediction(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Pemanggilan Llama 3 melalui Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": PROMPT_MASTER
                },
                {
                    "role": "user",
                    "content": message.text,
                }
            ],
            model="llama3-70b-8192", # Model terbaik untuk logika matematika
            temperature=0.2, # Rendah agar lebih fokus pada angka/data
        )
        
        response_text = chat_completion.choices[0].message.content
        bot.reply_to(message, response_text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
