TOKEN = '5760331339:AAG4QLiTfFBO2z9SDtSoAOGVw3-ukMsiX9g'

DB_HOST = 'localhost'
DB_PORT = 3306
DB_LOGIN = 'root'
DB_PASS = 'Neetqw2110+++'  # mac Neetqw2110
DB_NAME = 'realtor'


# ---------- dadata ------------

D_KEY = '4dc3b433f0ba3cec514a5019580c0688be029c16'
D_SECRET_KEY = '7b0549cd7cfae55471dcceb815f515d402655ffa'

# ------------ yandex --------------

Y_TOKEN = '334f77fd-ed61-4f8d-8b91-6b78273063bf'

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
        'enter_city': 'Введите ваш город',
        # exception
        'exc_key': 'Ключ не корректен, повторите ввод',
        'exc_region': 'Введено не корректное значение, повторите ввод',
        'exc_city': 'Введено не корректное значение, повторите ввод'
    },
    'objects': {
        # login
        'start_add': 'Добавить объект',
        'finish_add': 'Объект добавлен',
        # enter data
        'enter_region': 'Введите регион',
        'enter_city': 'Введите город',
        'enter_address': 'Введите адрес',
        'enter_area': 'Введите район',
        'enter_street': 'Введите улицу',
        'enter_rooms': 'Введите кол-во комнат',
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
        'exc_rooms': 'Ошибка ввода. Повторите запрос.\nДопустимы только целые числа.',
        'exc_quadrature': 'Ошибка ввода. Повторите запрос.\nДопустимы дробные и целые числа.',
        'exc_region': 'Ошибка ввода. Повторите запрос.',
        'exc_city': 'Ошибка ввода. Повторите запрос.',
        'exc_address': 'Ошибка ввода. Повторите запрос.',
        'exc_area': 'Ошибка ввода. Повторите запрос.',
        'loading': 'Загрузка...'
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
    },
    'feed': {
        'enter_current_price': 'Введите минималь и максимально допустимую сумму в формате: "0000-1111", где 0000-начальная цена, а 1111-максимальная',
        'no_objects': 'Данных нет',
        'exc_current_price': 'Ошибка ввода. \nДанный должны иметь вид: "0000-1111" где 0000-начальная цена, а 1111-максимальная.',
        'filter': 'Фильтр',
        'switch_filter': 'Применить фильтр к ленте ?',
        'feed': 'Лента',
        'objects_with_filter': 'Объекты с фильтром',
        'objects_without_filter': 'Все объекты',
        'city_btn': 'Населенный пункт',
        'area_btn': 'Район',
        'rooms_btn': 'Кол-во комнат',
        'price': 'Цена',
        'feed_ok_filter': 'Готово',
        'clear': 'Очистить фильтр'
    },
    'my_objects': {
        'all': 'Все объекты'
    }
}