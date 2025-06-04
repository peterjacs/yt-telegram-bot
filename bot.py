import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube

# توکن بات تلگرام را اینجا قرار دهید (از @BotFather گرفته‌اید)
TOKEN = "8123151609:AAGPDRyCWsioC6A1OfU9It7OfSd4y87jbJo"

def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! لینک یوتیوب رو بفرست تا برات دانلود کنم.')

def download_video(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    url = update.message.text

    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()  # بهترین کیفیت
        video.download(filename='video.mp4')
        
        # ارسال ویدیو به کاربر
        context.bot.send_video(chat_id=chat_id, video=open('video.mp4', 'rb'))
        
        # حذف فایل موقت
        os.remove('video.mp4')
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
