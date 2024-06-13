import telebot
from config import prompts, models


def role_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    for role in prompts.keys():
        keyboard.row(telebot.types.KeyboardButton(f"{role}"))
    return keyboard


def model_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    for role in [i.name for i in models]:
        keyboard.row(telebot.types.KeyboardButton(f"{role}"))
    return keyboard


def buy_keyboard(roles):
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = []
    for role in roles.values():
        if role.get('name') != 'default':
            buttons.append(telebot.types.InlineKeyboardButton(role.get('name'), callback_data=role.get('name')))
    keyboard.add(*buttons)
    return keyboard