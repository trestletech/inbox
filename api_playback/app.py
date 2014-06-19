"""
This is a simple Flask app that just serves back the static responses
that we have previously cached.
"""

from flask import Flask, request, Response
app = Flask(__name__)

from util import resource_path_for_url
from conftest import ALL_API_ENDPOINTS


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Note that fragments are not supported
    if not path:
        return "<h2>Available endpoints:</h2>" + \
            "".join(['<a href="{0}">{0}</a><br/>'\
                    .format(url) for url in ALL_API_ENDPOINTS])

    path = resource_path_for_url(request.url)

    try:
        with open(path, 'r') as res_file:
            return Response(res_file.read(), mimetype='application/json')
    except IOError:
        return 'Not found.', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8999, debug=True)
