Inbox API Stub
------

#### Update Mock Responses

Running `./api_playback/bootstrap.py` will create a `data` directory with the cached responses from gunks. Subsequent runs of `py.test api_playback/test_api.py` will check against that.

#### Serve Mock Responses

Running `python app.py` will start a Flask webserver to return those cached responses. See the root URL for a listing of available resources. You should be able to make responses with query parameters in any order.

Zero NodeJS required. ;)
