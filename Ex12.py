import requests

class TestFirstAPI:
    def test_headers_definition(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers.items())
        assert ('x-secret-homework-header','Some secret value') in list(response.headers.items()) ,\
            f"Хэдер пропал из списка: {response.headers.items()}"