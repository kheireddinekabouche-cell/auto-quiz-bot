import os
import telebot
from faster_whisper import WhisperModel

# التأكد من وجود التوكن
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    print("خطأ: لم يتم العثور على TELEGRAM_BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# تشغيل الموديل
try:
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
except Exception as e:
    print(f"خطأ في تحميل الموديل: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا أعمل الآن. أرسل لي أي تسجيل صوتي وسأحلله لك.")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    try:
        bot.reply_to(message, "⏳ جاري التحليل... انتظر ثواني.")
        file_info = bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("audio.ogg", "wb") as f:
            f.write(downloaded_file)

        segments, _ = model.transcribe("audio.ogg")
        
        result = "✅ تم التحليل بنجاح:\n"
        for s in segments:
            result += f"🎤 نطقك: '{s.text}' في ثانية: {round(s.start, 2)}\n"
        
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ: {e}")

print("البوت بدأ العمل الآن...")
bot.infinity_polling()
