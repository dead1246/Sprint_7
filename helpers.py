import random
import string
import time

import requests

from urls import COURIER_LOGIN_URL, COURIER_URL, ORDER_CANCEL_URL, ORDER_TRACK_URL, ORDERS_URL

REQUEST_TIMEOUT = 20
RETRY_STATUSES = {500, 502, 503, 504}


def api_request(method, url, **kwargs):
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    last_exception = None

    for attempt in range(3):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code not in RETRY_STATUSES or attempt == 2:
                return response
        except requests.RequestException as exception:
            last_exception = exception
            if attempt == 2:
                raise
        time.sleep(1)

    raise last_exception


def generate_random_string(length=10):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }


def create_courier(payload=None):
    courier_payload = payload or generate_courier_payload()
    response = api_request("post", COURIER_URL, data=courier_payload)
    return response, courier_payload


def login_courier(login, password):
    return api_request(
        "post",
        COURIER_LOGIN_URL,
        data={"login": login, "password": password},
    )


def create_courier_and_return_payload_with_id():
    response, payload = create_courier()
    if response.status_code != 201:
        return {}

    login_response = login_courier(payload["login"], payload["password"])
    if login_response.status_code == 200:
        payload["id"] = login_response.json()["id"]

    return payload


def delete_courier(courier_id):
    if courier_id is None:
        return None
    try:
        return api_request("delete", f"{COURIER_URL}/{courier_id}")
    except requests.RequestException:
        return None


def build_order_payload(color=None):
    from data import OrderData

    payload = OrderData.DEFAULT_ORDER.copy()
    if color is not None:
        payload["color"] = color
    return payload


def create_order(color=None):
    return api_request("post", ORDERS_URL, json=build_order_payload(color))


def get_order_by_track(track):
    return api_request("get", ORDER_TRACK_URL, params={"t": track})


def cancel_order(track):
    if track is None:
        return None
    try:
        return api_request("put", ORDER_CANCEL_URL, params={"track": track})
    except requests.RequestException:
        return None
