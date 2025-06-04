import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

TOKEN = "8123151609:AAGPDRyCWsioC6A1OfU9It7OfSd4y87jbJo"

def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! لینک یوتیوب را بفرستید تا دانلود کنم.')

def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    chat_id = update.message.chat_id

    try:
        # تنظیمات yt-dlp
        ydl_opts = {
            'format': 'best',  # بهترین کیفیت
            'outtmpl': 'video.%(ext)s',  # نام فایل خروجی
            'quiet': True,  # عدم نمایش پیام‌های اضافی
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # ارسال ویدیو به کاربر
        context.bot.send_video(chat_id=chat_id, video=open(filename, 'rb'))
        
        # حذف فایل موقت
        os.remove(filename)
    except Exception as e:
        update.message.reply_text(f"خطا: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
