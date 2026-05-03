import os
import telebot
import google.generativeai as genai

# 1. KONFIGURASI API
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# FUNGSI UNTUK MEMBACA PROMPT DARI FILE TXT
def load_prompt():
    with open('prompt5.txt', 'r', encoding='utf-8') as file:
        return file.read()

# Inisialisasi Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Memuat instruksi dari prompt.txt
system_instructions = load_prompt()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instructions
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 2. HANDLER PESAN
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "📊 *Predictive Edge Ultra vAktif*\nKirim 'NEW MATCH: Tim A vs Tim B' untuk memulai."
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_prediction(message):
    try:
        # Memberikan efek "Bot sedang mengetik..." agar terlihat hidup
        bot.send_chat_action(message.chat.id, 'typing')
        
        chat = model.start_chat(history=[])
        response = chat.send_message(message.text)
        
        bot.reply_to(message, response.text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "❌ *Error:* Pastikan format input benar.", parse_mode='Markdown')

# 3. RUN BOT
if __name__ == "__main__":
    bot.infinity_polling()
