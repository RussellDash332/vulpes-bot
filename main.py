from env import SL_CHAT, PCT_CHAT, CLUSTER_CHAT, TOKEN
from telegram.ext import Updater, CommandHandler # MessageHandler, filters
import logging, requests, emoji, random
from datetime import datetime, timedelta
import pandas as pd

# def get_my_id(update, context):
#     update.message.reply_text(update.message.from_user.id)

# if __name__ == '__main__':
#     updater = Updater(token=TOKEN, use_context=True)
#     dp = updater.dispatcher

#     dp.add_handler(CommandHandler("get_my_id", get_my_id))

#     updater.start_polling()
#     print("++++++++++ STARTING BOT +++++++++++")
#     updater.idle()
#     print("++++++++++  KILLING BOT  ++++++++++")

def send_message(chat_id, message):
    print(requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={
        "chat_id": chat_id,
        "parse_mode": "Markdown",
        "text": emoji.emojize(message, use_aliases=True),
        "disable_web_page_preview": True,
    }).json())

def check_birthdays():
    df = pd.read_table('birthdays.tsv', sep='\t', names=['Room', 'Name', 'Major', 'Telegram', 'Bday'])
    df = df.dropna(axis=0)

    # Clean name
    df.Name = df.Name.apply(lambda x: x.strip())

    # Clean date
    df.Bday = df.Bday.apply(lambda x: datetime.strptime(str(x), r"%m/%d"))

    # Clean tele
    df.Telegram = df.Telegram.apply(lambda x: x if x[0] == '@' else '@' + x)

    now = datetime.now()
    now = datetime(year=1900, month=now.month, day=now.day)
    GRACE_DAYS = 0

    df_bd = df[abs(df.Bday - now) <= timedelta(days=GRACE_DAYS)]
    if df_bd.shape[0]: # if there is someone inside
        msg = "*PCT 9 Vulpes wishes*\n\n" + \
            f"{chr(10).join(list(map(' '.join, zip(df_bd.Name, df_bd.Telegram))))}" + \
            "\n\na *HAPPY BIRTHDAY!!*\n🦊🥳🎉"
        # Telegram underscore parsing issue
        msg = msg.replace("_", "\\_")
        send_message(SL_CHAT, msg)

if __name__ == '__main__':
    check_birthdays()