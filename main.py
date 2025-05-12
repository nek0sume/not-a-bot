import telebot
from secrets import secrets
from answers import batteries, clothes, blood
from telebot import TeleBot, types
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters

token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)

class MyStates(StatesGroup):
    main_menu = State()
    batteries_district = State()
    clothes_district = State()
    blood_district = State()

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Батарейки")
    btn2 = types.KeyboardButton("Вещи")
    btn3 = types.KeyboardButton("Кровь")
    markup.add(btn1, btn2, btn3)
    bot.send_message(chat_id, "Выберите, что хотите сдать:", reply_markup=markup)
    bot.set_state(chat_id, MyStates.main_menu)

def show_district_menu1(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    districts = ["Заводский", "Центральный", "Рудничный", "Кировский", "Ленинский"]
    buttons = [types.KeyboardButton(district) for district in districts]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    bot.send_message(chat_id, "Выберите район:", reply_markup=markup)
    bot.set_state(chat_id, MyStates.batteries_district)

def show_district_menu2(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    districts = ["Заводский", "Центральный", "Рудничный", "Кировский", "Ленинский"]
    buttons = [types.KeyboardButton(district) for district in districts]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    bot.send_message(chat_id, "Приём вещей осуществляется через контейнеры 'Вещь во благо'. Выберите район:", reply_markup=markup)
    bot.set_state(chat_id, MyStates.clothes_district)

def show_district_menu3(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    districts = ["Заводский", "Центральный", "Рудничный", "Кировский", "Ленинский"]
    buttons = [types.KeyboardButton(district) for district in districts]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    bot.send_message(chat_id, "Выберите район:", reply_markup=markup)
    bot.set_state(chat_id, MyStates.blood_district)

@bot.message_handler(state=MyStates.main_menu)
def main_menu_handler1(message):
    if message.text == "Батарейки":
        show_district_menu1(message.chat.id)
    elif message.text == "Вещи":
        show_district_menu2(message.chat.id)
    elif message.text == "Кровь":
        show_district_menu3(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки")

@bot.message_handler(state=MyStates.batteries_district)
def district_handler1(message):
    if message.text == "Назад":
        show_main_menu(message.chat.id)
    elif message.text in batteries:
        addresses = batteries[message.text]
        response = f"📍 Пункты приёма батареек в районе {message.text}:\n\n" + "\n".join(addresses)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите район из списка")

@bot.message_handler(state=MyStates.clothes_district)
def district_handler2(message):
    if message.text == "Назад":
        show_main_menu(message.chat.id)
    elif message.text in clothes:
        addresses = clothes[message.text]
        response = f"📍 Пункты приёма вещей в районе {message.text}:\n\n" + "\n".join(addresses)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите район из списка")

@bot.message_handler(state=MyStates.blood_district)
def district_handler(message):
    if message.text == "Назад":
        show_main_menu(message.chat.id)
    elif message.text in blood:
        addresses = blood[message.text]
        response = f"📍 Пункты приёма крови в районе {message.text}:\n\n" + "\n".join(addresses)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите район из списка")

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message.chat.id)

if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.polling(none_stop=True)