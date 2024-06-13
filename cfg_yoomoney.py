from yoomoney import Quickpay, Client
from config import YOOMONEY, roles, reciver
from uuid import uuid4

client = Client(YOOMONEY)


def buy(name: str):
    sum1, label1 = roles[name].get('price'), uuid4()

    quickpay = Quickpay(
        receiver=reciver,
        quickpay_form="shop",
        targets="Покупка пакета",
        paymentType='SB',
        sum=sum1,
        label=str(label1)
    )
    print(quickpay.sum, quickpay.label)
    return [quickpay.redirected_url, quickpay.label]


def check(labels):
    history = client.operation_history(label=labels)
    for oper in history.operations:
        if oper.status == 'success':
            return True
    return False