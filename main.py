import logging
from telegram import Update
import telegram
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from selenium_stealth import stealth
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


def prepare_browser():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("start-maximized")
    # chrome_options.add_experimental_option(
    #     "excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    # stealth(driver,
    #         user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
    #         languages=["en-US", "en"],
    #         vendor="Google Inc.",
    #         platform="Win32",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=False,
    #         run_on_insecure_origins=False,
    #         )
    return driver


url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def url_validator(url):
    return re.match(url_regex, url) is not None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello "+name+".\nI'm a bot created by @NabidaM for downloading instagram contents, send me the link!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    isUrl = url_validator(text)
    if not isUrl:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a valid link!")
        return

    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=telegram.constants.ChatAction.TYPING)
        await update.message.reply_text(
            "Fetching Image...\nMake Sure Account is not Private !")

        imgLink = update.message.text + "?__a=1&__d=dis"
        chrome = prepare_browser()
        chrome.get(imgLink)
        logger.info(f"Attempting: {chrome.current_url}")
        if "login" in chrome.current_url:
            logger.info("Failed/ redir to login")
            chrome.quit()
        else:
            logger.info("Success")
            resp_body = chrome.find_element(By.TAG_NAME, "body").text
            data_json = json.loads(resp_body)
            logger.info(data_json)
            postImages = data_json['items'][0]['image_versions2']
            hdImage = postImages["candidates"][0]["url"]
        #     parse_data(username, user_data)
        #     chrome.quit()
        # with urllib.request.urlopen(imgLink) as url:
        #     data = url.read().decode()
        #     soup = BeautifulSoup(data, "html5lib")
        #     j = soup.find_all(class_="PolarisPhoto")
        #     logger.info(soup)
        #     logger.info(j)
        #     vLink = j.get('content')
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=hdImage)
    except Exception as error:
        await update.message.reply_text(str(error))


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
