from telegram.ext import Updater
from telegram.ext import CommandHandler


# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
#

# updater = Updater(token=TOKEN)
# dispatcher = updater.dispatcher
#
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
# updater.start_polling()

import telegram

bot = telegram.Bot(token=TOKEN)
bot.send_message(chat_id=chat_id, text="I'm a bot,")


