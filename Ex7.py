import requests

# Скрипты задания 7
# Объявляем переменные
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
list_of_methods = ["get", "post", "put", "delete", "head"]

# Делает http-запрос любого типа без параметра method
for method in list_of_methods[:4]:
    without_method_in_param = requests.request(method, url)
    print(f"1---> Метод - {method} без параметра и ответ {without_method_in_param.text}")

# Делает http-запрос не из списка. Например, HEAD
head_without_method_in_param = requests.request(list_of_methods[4], url)
print(f"2---> Метод - {list_of_methods[4]} без параметра и ответ {head_without_method_in_param.text}")

# Делает запрос с правильным значением method
for method in list_of_methods[:4]:
    param = {"method": method.upper()}
    if method == "get" :
        with_method_in_param = requests.request(method, url, params=param)
        # print(with_method_in_param.url)
        print(f"3---> Метод - {method} c параметром {param.get("method")} и ответ {with_method_in_param.text}")
    else:
        with_method_in_param = requests.request(method, url, data=param)
        # print(with_method_in_param.url)
        print(f"3---> Метод - {method} c параметром {param.get("method")} и ответ {with_method_in_param.text}")

#  С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method
for method in list_of_methods[:4]:
    if method == "get" :
        for method_param in list_of_methods[:4]:
            param = {"method": method_param.upper()}
            Get_method_with_others_params = requests.request(method, url, params=param)
            print(Get_method_with_others_params.url)
            print(f"4---> Метод - {method} c параметром {param.get("method")} и ответ {Get_method_with_others_params.text}")
    else:
        for method_param in list_of_methods[:4]:
            param = {"method": method_param.upper()}
            not_Get_method_with_others_params = requests.request(method, url, data=param)
            print(not_Get_method_with_others_params.url)
            print(f"4---> Метод - {method} c параметром {param.get("method")} и ответ {not_Get_method_with_others_params.text}")
