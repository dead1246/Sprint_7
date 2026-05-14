import allure

from api_methods import OrderApi
from data import OrderData


@allure.feature("Get order by track")
class TestGetOrderByTrack:
    @allure.title("Успешный запрос возвращает объект с заказом")
    def test_get_order_by_track_success(self, order):
        response = OrderApi.get_order_by_track({"t": order["track"]})

        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == order["track"]

    @allure.title("Запрос без номера заказа возвращает ошибку")
    def test_get_order_without_track_returns_error(self):
        response = OrderApi.get_order_by_track()

        assert response.status_code == 400
        assert response.json()["message"] == OrderData.TRACK_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Запрос с несуществующим заказом возвращает ошибку")
    def test_get_nonexistent_order_returns_error(self):
        response = OrderApi.get_order_by_track({"t": 999999999})

        assert response.status_code == 404
        assert response.json()["message"] == OrderData.ORDER_NOT_FOUND_MESSAGE
