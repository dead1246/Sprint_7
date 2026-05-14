class CourierData:
    DEFAULT_PASSWORD = "password123"
    DUPLICATE_LOGIN_MESSAGE = "Этот логин уже используется. Попробуйте другой."
    CREATE_NOT_ENOUGH_DATA_MESSAGE = "Недостаточно данных для создания учетной записи"
    LOGIN_NOT_ENOUGH_DATA_MESSAGE = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND_MESSAGE = "Учетная запись не найдена"
    COURIER_NOT_FOUND_MESSAGE = "Курьера с таким id нет."
    COURIER_ACCEPT_NOT_FOUND_MESSAGE = "Курьера с таким id не существует"


class OrderData:
    DEFAULT_ORDER = {
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "address": "Moscow, Test street, 1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 2,
        "deliveryDate": "2026-05-12",
        "comment": "Created by autotest",
    }
    ORDER_WITHOUT_COLOR = DEFAULT_ORDER.copy()
    ORDER_WITH_BLACK_COLOR = {**DEFAULT_ORDER, "color": ["BLACK"]}
    ORDER_WITH_GREY_COLOR = {**DEFAULT_ORDER, "color": ["GREY"]}
    ORDER_WITH_BOTH_COLORS = {**DEFAULT_ORDER, "color": ["BLACK", "GREY"]}
    ORDER_PAYLOADS_WITH_COLOR_OPTIONS = [
        ORDER_WITH_BLACK_COLOR,
        ORDER_WITH_GREY_COLOR,
        ORDER_WITH_BOTH_COLORS,
        ORDER_WITHOUT_COLOR,
    ]

    ORDER_NOT_FOUND_MESSAGE = "Заказ не найден"
    ORDER_ID_NOT_FOUND_MESSAGE = "Заказа с таким id не существует"
    TRACK_NOT_ENOUGH_DATA_MESSAGE = "Недостаточно данных для поиска"
    NOT_FOUND_MESSAGE = "Not Found."
