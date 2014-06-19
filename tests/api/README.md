Inbox API Stub
------

#### Update Mock Responses

Running `py.test tests/api/ --bootstrap` will create a `data` directory with the cached responses from gunks. Subsequent runs of `py.test` will check against that.

#### Serve Mock Responses

Running `python app.py` will start a Flask webserver to return those cached responses. See the root URL for a listing of available resources. You should be able to make responses with query parameters in any order.

Zero NodeJS required. ;)
