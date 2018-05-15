import json
import time


class Code:
    C_100 = '100'
    C_101 = '101'
    C_200 = '200'
    C_201 = '201'
    C_202 = '202'
    C_400 = '400'
    C_401 = '401'
    C_402 = '402'
    C_403 = '403'
    C_404 = '404'
    C_409 = '409'
    C_410 = '410'
    C_500 = '500'

    _DESCRIPTION = {
        C_100: 'базовое уведомление',
        C_101: 'важное уведомление',
        C_200: 'OK',
        C_201: 'объект создан',
        C_202: 'подтверждение',
        C_400: 'неправильный запрос/JSON-объект',
        C_401: 'не авторизован',
        C_402: 'неправильный логин/пароль',
        C_403: 'пользователь заблокирован',
        C_404: 'пользователь/чат отсутствует на сервере',
        C_409: 'уже имеется подключение с указанным логином',
        C_410: 'адресат существует, но недоступен (offline)',
        C_500: 'ошибка сервера'
    }

    @staticmethod
    def get_description(code):
        return Code._DESCRIPTION.get(str(code))


class Message:

    _DEF_ENCODING = 'utf-8'
    _MAX_LENGTH = 640

    ACTION_PRESENCE = 'presence'
    ACTION_PROBE = 'probe'
    ACTION_MSG = 'msg'
    ACTION_QUIT = 'quit'
    ACTION_AUTH = 'authenticate'
    ACTION_LEAVE = 'leave'
    ACTION_JOIN = 'join'

    @staticmethod
    def set_encoding(coding_type):
        Message._DEF_ENCODING = coding_type

    @staticmethod
    def get_encoding():
        return Message._DEF_ENCODING

    @staticmethod
    def request_presence(encoding=_DEF_ENCODING):
        message = {
            'action': Message.ACTION_PRESENCE,
            'time': time.time()
        }
        return json.dumps(message).encode(encoding)

    @staticmethod
    def response(code, text=None, encoding=_DEF_ENCODING):
        if Code.get_description(code) is None:
            return None
        message = {
            'response': code,
            'time': time.time(),
            'text': text if text else ''
        }
        return json.dumps(message).encode(encoding)

    @staticmethod
    def parse(message, encoding=_DEF_ENCODING):
        return json.loads(message.decode(encoding))

    @staticmethod
    def get_max_length():
        return Message._MAX_LENGTH


if __name__ == '__main__':
    pass
