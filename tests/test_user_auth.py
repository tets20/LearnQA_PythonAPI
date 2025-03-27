import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    exclude_params = [
            ("no_cookie"),
            ("no_token")
    ]
    def setup_method(self):
        data = {'email': 'vinkotov@example.com',
                'password': '1234'
                }
        response1 = requests.post('https://playground.learnqa.ru/api/user/login',data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")


    def test_auth_user(self):

        response2 = requests.get(
            'https://playground.learnqa.ru/api/user/auth',
        headers={"x-csrf-token" : self.token},
        cookies={"auth_sid" : self.auth_sid})

        Assertions.assert_json_value_by_name(response2,
                                             "user_id",
                                             self.user_id_from_auth_method,
                                             "User id from auth method is not equal to user id from check"
                                             " method")

    @pytest.mark.parametrize('condition', exclude_params )
    def test_negative_auth_check(self, condition):
        data = {'email': 'vinkotov@example.com',
                'password': '1234'
                }
        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)
        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user_id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")

        if condition == "no_cookie":
            response2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                headers={"x-csrf-token": self.token})
        else:
            response2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2,
                                             "user_id",
                                             0,
                                             f"User is authorized with condition {condition}")
