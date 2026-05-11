import pytest

from helpers import cancel_order, create_courier_and_return_payload_with_id, create_order, delete_courier


@pytest.fixture
def courier():
    courier_data = create_courier_and_return_payload_with_id()
    yield courier_data
    delete_courier(courier_data.get("id"))


@pytest.fixture
def order():
    response = create_order()
    track = response.json().get("track") if response.status_code == 201 else None
    yield {"response": response, "track": track}
    cancel_order(track)
