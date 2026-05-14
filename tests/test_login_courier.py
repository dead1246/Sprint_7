import allure
import pytest

from api_methods import CourierApi
from data import CourierData
from helpers import generate_random_string


@allure.feature("Courier login")
class TestLoginCourier:
    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self, courier):
        response = CourierApi.login_courier(
            {"login": courier["payload"]["login"], "password": courier["payload"]["password"]}
        )

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Для авторизации обязательны логин и пароль")
    @pytest.mark.parametrize("payload", [{"password": "password"}, {"login": "login", "password": ""}])
    def test_login_without_required_field_returns_bad_request(self, payload):
        response = CourierApi.login_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == CourierData.LOGIN_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Система возвращает ошибку при неверном пароле")
    def test_login_with_wrong_password_returns_not_found(self, courier):
        response = CourierApi.login_courier(
            {"login": courier["payload"]["login"], "password": generate_random_string()}
        )

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title("Система возвращает ошибку при неверном логине")
    def test_login_with_wrong_login_returns_not_found(self, courier):
        response = CourierApi.login_courier(
            {"login": generate_random_string(), "password": courier["payload"]["password"]}
        )

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title("Авторизация несуществующего пользователя возвращает ошибку")
    def test_login_nonexistent_courier_returns_not_found(self):
        response = CourierApi.login_courier(
            {"login": generate_random_string(), "password": generate_random_string()}
        )

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.ACCOUNT_NOT_FOUND_MESSAGE
