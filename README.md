# TG-GPT - Telegram Bot with Chat and Payment

**Описание:**

TG-GPT - это Telegram-бот, предоставляющий пользователям возможности чата и приема платежей. Бот может быть использован для различных целей, таких как продажа услуг.

## Функциональность:

*   **Чат:** Возможность вести текстовые диалоги с ботом.
*   **Прием платежей:** Интеграция с платежной системой ЮMoney для приема платежей от пользователей.
*  **Управление аккаунтом:** Просмотр информации об аккаунте пользователя.
*   **Выбор роли:** Возможность выбора роли для бота.
*  **Очистка контекста:** Сброс истории чата.
*   **Настройки:** Выбор модели нейросети.

## Используемые библиотеки:

*   **pyTelegramBotAPI (Telebot):** Для создания Telegram-ботов.
*   **g4f:** Для доступа к различным языковым моделям (опционально, для использования AI в боте).
*   **python-dotenv:** Для управления конфигурационными параметрами из файла `.env`.
*   **yoomoney:** Для интеграции с платежной системой ЮMoney.

## Установка зависимостей:
```bash
pip install g4f python-dotenv pyTelegramBotAPI curl_cffi yoomoney
```

## Настройка и запуск:
1. • Создайте файл **.env** в корне проекта.
2. • Добавьте ваш токен Telegram бота, кошелька вашего yoomoney
```.env
TG-TOKEN = "Ваш токен, полученный от BotFather"
YOOMONEY-TOKEN = "Ваш токен, полученный из yoomoney"
RECIVER = "Ваш номер кошелька"
```
3. • Запустите бота:

## Настройка конфигов для оплаты и выбора нейросети:

* Изменить | Добавить | Убрать
1. Выбор нейросети --> config.py
```python
roles = {
  'default': {
      'name': 'default', 
      'tokens': 1500,    
      'requests': 100    
  },
  'Название':{
      'name': 'Название', # <-- Изменить название
      'tokens' 3500,      # <-- Изменить количество токенов
      'requests': 200,    # <-- Изменить максимальное количество запросов
      'price': 150,       # <-- Цена за модель нейросети
  }
}
```
2. Prompt для нейросети --> config.py
```python
prompts = {
    'Название': "Ваш промпт",
}
```
3. Модели для выбора --> config.py
```python
models = [g4f.models.gpt_35_turbo, g4f.models.gemini_pro, g4f.models.claude_3_haiku, g4f.models.gpt_4o, g4f.models.gpt_4_turbo] # <-- Можно добавить в список нейросети | Или изменить список под другую библиотеку с нейросетями
models = ["gpt-4o", "gpt-4", "gpt-4.1"] # <-- Пример для openai, но тогда следует изменить сам файл gpt.py
```

4. Изменить библиотеку для запросов нейросети
* Пример для OpenAi
```python
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def request(model, message: str, history: list, prompt: str, _try=0): # <--- Входные данные должны быть, как и в начальном виде
    if _try >= 3:
        return 'Извините возникла ошибка, измените запрос или попробуйте еще раз'
    try:
        _try += 1
        client = OpenAI(api_key=os.getenv("GPT-TOKEN")) # <--- Загрузить api key добавить в .env GPT-TOKEN = "Ваш токен от openai"

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "assistant", "content": ", ".join(history)},
                {"role": "user", "content": f"{prompt + message}.[на русском ответь]"}
            ],
        )
        return completion.choices[0].message.content # <--- Выходящий ответ должен быть ответ gpt : str
    except Exception as e:
        print(e)
        return request(model, message, history, prompt, _try)
```
* Пример для Gemini
```python
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

def request(model, message: str, history: list, prompt: str, _try): # <--- Входные данные должны быть, как и в начальном виде
    if _try >= 3:
        return 'Извините возникла ошибка, измените запрос или попробуйте еще раз'
    try:
        _try += 1
        full_prompt = "Твоя история: " + "\n ".join(history) + message + prompt
        genai.configure(api_key=os.getenv("GPT-TOKEN")) # <--- Загрузить api key добавить в .env GPT-TOKEN = "Ваш токен от gemini"

        model = genai.GenerativeModel('models/gemini-1.5-flash')

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        print(e)
        return request(model, message, history, prompt, _try)
```

## Пользовательские изменения:
* Вы можете добавлять свои собственные функции или изменения в код бота, редактируя файл bot.py и добавляя новые обработчики для команд Telegram.
* Новые команды для бота
```python
elif message.text == '/settings': # <-- Добавьте свобю команду
    bot.send_message(message.chat.id, "*Выберите тип модель ИИ*", parse_mode='Markdown', reply_markup=model_keyboard(models)) # <-- Обработчик событий
    return
```
## Команды бота:

*  **/start**- Запускает бота.
*  **/account** - Отображает информацию об аккаунте пользователя.
*  **/role** - Позволяет выбрать роль для бота. Влияет на стиль общения бота.
*  **/clear** - Очищает контекст (историю чата) бота.
*  **/payment** - Покупка платной версии нейросети.
*  **/settings** - Доступ к настройкам бота.

## Разработчик:

*  XTR1DE
*  Telegram: @XTR1DE
*  Email: xtreamd034@gmail.com
