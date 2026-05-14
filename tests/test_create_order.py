import allure
import pytest

from data import OrderData


@allure.feature("Order creation")
class TestCreateOrder:
    @allure.title("Заказ можно создать с разными вариантами цвета")
    @pytest.mark.parametrize("created_order", OrderData.ORDER_PAYLOADS_WITH_COLOR_OPTIONS, indirect=True)
    def test_create_order_with_color_options_returns_track(self, created_order):
        response = created_order["response"]

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
