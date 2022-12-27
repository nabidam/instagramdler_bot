import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
import os
from dotenv import load_dotenv
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

token = os.getenv('TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello "+name+".\nI'm a bot created by @NabidaM for downloading instagram contents, send me the link!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()