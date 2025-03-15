import requests

 # Скрипт расчета редиреекта из ответа
response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(f"Количество редиректов - {len(response.history)}")
print(f"Конечный адрес - {response.url}")