import json

# Скрипт вывода текста второго сообщения
json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
try:
    print(json.loads(json_text)["messages"][1]["message"])
except KeyError as ke:
    print (f"Такого ключа нет {ke}")