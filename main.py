import os
import subprocess
import logging

from telegram import Update, File, InputFile
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackContext, ContextTypes
from pathlib import Path

# Configuration
VIDEO_PATH = "./videos/received_video.mp4"
OUTPUT_PATH = "./videos/processed_video.mp4"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Log all incoming messages (raw log)
# async def log_message(update: Update, context: CallbackContext) -> None:
#     user = update.effective_user
#     message = update.effective_message
#     raw_data = update.to_dict()  # Get raw message data
#     logging.info(f"Raw Message Data: {raw_data}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! This bot apply a mask to your video. The upload limit is 20 MB for now.")

# Video handler
async def handle_video(update: Update, context: CallbackContext) -> None:
    # raw_data = update.to_dict()  # Get raw message data
    # logging.info(f"Raw Message Data from handle_video: {raw_data}")
    
    video = update.message.video

    # Check if file size exceeds limit
    file_size_mb = video.file_size / (1024 * 1024)  # Convert to MB
    if file_size_mb > 20:
        await update.message.reply_text("The video is too large (max 20 MB).")
        return
    
    # logging.info(f"video_id: {video_id}")
    video_file = await context.bot.get_file(video.file_id)
    await video_file.download_to_drive(VIDEO_PATH)
    await update.message.reply_text("Video received! Processing...")

    # Execute ffmpeg script
    try:
        subprocess.run(["ffmpeg", "-i", VIDEO_PATH, "-vf", "scale=480:854", OUTPUT_PATH], check=True)
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(OUTPUT_PATH, 'rb'))
    except subprocess.CalledProcessError:
        await update.message.reply_text("Processing failed.")
    # finally:
    #     os.remove(VIDEO_PATH)
    #     if os.path.exists(OUTPUT_PATH):
    #         os.remove(OUTPUT_PATH)

if __name__ == '__main__':
    token = Path('token.txt').read_text()
    application = ApplicationBuilder().token(token).build()
    

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.ALL, handle_video))
    # application.add_handler(MessageHandler(filters.ALL, log_message))  # Log all messages   
    
    application.run_polling()