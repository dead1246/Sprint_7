import allure
import pytest

from data import CourierData, OrderData
from helpers import api_request, cancel_order, create_order, get_order_by_track
from urls import BASE_URL


@allure.feature("Order accept")
class TestAcceptOrder:
    @allure.title("Курьер может принять заказ")
    def test_accept_order_success(self, courier):
        order_response = create_order()
        track = order_response.json()["track"]
        order_id = get_order_by_track(track).json()["order"]["id"]

        try:
            response = api_request(
                "put",
                f"{BASE_URL}/orders/accept/{order_id}",
                params={"courierId": courier["id"]},
            )

            assert response.status_code == 200
            assert response.json() == {"ok": True}
        finally:
            cancel_order(track)

    @allure.title("Если не передать id курьера, запрос вернёт ошибку")
    def test_accept_order_without_courier_id_returns_error(self, order):
        order_id = get_order_by_track(order["track"]).json()["order"]["id"]

        response = api_request("put", f"{BASE_URL}/orders/accept/{order_id}")

        assert response.status_code == 400
        assert response.json()["message"] == OrderData.TRACK_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Если передать неверный id курьера, запрос вернёт ошибку")
    def test_accept_order_with_wrong_courier_id_returns_error(self, order):
        order_id = get_order_by_track(order["track"]).json()["order"]["id"]

        response = api_request(
            "put",
            f"{BASE_URL}/orders/accept/{order_id}",
            params={"courierId": 999999999},
        )

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.COURIER_ACCEPT_NOT_FOUND_MESSAGE

    @allure.title("Если не передать id заказа, запрос вернёт ошибку")
    def test_accept_order_without_order_id_returns_error(self, courier):
        response = api_request("put", f"{BASE_URL}/orders/accept/", params={"courierId": courier["id"]})

        assert response.status_code == 404
        assert response.json()["message"] == OrderData.NOT_FOUND_MESSAGE

    @allure.title("Если передать неверный id заказа, запрос вернёт ошибку")
    @pytest.mark.parametrize("order_id", [999999999])
    def test_accept_order_with_wrong_order_id_returns_error(self, courier, order_id):
        response = api_request(
            "put",
            f"{BASE_URL}/orders/accept/{order_id}",
            params={"courierId": courier["id"]},
        )

        assert response.status_code == 404
        assert response.json()["message"] == OrderData.ORDER_ID_NOT_FOUND_MESSAGE
