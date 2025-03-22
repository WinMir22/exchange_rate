import requests


async def get_exchange_rate(code: str) -> str:  # noqa
    answer = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    if answer.status_code == 200:
        answer = answer.json()
        answer = answer["Valute"][code]["Value"]
        return "На данный момент эта валюта составляет " + str(answer) + " рублей"
    return "Извините, вы ввели неправильный код"
