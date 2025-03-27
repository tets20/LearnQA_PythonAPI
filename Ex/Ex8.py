import json
import time
import requests

# Создаем задачу и получаем по ней фактуру с токеном и таймингом
start_job = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
resp_1 = json.loads(start_job.text)
token = {list(resp_1.items())[0]}
timing = resp_1.get("seconds")

# Делаем один запрос с токеном до того, как задача готова
chek_job_status_before = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)

# Убеждаемся в правильности поля status и ждем тайминг по джобе
resp_2= json.loads(chek_job_status_before.text)
status1_job = resp_2.get("status")
if status1_job == "Job is NOT ready": print(f"Статус правильный - {status1_job}, ждем {timing} c и проверяем статус снова"); time.sleep(timing)

# Делаем запрос c token ПОСЛЕ того, как задача готова
chek_job_status_after = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)

# Убеждаемся в правильности поля status и наличии поля result
resp_3= json.loads(chek_job_status_after.text)
status2_job = resp_3.get("status")
if status2_job == "Job is ready" and "result" in resp_3: print(f"Теперь статус джобы - {status2_job} и поле result в наличии")


