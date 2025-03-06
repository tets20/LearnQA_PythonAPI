import requests

respose = requests.get("https://playground.learnqa.ru/api/get_text")
print (respose.text)