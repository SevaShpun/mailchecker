# -*- coding: utf-8 -*-

import poplib
import urllib
from settings import PASSWORD, USER_NAME, SMS_API_KEY, PHONE, POP_SERVER


class MailChecker(object):
    def __init__(self, password=PASSWORD, pop_server=POP_SERVER, user_name=USER_NAME, sms_api_key=SMS_API_KEY, phone=PHONE):
        self.password = password
        self.pop_server = pop_server
        self.user_name = user_name
        self.sms_api_key = sms_api_key
        self.phone = phone

    def check(self):
        print self.pop_server
        mailServer = poplib.POP3_SSL(self.pop_server)
        mailServer.user(self.user_name)
        mailServer.pass_(self.password)

        servicecodes = {
            100: "Сообщение принято к отправке. На следующих строчках вы найдете идентификаторы отправленных сообщений в том же порядке, в котором вы указали номера, на которых совершалась отправка.",
            200: "Неправильный api_id.",
            201: "Не хватает средств на лицевом счету.",
            202: "Неправильно указан получатель.",
            203: "Нет текста сообщения.",
            204: "Имя отправителя не согласовано с администрацией.",
            205: "Сообщение слишком длинное (превышает 8 СМС).",
            206: "Будет превышен или уже превышен дневной лимит на отправку сообщений.",
            207: "На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров в списке получателей.",
            208: "Параметр time указан неправильно.",
            209: "Вы добавили этот номер (или один из номеров) в стоп-лист.",
            210: "Используется GET, где необходимо использовать POST.",
            211: "Метод не найден.",
            212: "Текст сообщения необходимо передать в кодировке UTF-8 (вы передали в другой кодировке).",
            220: "Сервис временно недоступен, попробуйте чуть позже.",
            230: "Превышен общий лимит количества сообщений на этот номер в день.",
            231: "Превышен лимит одинаковых сообщений на этот номер в минуту.",
            232: "Превышен лимит одинаковых сообщений на этот номер в день.",
            300: "Неправильный token (возможно истек срок действия, либо ваш IP изменился).",
            301: "Неправильный пароль, либо пользователь не найден.",
            302: "Пользователь авторизован, но аккаунт не подтвержден (пользователь не ввел код, присланный в регистрационной смс).",
        }

        numMessages = len(mailServer.list()[1])
        for i in range(numMessages):
            for j in mailServer.retr(i + 1)[1]:
                if (j.find("Subject: Test") > -1):
                    smsParams = urllib.urlencode(
                        {
                            'api_id': self.sms_api_key,
                            'to': self.phone,
                            'text': 'Test message has arrived'
                        }
                    )
                    f = urllib.urlopen("http://sms.ru/sms/send?%s" % smsParams)
                    if f.read() in servicecodes:
                        print(servicecodes[int(f.read())])
                    else:
                        print(f.read())

        mailServer.quit()


def main():
    mc = MailChecker()
    mc.check()


if __name__ == '__main__':
    main()
