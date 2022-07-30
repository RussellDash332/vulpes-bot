from env import *
from telegram.ext import Updater, CommandHandler # MessageHandler, filters

def get_my_id(update, context):
    update.message.reply_text(update.message.from_user.id)

if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("get_my_id", get_my_id))

    updater.start_polling()
    print("++++++++++ STARTING BOT +++++++++++")
    updater.idle()
    print("++++++++++  KILLING BOT  ++++++++++")