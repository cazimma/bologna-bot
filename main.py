from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from pathlib import Path

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! This is a test message!")

if __name__ == '__main__':
    token = Path('token.txt').read_text()
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)

    application.run_polling()