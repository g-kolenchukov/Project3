import logging
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def register(update, context):
    update.message.reply_text(
        "Для регистрации карточки ученика введите имя и фамилию.\n"
        "Вы можете прервать регистрацию, послав команду /stop.")
    return 1


def first_response(update, context):
    global sp
    imya_familiya = update.message.text
    sp = imya_familiya.split(' ')
    if len(sp) < 2:
        update.message.reply_text('Введи имя и фамилию через пробел')
    else:
        for i in range(len(sp)):
            sp[i] = sp[i].capitalize()
        imya_familiya = ' '.join(sp)
        update.message.reply_text(
            f"{imya_familiya} в каком классе вы учитесь?\n"
            'Введите параллель и букву своего класса через пробел')
        return 2


def second_response(update, context):
    klass = update.message.text
    klass = klass.split()
    if len(klass) < 2:
        update.message.reply_text('Введи параллель числом и букву класса через пробел')
    else:
        for i in range(len(klass)):
            if i == 0:
                try:
                    klass[i] = int(klass[i])
                except ValueError:
                    update.message.reply_text('Введи параллель числом и букву класса через пробел')
                    return
            sp.append(klass[i])
        print(sp)
        logger.info(klass)
        con = sqlite3.connect("cards_bd.sqlite")
        cur = con.cursor()
        zapros_bd = """INSERT INTO cods(imya,familiya,parallel,klass) """
        zapros_bd += """VALUES("""
        zapros_bd += """, """.join([f"'{key}'"
                                    for key in sp])
        zapros_bd += """)"""
        cur.execute(zapros_bd)
        con.commit()
        con.close()
        update.message.reply_text("Карточка успешно зарегистрирована")
        return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Действие отменено")
    return ConversationHandler.END


