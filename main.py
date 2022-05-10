import logging
import csv
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from register import register, first_response, second_response
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5362034738:AAGFJgDIRBDn4RyUwzZecugQF2kgzC_0NuQ'


def start(update, context):
    global id
    id = update.message['chat']['id']
    update.message.reply_text(
        'Я бот-библиотекарь ver. 1.0.\n'
        'Умею создавать карточку ученика и редактировать её.\n'
        'Для получения доступных команд наберите /help')


def stop(update, context):
    update.message.reply_text("Действие отменено")
    return ConversationHandler.END


def get(update, context):
    update.message.reply_text(
        'Для получения какой-либо книги введите свой номер карточки')
    return 1


def get2(update, context):
    global number
    number = update.message.text
    try:
        number = int(number)
        con = sqlite3.connect("cards_bd.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM cods
                    WHERE number = {number}""").fetchall()
        con.close()
        print(result)
        update.message.reply_text(
            f'Номер: {result[0][0]}\nФамилия: {result[0][1]}\nИмя: {result[0][2]}\nПараллель: {result[0][3]}\nКласс: {result[0][4]}')
        update.message.reply_text('Это вы? Если это вы, наберите название книги которую вы хотите взять\n'
                                  'Если это не вы, наберите команду /stop')
    except:
        update.message.reply_text('Нужно ввести номер карточки числом без букв и пробелов')
    return 2


def get3(update, context):
    kniga = update.message.text
    try:
        con2 = sqlite3.connect("cards_bd.sqlite")
        cur = con2.cursor()
        result2 = cur.execute(f"""SELECT * FROM knigi WHERE nazvanie = '{kniga}'""").fetchall()
        con2.close()
        if result2 == []:
            update.message.reply_text(
                f'Такой книги в библиотеке пока нет, либо вы ввели название неправильно или не полностью')
        else:
            con = sqlite3.connect("cards_bd.sqlite")
            cur = con.cursor()
            ms = cur.execute(f"""SELECT knigi FROM cods
                                WHERE number = {number}""").fetchall()[0][0]
            ms = ms.split(';')
            if result2[0][0] in ms:
                update.message.reply_text('Такая книга уже была вам выдана')
            else:
                msg = ''
                msg += 'На вас оформлена книга:\n'
                msg += result2[0][0]
                msg += f', автор: {result2[0][1]}'
                update.message.reply_text(f'{msg}')
                ms.append(result2[0][0])
                ms = ';'.join(ms)
                uqe = f"""UPDATE cods SET knigi = '{ms}' WHERE number = {number}"""
                cur.execute(uqe)
                con.commit()
                con.close()
    except:
        update.message.reply_text('Нужно ввести название книги')
    return ConversationHandler.END


def info(update, context):
    with open('ids.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            i = int(row[0])
            if int(update.message['chat']['id']) == i:
                global number
                number = row[1]
                con = sqlite3.connect("cards_bd.sqlite")
                cur = con.cursor()
                result = cur.execute(f"""SELECT * FROM cods
                                    WHERE number = {number}""").fetchall()
                con.close()
                print(result)
                update.message.reply_text(
                    f'Номер: {result[0][0]}\nФамилия: {result[0][1]}\nИмя: {result[0][2]}\nПараллель: {result[0][3]}\nКласс: {result[0][4]}')
                if result[0][5] == None:
                    update.message.reply_text(
                        f'Взятых книг у вас пока нет, но вы можете это исправить:)')
                else:
                    msg = ''
                    sp = result[0][5].split(';')
                    print(sp)
                    msg += 'Взятые вами книги:\n'
                    for i in range(len(sp)):
                        msg += (f'{i + 1}. {sp[i]}\n')
                    update.message.reply_text(f'{msg}')
            return ConversationHandler.END
    update.message.reply_text(
        "Для получения информации о карточке введите свой номер\n"
        'Он был дан вам при регистрации')
    return 1


def info2(update, context):
    number = update.message.text
    try:
        number = int(number)
        con = sqlite3.connect("cards_bd.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM cods
                    WHERE number = {number}""").fetchall()
        con.close()
        print(result)
        update.message.reply_text(
            f'Номер: {result[0][0]}\nФамилия: {result[0][1]}\nИмя: {result[0][2]}\nПараллель: {result[0][3]}\nКласс: {result[0][4]}')
        if result[0][5] == None:
            update.message.reply_text(
            f'Взятых книг у вас пока нет, но вы можете это исправить:)')
        else:
            msg = ''
            sp = result[0][5].split(';')
            print(sp)
            msg += 'Взятые вами книги:\n'
            for i in range(len(sp)):
                msg += (f'{i + 1}. {sp[i]}\n')
            update.message.reply_text(f'{msg}')
    except:
        update.message.reply_text('Нужно ввести номер карточки числом без букв и пробелов')
    return ConversationHandler.END


