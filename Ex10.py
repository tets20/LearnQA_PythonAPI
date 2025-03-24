class TestInput:
    def test_check_15_input(self):
        phrase = input("Set the phrase shorter than 15 characters: ")
        assert len(phrase) <= 15 , f"Введено {len(phrase)} символ(a/ов),что больше лимита"


