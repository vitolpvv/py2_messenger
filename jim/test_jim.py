import jim.protocol as protocol


class TestJim:

    def test_get_code_description(self):
        # описание кода по константе
        assert protocol.Code.get_description(protocol.Code.C_200) == 'OK'

        # описание кода по строке
        assert protocol.Code.get_description('201') == protocol.Code.get_description(protocol.Code.C_201)

        # описание кода по числу
        assert protocol.Code.get_description(500) == protocol.Code.get_description(protocol.Code.C_500)

        # описание не существующего кода
        assert protocol.Code.get_description(123456) is None
