import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

import random
import string

class TestUserRegister(BaseCase):
    exclude_params = [
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'email'}, 'password'),
        ({'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'email'}, 'username'),
        ({'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'email'}, 'firstName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'email'},'lastName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa'}, 'email')
    ]

    def test_user_create_sucessfully(self):
        data = self.prepare_registration_data()
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = requests.post('https://playground.learnqa.ru/api/user/',data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    # Тест создание пользователя с некорректным email - без символа @
    def test_create_user_without_post_symbol_in_email(self):
        invalid_email = "a.v.inanovexample.com"
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': invalid_email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/',data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format",\
            f"Invalid email format message -{response.content}- is not correct"

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_too_short_username(self):
        user_short_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': user_short_name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/',data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short",\
            f"Invalid username format message -{response.content}- is not correct"

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_too_long_username(self):
        user_long_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(251))
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': user_long_name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/',data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long",\
            f"Invalid username format message -{response.content}- is not correct"

    # Создание пользователя без указания одного из полей
    @pytest.mark.parametrize('data_without_some_param, param_name',exclude_params)
    def test_create_user_without_parameter(self,data_without_some_param,param_name):
        data = data_without_some_param
        response = requests.post('https://playground.learnqa.ru/api/user/',data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {param_name}",\
            f"Invalid parameter name message -{response.content}- is not correct"