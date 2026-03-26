import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# START
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.reply("🎬 Send a video link\n🎧 /mp3 <link> for audio")

# تحميل فيديو
@dp.message_handler()
async def download(msg: types.Message):
    url = msg.text

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        await msg.reply_document(open(file, 'rb'))

    except:
        await msg.reply("❌ Failed to download")

# تحويل MP3
@dp.message_handler(commands=['mp3'])
async def mp3(msg: types.Message):
    url = msg.get_args()

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info).replace(".webm", ".mp3")

        await msg.reply_audio(open(file, 'rb'))

    except:
        await msg.reply("❌ Failed to convert")

if __name__ == "__main__":
    executor.start_polling(dp)
