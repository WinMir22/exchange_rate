import requests


async def get_exchange_rate(check_code: str, give_code: str) -> str:
    response = requests.get(
        f"https://cdn.jsdelivr.net/npm/@fawazahmed0/"
        f"currency-api@latest/v1/currencies/{check_code.lower()}.json"
    )
    if response.status_code == 200:
        data = response.json()
        rate = data.get(check_code.lower(), {}).get(give_code.lower(), '')
        return str(rate)
    return ''