def redactor(update, context):
    with open('ids.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            i = int(row[0])
            if int(update.message['chat']['id']) == i:
                global NUM
                NUM = row[1]
    update.message.reply_text(
        "Для редактирования карточки введите её номер")
    return 1


def redactor2(update, context):
    if NUM:
        number = NUM
    else:
        number = update.message.text
    print(number)
    try:
        number = int(number)
        con = sqlite3.connect("cards_bd.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM cods
                        WHERE number = {number}""").fetchall()
        con.close()
        print(result)
        update.message.reply_text(
            f'Номер: {result[0][0]}\nФамилия: {result[0][1]}\nИмя: {result[0][2]}\nПараллель: {result[0][3]}\nКласс: {result[0][4]}')
        update.message.reply_text(
            'Введите полностью правильную информацию в вашу карточку по образцу\n'
            'ФАМИЛИЯ ИМЯ НОМЕР_ПАРРАЛЕЛИ БУКВА_КЛАССА')
        carda = update.message.text
        carda.split(' ')
        try:
            con = sqlite3.connect("cards_bd.sqlite")
            cur = con.cursor()
            que = cur.execute(f"""UPDATE cods SET (familiya, imya, parallel, klass) = {carda[0]}, {carda[1]}, {carda[2]}, {carda[3]} WHERE number = {number}""")
            cur.execute(que)
            con.commit()
            con.close()
        except:
            update.message.reply_text(
                'Введите полностью правильную информацию в вашу карточку по образцу\n'
                'ФАМИЛИЯ ИМЯ НОМЕР_ПАРРАЛЕЛИ БУКВА_КЛАССА')
    except:
        update.message.reply_text('Нужно ввести номер карточки числом без букв и пробелов')
    return ConversationHandler.END

def help(update, context):
    update.message.reply_text(
        '/register поможет тебе зарегистрироваться в системе;\n'
        '/get подаст заявку на взятие книги;\n'
        '/info получение информации о своей карточке и о взятых книгах;\n'
        '/redactor поможет изменить неверную или недостоверную информацию в своей карточке;\n')


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    obych = MessageHandler(Filters.text & ~Filters.command, help)
    th_start = CommandHandler('start', start)
    th_redactor = CommandHandler('redactor', redactor)
    th_help = CommandHandler('help', help)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, first_response)],
            2: [MessageHandler(Filters.text & ~Filters.command, second_response)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('get', get)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, get2)],
            2: [MessageHandler(Filters.text & ~Filters.command, get3)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler3 = ConversationHandler(
        entry_points=[CommandHandler('info', info)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, info2, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler4 = ConversationHandler(
        entry_points=[CommandHandler('redactor', redactor)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, redactor2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler4)
    dp.add_handler(conv_handler3)
    dp.add_handler(conv_handler2)
    dp.add_handler(conv_handler)
    dp.add_handler(obych)
    dp.add_handler(th_start)
    dp.add_handler(th_redactor)
    dp.add_handler(th_help)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
