import os

import requests
import pytest


@pytest.mark.shipping
def test_availability():
    shipping_url = os.environ["SHIPPING_URL"]
    resp = requests.get(shipping_url)
    assert resp.status_code == 200
