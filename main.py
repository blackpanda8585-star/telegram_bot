import telebot
from pytube import YouTube
import instaloader
import os

TOKEN = "BU_YERGA_SIZNING_TOKEN"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! YouTube yoki Instagram link yuboring.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    if "youtube.com" in url or "youtu.be" in url:
        try:
            bot.send_message(message.chat.id, "YouTube videoni yuklab olinmoqda...")
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download(filename="video.mp4")
            video = open("video.mp4", "rb")
            bot.send_video(message.chat.id, video)
            video.close()
            os.remove("video.mp4")
        except Exception as e:
            bot.send_message(message.chat.id, f"Xatolik: {e}")

    elif "instagram.com" in url:
        try:
            bot.send_message(message.chat.id, "Instagram videoni yuklab olinmoqda...")
            L = instaloader.Instaloader(dirname_pattern=".")
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target="insta_video")
            video_path = os.path.join("insta_video", post.shortcode + ".mp4")
            video = open(video_path, "rb")
            bot.send_video(message.chat.id, video)
            video.close()
            os.remove(video_path)
        except Exception as e:
            bot.send_message(message.chat.id, f"Xatolik: {e}")
    else:
        bot.send_message(message.chat.id, "Faqat YouTube yoki Instagram link yuboring.")

bot.polling()
