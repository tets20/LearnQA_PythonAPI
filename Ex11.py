import requests

class TestFirstAPI:
    def test_cookie_definition(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        print(response.cookies.items())
        assert list(response.cookies.items()) == [('HomeWork', 'hw_value')], \
            f"Куки стало другое - {response.cookies.items()}"