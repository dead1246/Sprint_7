import allure

from api_methods import OrderApi


@allure.feature("Orders list")
class TestOrdersList:
    @allure.title("В тело ответа возвращается список заказов")
    def test_get_orders_returns_orders_list(self):
        response = OrderApi.get_orders()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
