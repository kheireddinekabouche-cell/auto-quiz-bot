import os
import telebot
from faster_whisper import WhisperModel

# جلب التوكن من الإعدادات التي وضعتها
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# تشغيل موديل Whisper (مجاني تماماً)
model = WhisperModel("tiny", device="cpu", compute_type="int8")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    bot.reply_to(message, "⏳ جاري سماع صوتك لتحديد وقت ظهور الإجابة...")
    
    # تحميل الصوت من تليجرام
    file_info = bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("input_audio.ogg", "wb") as f:
        f.write(downloaded_file)

    # تحليل الصوت واستخراج التوقيت
    segments, _ = model.transcribe("input_audio.ogg")
    
    report = "🎯 تم التحليل! إليك توقيت ظهور الإجابات بناءً على صوتك:\n\n"
    for s in segments:
        # هنا يتم تحديد الثانية بالضبط
        report += f"🔹 الكلمة: {s.text}\n⏱ تظهر في الثانية: {round(s.start, 2)}\n\n"
    
    bot.send_message(message.chat.id, report)

bot.polling()
