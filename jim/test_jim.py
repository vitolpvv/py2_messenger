import jim.protocol as protocol


class TestProtocol:

    def test_get_code_description(self):
        # описание кода по константе
        assert protocol.Code.get_description(protocol.Code.C_200) == 'OK'

        # описание кода по строке
        assert protocol.Code.get_description('201') == protocol.Code.get_description(protocol.Code.C_201)

        # описание кода по числу
        assert protocol.Code.get_description(500) == protocol.Code.get_description(protocol.Code.C_500)

        # описание не существующего кода
        assert protocol.Code.get_description(123456) is None

    def test_message_encoding_change(self):
        # кодировка по-умолчанию
        default_encoding = protocol.Message.get_encoding()

        assert protocol.Message.get_encoding() == 'utf-8'

        # смена кодировки
        protocol.Message.set_encoding('ascii')
        assert protocol.Message.get_encoding() == 'ascii'

        # смена кодировки
        protocol.Message.set_encoding(default_encoding)
        assert protocol.Message.get_encoding() == 'utf-8'

    def test_request_presence(self):
        message = protocol.Message.request_presence()

        # сообщение содержит поле 'action'
        assert protocol.Message.parse(message).get(protocol.Message.KEY_ACTION)
        # поле 'action' == 'presence'
        assert protocol.Message.parse(message).get(protocol.Message.KEY_ACTION) == protocol.Message.ACTION_PRESENCE

    def test_response(self):
        code = protocol.Code.C_200
        message = protocol.Message.response(code)

        # сообщение содержит поле 'response'
        assert protocol.Message.parse(message).get(protocol.Message.KEY_RESPONSE)
        # поле 'response' == code(200)
        assert protocol.Message.parse(message).get(protocol.Message.KEY_RESPONSE) == code

    def test_parse(self):
        message = protocol.Message.request_presence()

        # протокол возврыщает сообщение в виде набора байт
        assert type(message) == bytes
        # после парсинга получаем словарь
        assert type(protocol.Message.parse(message)) == dict
