import requests
import logging
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '789345848:AAHo_L1jWfFbyhLpy7eUhfMCDzO4t3j4UPc'


def start(bot, update):
    update.message.reply_text('welcome MESSAGE')


def help(bot, update):
    update.message.reply_text('help message')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def generatePDF(bot, update, product):
	r = requests.post('https://survey.fast-insight.com/mcd/it/voucher.php', data={'browser':'undefined','browserLANG':'undefined','deviceAPP_ID':'undefined','deviceType':'undefined','identifier':'undefined','incentivetype':str(product),'IP':'undefined','lang':'it','orderpoint':'1','platform':'undefined','promo':'','store_id':'0123','surveyform':'1224','transaction':'undefined','version':'undefined'}, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}, cookies={'VOC_id':'de_5aa55c6a535c3'})
	return r.text.split("' download target='_blank'")[0].split("<a href='")[1]

if __name__ == '__main__':
	print('- MCDonalds Voucher Generator -\n@ created by TheFamilyTeam @\n- Join @TFChat -\n\n1) Cheeseburger\n2) Coffee\n')
	product = input('Select: ')
	print('+ Generating voucher...')
	print('+ Done: ' + generatePDF(product))
	input()
  
# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
