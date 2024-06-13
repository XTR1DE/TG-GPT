import telebot
import time
from keyboards import role_keyboard, model_keyboard, buy_keyboard
from config import TG, prompts, models, roles
from database import create_base, change_info, info, update_data
from cfg_yoomoney import buy, check
from gpt import request


bot = telebot.TeleBot(TG)

keyboard = role_keyboard()
model_board = model_keyboard()


def info_message(message):
    if message.text in prompts:
        change_info(message.chat.id, 'change_prompt', message.text)
        bot.send_message(message.chat.id, f"Успешно изменен на - *{message.text}*", reply_markup=None)
        return

    elif message.text in [i.name for i in models]:
        change_info(message.chat.id, 'model', message.text)
        bot.send_message(message.chat.id, f'Модель вашей gpt - *{message.text}*', parse_mode='Markdown', reply_markup=None)
        return

    elif message.text == '/role':
        bot.send_message(message.chat.id, "Можете выбрать любую роль бота", reply_markup=keyboard)
        return

    elif message.text == '/clear':
        change_info(message.chat.id, "clear", "")
        bot.send_message(message.chat.id, "Контекст удален. По умолчанию бот в ответе учитывает ваш предыдущий вопрос и свой ответ на него.")
        return

    elif message.text == '/payment':
        if info(message.chat.id, "product") == '':
            bot.send_message(message.chat.id, "Выберите товар")
            return

        elif check(info(message.chat.id, 'labels')):
            change_info(message.chat.id, 'type', info(message.chat.id, 'product'))
            update_data(message.chat.id)
            bot.send_message(message.chat.id, f'Оплата успешно прошла, подписка {info(message.chat.id, "type")}')
            return

        else:
            bot.send_message(message.chat.id, f'Оплата не прошла. Если у вас возникли проблемы с оплатой, пожалуйста, свяжитесь с @xtr1de и мы постараемся помочь вам как можно скорее.')
            return

    elif message.text == '/settings':
        bot.send_message(message.chat.id, "*Список доступных gpt*\n"
                                          f"{',  '.join([i.name for i in models])}", parse_mode='Markdown', reply_markup=model_board)
        return

    elif message.text == '/account':
        bot.send_message(message.chat.id, f"Подписка *{info(message.chat.id, 'type')}*\n"
                         f"Модель GPT - *{info(message.chat.id, 'model')}* /settings\n"
                         f"Запросов GPT на неделю осталось *{info(message.chat.id, 'requests')}/{info(message.chat.id, 'max_requests')}*\n"
                         f"\n"
                         f"\n"
                         f"*Купили подписку, а она не изменилась?* /payment\n"
                         f"\n"
                         f"Подписка *medium* - *{roles['medium'].get('price')}rub*\n"
                         f"запросов на неделю *{roles['medium'].get('requests')}*\n"
                         f"\n"
                         f"Подписка *allinclusive* - *{roles['allinclusive'].get('price')}rub*\n "
                         f"запросов на неделю *{roles['allinclusive'].get('requests')}*\n"
                         f"\n"
                         f"*Выберите подписку. Если вы сначала выбрали одну подписку, а затем другую, то оплатите последнюю из выбранных вами подписок.*", parse_mode='Markdown', reply_markup=buy_keyboard(roles))
        return

    else:
        if info(message.chat.id, "requests") >= 1:
            bot.send_chat_action(message.chat.id, 'typing')
            resp = request(info(message.chat.id, "model"), message.text, info(message.chat.id, 'history'), info(message.chat.id, 'prompt'))
            change_info(message.chat.id, "add_history", {'role': 'assistant', 'content': resp})
            change_info(message.chat.id, "add_history", {'role': 'user', 'content': message.text})
            change_info(message.chat.id, '-request', "")
            bot.send_message(message.chat.id, resp, parse_mode="MarkdownV2")
        else:
            bot.send_message(message.chat.id, "У вас закончились запросы, чтобы купить подписку */account*", parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in roles:
        role_name = call.data
        url, label = buy(role_name)
        change_info(call.message.chat.id, 'product', role_name)
        change_info(call.message.chat.id, 'labels', str(label))
        bot.send_message(call.message.chat.id, f'Вы выбрали роль *"{role_name}"*. Оплатите *{roles[role_name]["price"]} рублей.*', parse_mode='Markdown', reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Оплатить', url=url)))


@bot.message_handler(content_types=['text'])
def handle_message(message):
    create_base(message)
    info_message(message)


def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e, '\n')
            time.sleep(5)
            print("Рестарт бота")


if __name__ == "__main__":
    main()