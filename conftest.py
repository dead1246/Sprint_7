import pytest

from api_methods import CourierApi, OrderApi
from data import OrderData
from helpers import generate_courier_payload


@pytest.fixture
def courier():
    payload = generate_courier_payload()
    create_response = CourierApi.create_courier(payload)
    login_response = CourierApi.login_courier({"login": payload["login"], "password": payload["password"]})
    courier_id = login_response.json()["id"]
    yield {"payload": payload, "id": courier_id, "create_response": create_response}
    CourierApi.delete_courier(courier_id)


@pytest.fixture
def order():
    response = OrderApi.create_order(OrderData.ORDER_WITHOUT_COLOR)
    track = response.json()["track"]
    yield {"response": response, "track": track}
    OrderApi.cancel_order({"track": track})


@pytest.fixture
def created_order(request):
    response = OrderApi.create_order(request.param)
    track = response.json()["track"]
    yield {"response": response, "track": track}
    OrderApi.cancel_order({"track": track})
