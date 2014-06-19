#!/usr/bin/env python
import requests
from util import cache_get, cache_set, TEST_API_ENDPOINTS


def bootstrap(endpoint, max_retries=3):
    print 'fetching {}'.format(endpoint)
    for _ in range(max_retries):
        r = requests.get(
            endpoint,
            auth=('foo-user', 'foo-pass'),
            verify=False)  # Testing server has self-signed cert
        if r.status_code == 200:
            print 'Response of length {}'.format(len(r.text))
            break
        else:
            print 'Error {}'.format(r.status_code)
    cache_set(endpoint, r.text)
    assert r.text == cache_get(endpoint)


if __name__ == '__main__':
    for endpoint in TEST_API_ENDPOINTS:
        bootstrap(endpoint)
