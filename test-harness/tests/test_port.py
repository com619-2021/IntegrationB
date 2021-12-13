import os

import requests
import pytest


@pytest.mark.port
def test_availability():
    port_url = os.environ["PORT_URL"]
    resp = requests.get(port_url)
    assert resp.status_code == 200
