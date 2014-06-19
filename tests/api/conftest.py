import os
from md5 import md5
import errno
from urlparse import urlparse, parse_qs, urlunparse
from urllib import urlencode
from urlparse import urljoin


URL_PREFIX = 'https://gunks.inboxapp.com'
RESOURCE_DIR = './data'


def pytest_addoption(parser):
    parser.addoption("--bootstrap", action="store_true", default=False,
        help="Downloads the url endpoints to save for api testing.")


ALL_API_ENDPOINTS = [
    "/n/",
    "/n/6rhcf8db14sq3i8aixskd8n1z/",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads?tag=unread",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads?tag=archive,unread",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads?subject=The%20stealth%20hilarity%20of%20the%20mean%20tweet%20on%20YouTube",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads?count=10&offset=0",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads?count=10&offset=10",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads?from=golang-nuts@googlegroups.com",
    "/n/6rhcf8db14sq3i8aixskd8n1z/threads/2qzpuwm60t74mzw3a4r0x4ysi",
    "/n/6rhcf8db14sq3i8aixskd8n1z/contacts",
    "/n/6rhcf8db14sq3i8aixskd8n1z/contacts?filter=Michael&order_by=rank",
    "/n/6rhcf8db14sq3i8aixskd8n1z/contacts?filter=spang&order_by=rank",
    "/n/6rhcf8db14sq3i8aixskd8n1z/contacts?filter=spang@inboxapp.com&order_by=rank",
    "/n/6rhcf8db14sq3i8aixskd8n1z/contacts/752dvpgs2w96w8m59x3udrzb",
    "/n/6rhcf8db14sq3i8aixskd8n1z/drafts",
    "/n/6rhcf8db14sq3i8aixskd8n1z/messages",
    "/n/6rhcf8db14sq3i8aixskd8n1z/messages?from=golang-nuts@googlegroups.com",
    "/n/6rhcf8db14sq3i8aixskd8n1z/messages?subject=The%20stealth%20hilarity%20of%20the%20mean%20tweet%20on%20YouTube",
    "/n/6rhcf8db14sq3i8aixskd8n1z/messages?order_by=date",
    "/n/6rhcf8db14sq3i8aixskd8n1z/messages/e06ma4gy67l7356xi1knct61b"
]

TEST_API_ENDPOINTS = [urljoin(URL_PREFIX, url) for url in ALL_API_ENDPOINTS]


def cannonical_url(url):
    # clean up to cannonical
    scheme, netloc, path, params, query, fragment = urlparse(url)
    query_sorted = sorted(parse_qs(query).items())  # just to be safe

    def str_sanitize(k):
        """ Recursively convert elements to bytestrings. urlencode doesn't
            like unicode """
        if k is None:
            return None
        if isinstance(k, basestring):
            return str(k)
        if len(k) == 1 and isinstance(k[0], basestring):
            return str(k[0])
        return tuple([str_sanitize(a) for a in k])  # urlencode likes tuples
    try:
        query = urlencode(str_sanitize(query_sorted))
    except TypeError:
        print query_sorted
        raise
    return urlunparse(['', '', path, params, query, fragment])


def resource_name(url):
    return md5(url).hexdigest()


def resource_base_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
        RESOURCE_DIR)


def resource_path_for_url(url):
    url = cannonical_url(url)
    name = resource_name(url)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
        RESOURCE_DIR, name)


def cache_set(url, content):
    base_path = resource_base_path()
    try:
        os.makedirs(base_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(base_path):
            pass
        else:
            raise
    with open(resource_path_for_url(url), 'w') as f:
        f.write(content)
    print 'Done'


def cache_get(url):
    with open(resource_path_for_url(url), 'r') as f:
        return f.read()
