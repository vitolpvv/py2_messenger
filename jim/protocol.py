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


class Converter:

    _DEF_ENCODING = 'utf-8'

    @staticmethod
    def set_encoding(coding_type):
        Converter._DEF_ENCODING = coding_type

    @staticmethod
    def get_encoding():
        return Converter._DEF_ENCODING

    @staticmethod
    def from_bytes(message, encoding=None):
        return json.loads(message.decode(Converter._DEF_ENCODING if encoding is None else encoding))

    @staticmethod
    def to_bytes(message, encoding=None):
        return json.dumps(message).encode(Converter._DEF_ENCODING if encoding is None else encoding)


class Message:
    _MAX_LENGTH = 640

    KEY_ACTION = 'action'
    KEY_TIME = 'time'
    KEY_RESPONSE = 'response'
    KEY_TEXT = 'text'
    KEY_USER = 'user'
    KEY_USER_NAME = 'name'
    KEY_USER_PASS = 'password'
    KEY_MSG_TO = 'to'
    KEY_MSG_FROM = 'from'
    KEY_MSG_MESSAGE = 'message'

    ACTION_PRESENCE = 'presence'
    ACTION_PROBE = 'probe'
    ACTION_MSG = 'msg'
    ACTION_QUIT = 'quit'
    ACTION_AUTH = 'authenticate'
    ACTION_LEAVE = 'leave'
    ACTION_JOIN = 'join'

    @staticmethod
    def request_presence(name='Guest', encoding=None):
        message = {
            Message.KEY_ACTION: Message.ACTION_PRESENCE,
            Message.KEY_TIME: time.time(),
            Message.KEY_USER: {
                Message.KEY_USER_NAME: name
            }

        }
        return Converter.to_bytes(message, encoding)

    @staticmethod
    def request_message(name_from, name_to, message='', encoding=None):
        if message == '':
            return None
        message = {
            Message.KEY_ACTION: Message.ACTION_MSG,
            Message.KEY_TIME: time.time(),
            Message.KEY_MSG_FROM: name_from,
            Message.KEY_MSG_TO: name_to,
            Message.KEY_MSG_MESSAGE: message
        }
        return Converter.to_bytes(message, encoding)

    @staticmethod
    def response(code, text=None, encoding=None):
        if Code.get_description(code) is None:
            return None
        message = {
            Message.KEY_RESPONSE: code,
            Message.KEY_TIME: time.time(),
            Message.KEY_TEXT: text if text else ''
        }
        return Converter.to_bytes(message, encoding)

    @staticmethod
    def get_max_length():
        return Message._MAX_LENGTH


if __name__ == '__main__':
    pass
