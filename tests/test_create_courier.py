import allure
import pytest

from api_methods import CourierApi
from data import CourierData
from helpers import generate_courier_payload


@allure.feature("Courier creation")
class TestCreateCourier:
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, courier):
        assert courier["create_response"].status_code == 201
        assert courier["create_response"].json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_returns_conflict(self, courier):
        response = CourierApi.create_courier(courier["payload"])

        assert response.status_code == 409
        assert response.json()["message"] == CourierData.DUPLICATE_LOGIN_MESSAGE

    @allure.title("Для создания курьера обязательны логин и пароль")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field_returns_bad_request(self, missing_field):
        payload = generate_courier_payload()
        payload.pop(missing_field)

        response = CourierApi.create_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == CourierData.CREATE_NOT_ENOUGH_DATA_MESSAGE
