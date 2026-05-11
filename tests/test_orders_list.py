import allure

from helpers import api_request
from urls import ORDERS_URL


@allure.feature("Orders list")
class TestOrdersList:
    @allure.title("В тело ответа возвращается список заказов")
    def test_get_orders_returns_orders_list(self):
        response = api_request("get", ORDERS_URL)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
