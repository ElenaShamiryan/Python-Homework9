from telebot import TeleBot
from telebot import types

bot = TeleBot("5647767531:AAE0w23XE-xXLPGK9LZgBBQD2poyDH0WW8E", parse_mode=None)


@bot.message_handler(commands=['start'])
def but_ts(message):
    murkup = types.InlineKeyboardMarkup(row_width=4) # создали онлайн клавиатуру
    button_1 = types.InlineKeyboardButton(text='Список телефонов', callback_data='id_1' ) # кнопка списка
    button_2 = types.InlineKeyboardButton(text='Скачать справочник', callback_data='id_2' ) # скачать справочник
    button_3 = types.InlineKeyboardButton(text='Добавить данные', callback_data='id_3' ) # добавить данные
    button_4 = types.InlineKeyboardButton(text='Поиск по фамилии', callback_data='id_4' ) # поиск по файлу
    murkup.add(button_1,button_2,button_3,button_4) # добавили кнопку в клавиатуру
    bot.send_message(message.chat.id, f'Привет,{message.from_user.first_name}! Добро пожаловать в телефоный справочник. Выберите действие.'
        , reply_markup = murkup) 
    

with open('phonebook.txt', 'r', encoding='utf-8') as st:
    data = st.read()

@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'id_1':
            bot.send_message(call.message.chat.id, data )
        elif call.data == 'id_2':
            doc = open('phonebook.txt', 'rb')
            bot.send_document(call.message.chat.id, document=doc)
        elif call.data == 'id_3':
            bot.send_message(call.message.chat.id, f'Добавьте ФИО и номер телефона')
            @bot.message_handler(content_types='text')
            def handle_text(message):
                doc = open('phonebook.txt', 'a', encoding='utf-8')
                doc.write("{imia}\n".format(imia=message.text))
        elif call.data == 'id_4':   
            bot.send_message(call.message.chat.id, 'Кто Вам нужен?')
            @bot.message_handler(content_types = ['text'])
            def search_data(message):
                search_value = message.text
                with open('phonebook.txt','r', encoding='utf-8') as file:
                    count = 0
                    for line in file:
                        if search_value in line:
                            bot.send_message(message.chat.id, f'Вы искали {line}')
                            count = count + 1
                    if count == 0:
                        bot.send_message(call.message.chat.id, f'Такого человека тут нет') 
bot.polling(non_stop=True)
