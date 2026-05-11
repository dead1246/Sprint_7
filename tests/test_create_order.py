import allure
import pytest

from helpers import cancel_order, create_order


@allure.feature("Order creation")
class TestCreateOrder:
    @allure.title("Заказ можно создать с разными вариантами цвета")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], None])
    def test_create_order_with_color_options_returns_track(self, color):
        response = create_order(color)
        track = response.json().get("track") if response.status_code == 201 else None

        try:
            assert response.status_code == 201
            assert "track" in response.json()
            assert isinstance(response.json()["track"], int)
        finally:
            cancel_order(track)
