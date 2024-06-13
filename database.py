import json
from config import roles, models


def create_base(message):
    try:
        data = json.load(open('info.json', encoding='utf8'))
        for i in data["personal"]:
            if message.chat.id == i['id']:
                return

        data['personal'].append(
            {
                'id': message.chat.id,
                'username': message.chat.username,
                'language': message.from_user.language_code,
                'type': roles['default'].get('name'),
                'model': str(models[0].name),
                'prompt': 'default',
                'max_tokens': roles['default'].get('tokens'),
                'tokens': roles['default'].get('tokens'),
                'max_requests': roles['default'].get('requests'),
                'requests': roles['default'].get('requests'),
                'labels': "",
                'product': '',
                'history': []
            }
        )
        with open('info.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    except FileNotFoundError:
        return print("Нет файла")
    except Exception as e:
        return print(e)


def info(id: int, _type: str):
    try:
        data = json.load(open('info.json', encoding='utf8'))
        _info = data["personal"]
        for item in _info:
            if item['id'] == id:
                information = item.get(_type)
                if information is not None:
                    return information
                else:
                    raise KeyError(f"Ключ {_type} не найден")

    except FileNotFoundError:
        return print("Нет файла")
    except Exception as e:
        return print(e)


def change_info(id: int, _type: str, message):
    try:
        data = json.load(open('info.json', encoding='utf8'))
        for i in data["personal"]:
            if i["id"] == id:
                if _type in ['type', 'prompt', 'model', 'labels', 'product']:
                    i[_type] = message
                elif _type in ['requests', 'max_requests', 'tokens', 'max_tokens']:
                    i[_type] = int(message)
                elif _type == 'clear':
                    i['history'] = []
                elif _type == 'add_history':
                    i['history'].append(message)
                elif _type == '-request':
                    i['requests'] = i['requests'] - 1
        with open('info.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    except FileNotFoundError:
        print("Файл info.json не найден")

    except json.JSONDecodeError:
        print("Ошибка декодирования JSON")

    except Exception as e:
        print(f"Ошибка: {e}")


def update_data(id=0):
    if id != 0:
        role = info(id, 'type')
        change_info(id, 'requests', roles[role].get('requests'))
        change_info(id, 'max_requests', roles[role].get('requests'))
        change_info(id, 'tokens', roles[role].get('tokens'))
        change_info(id, 'max_tokens', roles[role].get('tokens'))
        change_info(id, 'product', '')
        change_info(id, 'labels', '')
    else:
        try:
            data = json.load(open('info.json', encoding='utf8'))
            for user in data['personal']:
                role = user['type']
                user['requests'] = roles[role].get('requests')
                user['max_requests'] = roles[role].get('requests')
                user['tokens'] = roles[role].get('tokens')
                user['max_tokens'] = roles[role].get('tokens')
                user['product'] = ''
                user['labels'] = ''
            with open('info.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except FileNotFoundError:
            print("Файл info.json не найден")


if __name__ == "__main__":
    print(info(5560736206, 'username'))