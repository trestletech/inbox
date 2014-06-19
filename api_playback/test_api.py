import pytest
import requests
from .util import cache_get, TEST_API_ENDPOINTS

@pytest.mark.parametrize('endpoint', TEST_API_ENDPOINTS)
def test_api_endpoint(endpoint):
    r = requests.get(
        endpoint,
        auth=('foo-user', 'foo-pass'),
        verify=False)  # Testing server has self-signed cert
    assert r.status_code == 200
    assert cache_get(endpoint) == r.text
