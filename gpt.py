import g4f
from g4f import Provider
from config import gpt_provider, prompts


def request(model, message: str, history: list, prompt: str, _try=0):
    if _try >= 3:
        return 'Извините возникла ошибка, измените запрос или попробуйте еще раз'
    try:
        _try += 1

        response = g4f.ChatCompletion.create(
            model=model,
            provider=gpt_provider,
            messages= history + [
                {"role": "assistant", "content": prompts[prompt]},
                {"role": "user", "content": f"{message}.[на русском ответь]"},
            ],
        )
        content = response.split("$@$")[2] if gpt_provider == g4f.Provider.Blackbox else response

        for i in "*_~[]()<>#+-=|.!{}":  #telegram reserve for MarkdownV2
            content = content.replace(i, "\{}".format(i))

        return content

    except Exception as e:
        return request(model, message, history, prompt, _try)