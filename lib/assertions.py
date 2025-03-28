from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expecte_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format.Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key'{name}"
        assert response_as_dict[name] == expecte_value, error_message