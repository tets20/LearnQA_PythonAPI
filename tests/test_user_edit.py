import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import string


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
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

        # EDIT
        new_name = "Changed Name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid},
                                 data = {"firstName" : new_name})

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid})

        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit")


    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_no_auth_user(self):
        # REGISTER NEW USER
        register_data = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # EDIT BY NO AUTH
        new_name = "Changed Name"
        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        assert '"error":"Auth token not supplied"' in  response2.content.decode("utf-8"), \
            f"Invalid  message -{response2.content}"


    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_created_user_by_another_user(self):
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
        response2 = requests.post('https://playground.learnqa.ru/api/user/login',data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid},
                                 data = {"firstName" : new_name})

        Assertions.assert_code_status(response3, 400)

        # Тут похоже на баг апи в мессадже, потому что тест редактирует пользователя с user_id не из пула 1-5
        assert ('"error":"Please, do not edit test users with ID 1, 2, 3, 4 or 5."' in
                response3.content.decode("utf-8")),f"Invalid  message -{response3.content}"

    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_just_created_user_on_invalid_email(self):
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

        # EDIT MAIL WITHOUT @
        new_email = "mail.mail.com"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid},
                                 data = {"email" : new_email})

        Assertions.assert_code_status(response3, 400)
        assert '"error":"Invalid email format"' in  response3.content.decode("utf-8"), \
            f"Invalid  message -{response3.content}"


    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    def test_edit_just_created_user_on_too_short_firstname(self):
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

        # EDIT MAIL WITHOUT @
        new_firstName = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid" : auth_sid},
                                 data = {"firstName" : new_firstName})

        Assertions.assert_code_status(response3, 400)
        assert '"error":"The value for field `firstName` is too short"' in  response3.content.decode("utf-8"), \
             f"Invalid  message -{response3.content}"
