import telebot
from pytube import YouTube
import instaloader
import os
import time

TOKEN = "8209100928:AAFzFsG7bfBkt-rKG7ObE0UAQQuggq8llWY"

bot = telebot.TeleBot(TOKEN)

# Foydalanuvchi bandligini saqlash
user_busy = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Salom 👋\nYouTube yoki Instagram video link yuboring."
    )


@bot.message_handler(func=lambda message: True)
def download_video(message):

    chat_id = message.chat.id
    url = message.text.strip()

    # Agar foydalanuvchi band bo‘lsa
    if user_busy.get(chat_id, False):
        bot.send_message(chat_id, "⏳ Iltimos, avvalgi yuklash tugashini kuting.")
        return

    user_busy[chat_id] = True

    try:

        # ================= YOUTUBE =================
        if "youtube.com" in url or "youtu.be" in url:

            bot.send_message(chat_id, "📥 YouTube videoni yuklab olinmoqda...")

            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()

            stream.download(filename="video.mp4")

            time.sleep(3)

            with open("video.mp4", "rb") as video:
                bot.send_video(chat_id, video)

            os.remove("video.mp4")

        # ================= INSTAGRAM =================
        elif "instagram.com" in url:

            bot.send_message(chat_id, "📥 Instagram videoni yuklab olinmoqda...")

            L = instaloader.Instaloader(dirname_pattern=".")

            shortcode = url.split("/")[-2]

            post = instaloader.Post.from_shortcode(L.context, shortcode)

            L.download_post(post, target="insta")

            video_path = f"insta/{post.shortcode}.mp4"

            time.sleep(3)

            with open(video_path, "rb") as video:
                bot.send_video(chat_id, video)

            os.remove(video_path)

        else:
            bot.send_message(chat_id, "❌ Faqat YouTube yoki Instagram link yuboring.")

    except Exception as e:
        bot.send_message(chat_id, f"❌ Xatolik: {e}")

    user_busy[chat_id] = False


print("Bot ishga tushdi...")
bot.polling(none_stop=True)
