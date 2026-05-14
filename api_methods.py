import allure
import requests

from urls import (
    BASE_URL,
    COURIER_LOGIN_URL,
    COURIER_URL,
    ORDER_CANCEL_URL,
    ORDER_TRACK_URL,
    ORDERS_URL,
)

REQUEST_TIMEOUT = 20


class CourierApi:
    @staticmethod
    @allure.step("Создать курьера")
    def create_courier(payload):
        return requests.post(COURIER_URL, data=payload, timeout=REQUEST_TIMEOUT)

    @staticmethod
    @allure.step("Авторизоваться курьером")
    def login_courier(payload):
        return requests.post(COURIER_LOGIN_URL, data=payload, timeout=REQUEST_TIMEOUT)

    @staticmethod
    @allure.step("Удалить курьера")
    def delete_courier(courier_id):
        return requests.delete(f"{COURIER_URL}/{courier_id}", timeout=REQUEST_TIMEOUT)


class OrderApi:
    @staticmethod
    @allure.step("Создать заказ")
    def create_order(payload):
        return requests.post(ORDERS_URL, json=payload, timeout=REQUEST_TIMEOUT)

    @staticmethod
    @allure.step("Получить список заказов")
    def get_orders():
        return requests.get(ORDERS_URL, timeout=REQUEST_TIMEOUT)

    @staticmethod
    @allure.step("Получить заказ по номеру")
    def get_order_by_track(params=None):
        return requests.get(ORDER_TRACK_URL, params=params, timeout=REQUEST_TIMEOUT)

    @staticmethod
    @allure.step("Отменить заказ")
    def cancel_order(params):
        return requests.put(ORDER_CANCEL_URL, params=params, timeout=REQUEST_TIMEOUT)

    @staticmethod
    @allure.step("Принять заказ")
    def accept_order(order_id, params=None):
        return requests.put(f"{BASE_URL}/orders/accept/{order_id}", params=params, timeout=REQUEST_TIMEOUT)
