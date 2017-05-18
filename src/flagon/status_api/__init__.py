# The MIT License (MIT)
#
# Copyright (c) 2014 Steve Milner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
Status API for flags.
"""
import json

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException

from flagon.errors import UnknownFeatureError


class FlagonStatusAPI(object):
    """
    Simple Flag status read-only REST api.
    """

    _url_map = Map([
        Rule('/v0/<flag>', endpoint='flag_status')
    ])

    def __init__(self, backend):
        """
        Creates the API object. Requires a pre-configured backend.
        """
        self._backend = backend

    def wsgi_app(self, environ, start_response):
        """
        The WSGI App entry point.
        """
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        """
        Dispatcher for requests. Usees the _url_map to find the
        proper view to call.
        """
        adapter = self._url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException as e:
            return e

    def __call__(self, environ, start_response):
        """
        Callable interface which forwards to wsgi_app.
        """
        return self.wsgi_app(environ, start_response)

    # VIEWS

    def flag_status(self, request, flag):
        response = Response(content_type='application/json')
        response.headers.add_header(
            'Cache-Control', 'no-cache, no-store, must-revalidate')
        try:
            active = self._backend.is_active(flag)
            response.data = json.dumps({
                'active': bool(active), 'known': True})
            response.status_code = 200
            return response
        except UnknownFeatureError:
            response.data = json.dumps({
                'active': False, 'known': False})
            response.status_code = 404
            return response


def run_local_test_server(backend):
    """
    Runs a local test server using the given backend/
    """
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, FlagonStatusAPI(backend))
