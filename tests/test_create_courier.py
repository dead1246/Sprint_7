import allure
import pytest

from data import CourierData
from helpers import create_courier, delete_courier, generate_courier_payload, login_courier


@allure.feature("Courier creation")
class TestCreateCourier:
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        response, payload = create_courier()
        courier_id = None

        try:
            assert response.status_code == 201
            assert response.json() == {"ok": True}

            login_response = login_courier(payload["login"], payload["password"])
            courier_id = login_response.json().get("id")
        finally:
            delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_returns_conflict(self):
        first_response, payload = create_courier()
        courier_id = None

        try:
            duplicate_response, _ = create_courier(payload)

            assert first_response.status_code == 201
            assert duplicate_response.status_code == 409
            assert duplicate_response.json()["message"] == CourierData.DUPLICATE_LOGIN_MESSAGE

            login_response = login_courier(payload["login"], payload["password"])
            courier_id = login_response.json().get("id")
        finally:
            delete_courier(courier_id)

    @allure.title("Для создания курьера обязательны логин и пароль")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field_returns_bad_request(self, missing_field):
        payload = generate_courier_payload()
        payload.pop(missing_field)

        response, _ = create_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == CourierData.CREATE_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Создание курьера с существующим логином возвращает ошибку")
    def test_create_courier_with_existing_login_returns_error(self):
        first_response, payload = create_courier()
        courier_id = None

        try:
            payload_with_same_login = {
                "login": payload["login"],
                "password": "another_password",
                "firstName": "another_name",
            }
            response, _ = create_courier(payload_with_same_login)

            assert first_response.status_code == 201
            assert response.status_code == 409
            assert response.json()["message"] == CourierData.DUPLICATE_LOGIN_MESSAGE

            login_response = login_courier(payload["login"], payload["password"])
            courier_id = login_response.json().get("id")
        finally:
            delete_courier(courier_id)
