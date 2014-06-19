import pytest
import requests
from util import cache_get, cache_set, TEST_API_ENDPOINTS


@pytest.mark.parametrize("to_fetch", TEST_API_ENDPOINTS)
def test_bootstrap(to_fetch, request):
    if not request.config.getoption("--bootstrap"):
        pytest.skip("only used to boostrap endpoint cache")
    print 'fetching {}'.format(to_fetch)
    r = requests.get(
        to_fetch,
        auth=('foo-user', 'foo-pass'),
        verify=False)  # Testing server has self-signed cert
    assert r.status_code == 200
    print 'Response of length {}'.format(len(r.text))
    cache_set(to_fetch, r.text)
    assert r.text == cache_get(to_fetch)




@pytest.mark.parametrize("to_fetch", TEST_API_ENDPOINTS)
def test_api_endpoints(to_fetch):
    r = requests.get(
        to_fetch,
        auth=('foo-user', 'foo-pass'),
        verify=False)  # Testing server has self-signed cert
    assert r.status_code == 200
    assert cache_get(to_fetch) == r.text

