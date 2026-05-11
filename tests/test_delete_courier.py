import allure

from data import CourierData, OrderData
from helpers import api_request, create_courier_and_return_payload_with_id
from urls import COURIER_URL


@allure.feature("Courier deletion")
class TestDeleteCourier:
    @allure.title("Успешное удаление курьера возвращает ok true")
    def test_delete_courier_success(self):
        courier = create_courier_and_return_payload_with_id()

        response = api_request("delete", f"{COURIER_URL}/{courier['id']}")

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Запрос на удаление без id возвращает ошибку")
    def test_delete_courier_without_id_returns_error(self):
        response = api_request("delete", f"{COURIER_URL}/")

        assert response.status_code == 404
        assert response.json()["message"] == OrderData.NOT_FOUND_MESSAGE

    @allure.title("Запрос на удаление с несуществующим id возвращает ошибку")
    def test_delete_nonexistent_courier_returns_error(self):
        response = api_request("delete", f"{COURIER_URL}/999999999")

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.COURIER_NOT_FOUND_MESSAGE
