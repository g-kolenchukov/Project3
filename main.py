import logging
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from register import register, first_response, second_response, stop
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5362034738:AAGFJgDIRBDn4RyUwzZecugQF2kgzC_0NuQ'

last_count = 0
def start(update, context):
    update.message.reply_text(
        'Я бот-библиотекарь ver. 1.0.\n'
        'Умею создавать карточку ученика и редактировать её.\n'
        'Для получения доступных команд наберите /help')


def search(update, context):
    update.message.reply_text("Введите книгу которую вы хотите найти.")
    return 1


def search_kniga(update, context):
    con = sqlite3.connect("cards_bd.sqlite")
    cur = con.cursor()
    zapros_bd = """INSERT INTO cods(imya,familiya,parallel,klass) """
    zapros_bd += """VALUES("""
   # zapros_bd += """, """.join([f"'{key}'"
                               # for key in sp])
    zapros_bd += """)"""
    cur.execute(zapros_bd)
    con.commit()
    con.close()
    update.message.reply_text("Пока в разработке")


def get(update, context):
    update.message.reply_text("Пока в разработке")


def info(update, context):
    update.message.reply_text("Пока в разработке")


def redactor(update, context):
    update.message.reply_text(
        "Укажите полностью ")


def help(update, context):
    update.message.reply_text(
        '/register поможет тебе зарегистрироваться в системе;\n'
        # '/search поможет найти нужную тебе книгу в базе;\n'
        '/get подаст заявку на взятие книги;\n'
        '/info получение информации о своей карточке и о взятых книгах;\n'
        '/redactor поможет изменить неверную или недостоверную информацию в своей карточке;\n')


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    th_start = CommandHandler('start', start)
    th_get = CommandHandler('get', get)
    th_info = CommandHandler('info', info)
    th_redactor = CommandHandler('redactor', redactor)
    th_help = CommandHandler('help', help)
    conv_handler = ConversationHandler(
        # Точка входа в диалог. В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('register', register)],
        # Состояние внутри диалога. Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, first_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text & ~Filters.command, second_response)]
        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('search', search)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, search_kniga)]
        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler2)
    dp.add_handler(conv_handler)
    dp.add_handler(th_start)
    dp.add_handler(th_get)
    dp.add_handler(th_info)
    dp.add_handler(th_redactor)
    dp.add_handler(th_help)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
