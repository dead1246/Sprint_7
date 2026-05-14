import allure

from api_methods import CourierApi
from data import CourierData, OrderData


@allure.feature("Courier deletion")
class TestDeleteCourier:
    @allure.title("Успешное удаление курьера возвращает ok true")
    def test_delete_courier_success(self, courier):
        response = CourierApi.delete_courier(courier["id"])

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Запрос на удаление без id возвращает ошибку")
    def test_delete_courier_without_id_returns_error(self):
        response = CourierApi.delete_courier("")

        assert response.status_code == 404
        assert response.json()["message"] == OrderData.NOT_FOUND_MESSAGE

    @allure.title("Запрос на удаление с несуществующим id возвращает ошибку")
    def test_delete_nonexistent_courier_returns_error(self):
        response = CourierApi.delete_courier(999999999)

        assert response.status_code == 404
        assert response.json()["message"] == CourierData.COURIER_NOT_FOUND_MESSAGE
