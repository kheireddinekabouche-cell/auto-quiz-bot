import os
import telebot
try:
    from faster_whisper import WhisperModel
    print("✅ المكتبات تعمل بنجاح")
except ImportError as e:
    print(f"❌ خطأ في المكتبات: {e}")

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# تحميل موديل صغير جداً ليناسب سرعة GitHub المجاني
model = WhisperModel("tiny", device="cpu", compute_type="int8")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت يعمل الآن! أرسل لي المقطع الصوتي.")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    bot.reply_to(message, "⏳ جاري المعالجة...")
    file_info = bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("input.ogg", "wb") as f:
        f.write(downloaded_file)
    
    segments, _ = model.transcribe("input.ogg")
    response = "🎯 التوقيتات المستخرجة:\n"
    for s in segments:
        response += f"🔹 {s.text} (في الثانية: {round(s.start, 2)})\n"
    bot.send_message(message.chat.id, response)

print("🚀 بدأ تشغيل البوت...")
bot.infinity_polling()
