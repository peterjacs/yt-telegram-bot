def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    try:
        ydl_opts = {
            'format': 'best',
            'geo_bypass': True,  # عبور از محدودیت منطقه‌ای
            'cookiefile': 'cookies.txt',  # اگر نیاز به لاگین دارید
            'ignoreerrors': True,
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise Exception("ویدیو در دسترس نیست یا حذف شده")
            
            filename = ydl.prepare_filename(info)
            context.bot.send_video(
                chat_id=update.message.chat_id,
                video=open(filename, 'rb'),
                supports_streaming=True
            )
            os.remove(filename)
            
    except Exception as e:
        update.message.reply_text(f"❌ خطا: {str(e)}\n\n"
                                "⚠️ ممکن است ویدیو:\n"
                                "- حذف شده باشد\n"
                                "- محدودیت منطقه‌ای داشته باشد\n"
                                "- نیاز به تایید سن داشته باشد")
