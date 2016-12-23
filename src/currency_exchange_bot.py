from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from fixer import Fixer

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
    update.message.reply_text('Hi!')


def start(bot, update):
    print('request: start')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='I\'m a bot, please talk to me !')


def echo(bot, update):
    print('request: echo')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=update.message.text.replace(' ', '_'))


def caps(bot, update, args):
    print('request: caps')
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=text_caps)


def error(bot, update,error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def is_num(val):
    try:
        float(val)
        return True
    except:
        return False

def convert(bot, update, args):
    """
    request example: /convert 1000 usd to rub
    """
    args = args[:5] # prevent too long arg list
    try:
        amount = float(list(filter(lambda it: is_num(it), args))[0])
        cur_from, cur_to = list(filter(lambda it: it.upper()
            in Fixer._allowed_curr, args))[:2]
        cur_from = cur_from.upper()
        cur_to = cur_to.upper()
        resp = f.convert(cur_from, cur_to, amount)
        if resp:
            bot.sendMessage(chat_id=update.message.chat_id,
                text='{0} {1} is {2} {3}'.format(amount, cur_from,
                    resp, cur_to))
        else:
            raise Exception('No response from Fixer ')
    except:
        bot.sendMessage(chat_id=update.message.chat_id,
            text='I did not understand your request. :(')

def read_token(token_file='api.token'):
    with open(token_file) as f:
        return f.read().strip()


def main():
    updater = Updater(token=read_token())
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps, pass_args=True)
    dispatcher.add_handler(caps_handler)

    convert_handler = CommandHandler('convert', convert, pass_args=True)
    dispatcher.add_handler(convert_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    f = Fixer()
    main()
