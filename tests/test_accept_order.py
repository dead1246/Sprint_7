import allure

from api_methods import OrderApi
from data import CourierData, OrderData


@allure.feature("Order accept")
class TestAcceptOrder:
    @allure.title("Курьер может принять заказ")
    def test_accept_order_success(self, courier, order):
        order_id = OrderApi.get_order_by_track({"t": order["track"]}).json()["order"]["id"]

        response = OrderApi.accept_order(order_id, {"courierId": courier["id"]})

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Если не передать id курьера, запрос вернёт ошибку")
    def test_accept_order_without_courier_id_returns_error(self, order):
        order_id = OrderApi.get_order_by_track({"t": order["track"]}).json()["order"]["id"]

        response = OrderApi.accept_order(order_id)

        assert response.status_code == 400
        assert response.json()["message"] == OrderData.TRACK_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Если передать неверный id курьера, запрос вернёт ошибку")
    def test_accept_order_with_wrong_courier_id_returns_error(self, order):
        order_id = OrderApi.get_order_by_track({"t": order["track"]}).json()["order"]["id"]

        response = OrderApi.accept_order(order_id, {"courierId": 999999999})

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.COURIER_ACCEPT_NOT_FOUND_MESSAGE

    @allure.title("Если не передать id заказа, запрос вернёт ошибку")
    def test_accept_order_without_order_id_returns_error(self, courier):
        response = OrderApi.accept_order("", {"courierId": courier["id"]})

        assert response.status_code == 404
        assert response.json()["message"] == OrderData.NOT_FOUND_MESSAGE

    @allure.title("Если передать неверный id заказа, запрос вернёт ошибку")
    def test_accept_order_with_wrong_order_id_returns_error(self, courier):
        response = OrderApi.accept_order(999999999, {"courierId": courier["id"]})

        assert response.status_code == 404
        assert response.json()["message"] == OrderData.ORDER_ID_NOT_FOUND_MESSAGE
