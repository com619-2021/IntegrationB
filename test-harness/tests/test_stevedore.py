import os

import requests
import pytest


@pytest.mark.stevedore
def test_availability():
    stevedore_url = os.environ["STEVEDORE_URL"]
    resp = requests.get(stevedore_url)
    assert resp.status_code == 200
