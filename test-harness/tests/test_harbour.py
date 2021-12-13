import os

import requests
import pytest


@pytest.mark.harbour
def test_availability():
    harbour_url = os.environ["HARBOUR_URL"]
    resp = requests.get(harbour_url)
    assert resp.status_code == 200
