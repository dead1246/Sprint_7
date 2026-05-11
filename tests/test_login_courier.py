import allure
import pytest

from data import CourierData
from helpers import api_request, generate_random_string
from urls import COURIER_LOGIN_URL


@allure.feature("Courier login")
class TestLoginCourier:
    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self, courier):
        response = api_request(
            "post",
            COURIER_LOGIN_URL,
            data={"login": courier["login"], "password": courier["password"]},
        )

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Для авторизации обязательны логин и пароль")
    @pytest.mark.parametrize("payload", [{"password": "password"}, {"login": "login", "password": ""}])
    def test_login_without_required_field_returns_bad_request(self, payload):
        response = api_request("post", COURIER_LOGIN_URL, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == CourierData.LOGIN_NOT_ENOUGH_DATA_MESSAGE

    @allure.title("Система возвращает ошибку при неверном логине или пароле")
    @pytest.mark.parametrize(
        "login_value,password_value",
        [("correct_login", "wrong_password"), ("wrong_login", "correct_password")],
    )
    def test_login_with_wrong_credentials_returns_not_found(self, courier, login_value, password_value):
        login = courier["login"] if login_value == "correct_login" else generate_random_string()
        password = courier["password"] if password_value == "correct_password" else generate_random_string()

        response = api_request("post", COURIER_LOGIN_URL, data={"login": login, "password": password})

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title("Авторизация несуществующего пользователя возвращает ошибку")
    def test_login_nonexistent_courier_returns_not_found(self):
        response = api_request(
            "post",
            COURIER_LOGIN_URL,
            data={"login": generate_random_string(), "password": generate_random_string()},
        )

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.ACCOUNT_NOT_FOUND_MESSAGE
