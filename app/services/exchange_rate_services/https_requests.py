import requests


async def get_exchange_rate(check_code: str, give_code: str) -> str:  # noqa
    answer = requests.get(
        f"https://cdn.jsdelivr.net/npm/@fawazahmed0/"
        f"currency-api@latest/v1/currencies/{check_code.lower()}.json"
    )
    if answer.status_code == 200:
        answer = answer.json()
        answer = answer[check_code.lower()][give_code.lower()]
        return answer
