TOKEN = '5760331339:AAG4QLiTfFBO2z9SDtSoAOGVw3-ukMsiX9g'

DB_HOST = 'localhost'
DB_PORT = 3306
DB_LOGIN = 'root'
DB_PASS = 'Neetqw2110'  # no mac Neetqw2110+++
DB_NAME = 'realtor'

# --------- object text ---------

OBJECT_TEXT = {
    'user': {
        # login
        'start_registration': 'Регистрация',
        'finish_registration': 'Регистрация успешна',
        'login': 'Вы авторизованы',
        'not_login': 'Вы не авторизованы',
        # enter data
        'enter_fullname': 'Введите ФИО',
        'enter_phone': 'Введите контактный номер телефона',
        'enter_experience': 'Введите ваш стаж',
        'enter_job': 'Введите информацию о текущем месте работы (если это не АН, то ИП)',
        'enter_key': 'Введите ваш ключ',
        'enter_region': 'Введите ваш регион',
        # exception
        'exc_key': 'Ключ не корректен, повторите ввод'
    },
    'objects': {
        # login
        'start_add': 'Добавить объект',
        'finish_add': 'Объект добавлен',
        # enter data
        'enter_region': 'Введите регион',
        'enter_city': 'Введите город',
        'enter_address': 'Введите адрес',
        'enter_street': 'Введите улицу',
        'enter_stage': 'Введите этаж',
        'enter_description': 'Введите описание объекта',
        'enter_price': 'Введите цена',
        'enter_quadrature': 'Введите квадратуру',
        'enter_property_type': 'Выберите тип недвижимости',
        'enter_ownership_type': 'Выберите тип собственности',
        'enter_phone': 'Выберите телефон', 
        # exception
        'exc_stage': 'Ошибка ввода. Повторите запрос.\nТекст должен содержать только цифры',
        'exc_price': 'Ошибка ввода. Повторите запрос.\nДопустимы только целые числа.',
        'exc_quadrature': 'Ошибка ввода. Повторите запрос.\nДопустимы дробные и целые числа.'
    },
    'main': {
        'sale_btn': 'Продажа',
        'feed_btn': 'Лента',
        'my_objects_btn': 'Мои объекты',
        'notification_btn': 'Уведомления',
        'cancel_btn': 'Отмена',
        'cancel_ok': 'Ок',
        'back_btn': 'Назад',
        'back_ok': 'Ок'
    }
}
