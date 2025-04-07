import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    # Попытка удалить пользователя по ID 2
    def test_delete_protected_user(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        user_id = 2
        response2 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid})


        Assertions.assert_code_status(response2, 400)
        assert '"Please, do not delete test users with ID 1, 2, 3, 4 or 5."' in response2.content.decode("utf-8"), \
            f"Invalid  message -{response2.content}"


    # Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID
    # и убедиться, что пользователь действительно удален
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post('https://playground.learnqa.ru/api/user/login',data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid})

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid})

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == 'User not found', \
            f"Invalid  message -{response4.content}"


    # Попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_created_user_by_another_user(self):
        # REGISTER NEW USER
        register_data = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # LOGIN OTHER USER
        login_data = {'email': 'vinkotov@example.com',
                      'password': '1234'
                      }
        response2 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        # Тут тоже похоже на баг апи в мессадже, потому что тест удаляет пользователя с user_id не из пула 1-5
        assert ('"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."' in
                response3.content.decode("utf-8")), f"Invalid  message -{response3.content}"