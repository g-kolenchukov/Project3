import logging
import csv
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler




def register(update, context):
    update.message.reply_text(
        "Для регистрации карточки ученика введите фамилию и имя.\n"
        "Вы можете прервать регистрацию, послав команду /stop.")
    return 1


def first_response(update, context):
    with open('ids.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['first_name'], row['last_name'])
    #if update.message['chat']['id'] in expensive:
        #print('Похоже вы уже регистрировались в системе, отредактировать данные можно с помощью /redactor') \
        #return ConversationHandler.END
    # else:
        global sp
        imya_familiya = update.message.text
        sp = imya_familiya.split(' ')
        if len(sp) < 2:
            update.message.reply_text('Введи фамилию и имя через пробел')
        else:
            for i in range(len(sp)):
                sp[i] = sp[i].capitalize()
            imya_familiya = ' '.join(sp)
            update.message.reply_text(
                f"{imya_familiya} в каком классе вы учитесь?\n"
                'Введите параллель и букву своего класса через пробел')
            return 2


def second_response(update, context):
    f = open("knigi.txt", 'r')
    count = int(f.readline())
    f.close()
    sp.append(count)
    count += 1
    print(count)
    f = open("knigi.txt", 'w')
    f.write(str(count))
    f.close()
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
            elif i == 1:
                klass[i] = klass[i].capitalize()
            sp.append(klass[i])
        print(sp)
        con = sqlite3.connect("cards_bd.sqlite")
        cur = con.cursor()
        zapros_bd = """INSERT INTO cods(number,imya,familiya,parallel,klass) """
        zapros_bd += """VALUES("""
        zapros_bd += """, """.join([f"'{sp[2]}'", f"'{sp[1]}'", f"'{sp[0]}'", f"'{sp[3]}'", f"'{sp[4]}'"])
        zapros_bd += """)"""
        cur.execute(zapros_bd)
        con.commit()
        con.close()
        update.message.reply_text(f"Карточка успешно зарегистрирована под номером {sp[2]}")
        return ConversationHandler.END

