import json
import requests
from config import moneypool


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = moneypool[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = moneypool[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://api.exchangerate.host/convert?from={base_key}&to={sym_key}')
        resp = json.loads(r.content)
        new_price = resp['result'] * float(amount)
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} к {sym} : {new_price}"
        return message


        # r = requests.get(f'https://api.exchangerate.host/convert?from={base_key}&to={sym_key}')
        # resp = json.loads(r.content)
        # new_price = resp['result'] * float(amount)

