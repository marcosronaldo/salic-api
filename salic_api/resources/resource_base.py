import logging

from flask import Response
from flask import current_app
from flask import request
from flask_cache import Cache
from flask_restful import Resource

from .serialization import serialize, listify_queryset
from ..app.security import md5hash

log = logging.getLogger('salic-api')


class SalicResource(Resource):
    """
    Base class for all Salic-API resources.

    Salic API uses HAL (Hypertext application language) to model JSON responses.
    From a practical point of view, this means that most end points have a
    _links and a _embedded properties that collects all links the end point
    refers to and all lists of children objects embedded in the JSON response.
    """

    # Basics
    resource_path = None
    query_class = None

    # Formats
    valid_formats = {'json', 'xml', 'csv'}
    json_mime = 'application/hal+json; charset=utf-8'
    csv_mime = 'text/csv; charset=utf-8'
    xml_mime = 'application/xml; charset=utf-8'

    # Mime map
    accept_headers = {
        'application/xml': 'xml',
        'text/csv': 'csv',
        'application/hal+json': 'json',
        'application/json': 'json',
    }

    # Headers
    access_control_headers = (
        "Content-Length, Content-Type, Date, Server, "
        "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, "
        "Retry-After, "
        "X-Total-Count, "
        "Content-Disposition"
    )

    def __init__(self):
        # Rate limiting setup
        if current_app.config['RATE_LIMITING_ACTIVE']:
            rate_limit = current_app.config['GLOBAL_RATE_LIMITS']
            log.info('Rate limiting active: %s' % rate_limit)
        else:
            log.info('Rate limiting is off')

        # Caching setup
        if current_app.config['CACHING_ACTIVE']:
            log.info('Caching is active')
        else:
            current_app.config['CACHE_TYPE'] = 'null'
            log.info('Caching is off')
            current_app.config['CACHE_NO_NULL_WARNING'] = True

        # Register the cache instance and binds it on to your app
        current_app.cache = Cache(current_app)
        current_app.cache.clear()
        current_app.before_request(on_request_start)

        self.to_hal = self.build_hal

    def build_hal(self, data, args):
        """
        Insert HAL info on output data.

        HAL info usually comprises of a _links and a _embedded fields
        """
        links = self.get_hal_links(data, args)
        embedded = self.get_hal_embedded(data, args)

        if isinstance(data, dict):
            result = data
        else:
            result = {}

        if links:
            result['_links'] = links
        if embedded:
            result['_embedded'] = embedded
        return result

    def get_hal_links(self, data, args):
        """
        Return the link dictionary that is stored on '_links' field of a
        JSON+HAL response.
        """
        path = self.resource_path

        if path is None:
            return None
        else:
            return {'self': self.get_url('/%s/' % path)}

    def get_url(self, path):
        """
        Return a normalized URL for a path relative to the current resource.

        If path begins with a backslash, treat it as a absolute path relative
        to the API_ROOT_URL.
        """
        if path.startswith('/'):
            return current_app.config['API_ROOT_URL'] + path[1:]
        else:
            base = self.resource_path + '/' or ''
            return current_app.config['API_ROOT_URL'] + base + path

    def get_hal_embedded(self, data, args):
        """
        Return a dictionary of embedded resources stored at the '_embedded'
        field of a JSON+HAL response.
        """
        return None

    def get_unique_cgccpf(self, cgccpf, elements):
        """
        Given a cgc/cpf/cnpj, makes sure it return only elements with exact match
        Used to correct the use of SQL LIKE statement
        """
        return [e for e in elements if e['cgcpf'] == cgccpf]

    def get_last_offset(self, n_records, limit):
        if n_records % limit == 0:
            return (n_records / limit - 1) * limit
        else:
            return n_records - (n_records % limit)

    def all(self, **kwargs):
        """
        Return a query with all requested objects
        """
        if self.query_class is None:
            raise RuntimeError(
                'improperly configured (%s): please define the query_class for '
                'the current resource or implement the .all() method.' %
                type(self).__name__
            )
        return self.query_class().all(**kwargs)

    def get(self, **kwargs):
        """
        Default response to a GET request.
        """

        try:
            result = self.all(**kwargs)
        except RuntimeError:
            raise
        except Exception:
            if current_app.testing:
                raise
            log.error('not found: %s' % type(self).__name__)
            result = {
                'message': 'internal error',
                'message_code': 13,
            }
            return self.render(result, status_code=503)

        result = listify_queryset(result)
        return self.render(result)

    def render(self, data, headers=None, status_code=200, raw=False):
        """
        Render response for given data.

        Args:
            data:
                Raw data structure
            headers (dict):
                A mapping with extra headers for inclusion in the response.
            status_code (int):
                HTTP Response status code
            raw (bool):
                If True, do not serialize data to the desired format. Useful
                for testing.
        """

        headers = {} if headers is None else headers
        content_type = self.resolve_content()

        if content_type is None:
            data = {
                'message': 'invalid format',
                'code': 55,
            }
            status_code = 405

        if content_type == 'xml':
            if not raw:
                data = serialize(data, 'xml')
            response = Response(data, content_type=self.xml_mime)

        elif content_type == 'csv':
            if not raw:
                data = serialize(data, 'csv')
            resource_path = request.path.split("/")

            if resource_path[len(resource_path) - 1] != "":
                resource_type = resource_path[len(resource_path) - 1]
            else:
                resource_type = resource_path[len(resource_path) - 2]

            args_hash = md5hash(format_args(request.args))
            fmt = (resource_type, args_hash)
            filename = "attachment; filename=salicapi-%s-%s.csv" % fmt
            headers["Content-Disposition"] = filename
            response = Response(data, content_type=self.csv_mime)

        else:
            if not raw:
                if status_code == 200:
                    args = {}
                    if 'X-Total-Count' in headers:
                        args['total'] = headers['X-Total-Count']
                    data = self.to_hal(data, args=args)
                data = serialize(data, 'json')
            response = Response(data, content_type=self.json_mime)

        headers['Access-Control-Expose-Headers'] = self.access_control_headers
        response.headers.extend(headers)
        response.status_code = status_code
        real_ip = request.headers.get('X-Real-Ip') or ''
        log.info(' '.join(map(str, [request.path, real_ip, status_code,
                                    response.headers.get('Content-Length')])))
        return response

    def resolve_content(self):
        """
        Content Type resolution.
        """
        try:
            format = request.args['format']
            return format if format in self.valid_formats else None
        except KeyError:
            accept = request.headers.get('Accept', 'application/hal+json')
            if ('application/hal+json' in accept or
                    'application/json' in accept or
                    '*/*' in accept):
                return 'json'
            elif 'text/csv' in accept:
                return 'csv'
            elif 'application/xml' in accept:
                return 'xml'
            else:
                return None


def format_args(args: dict):
    return '&'.join('%s=%s' % item for item in args.items())


def on_request_start():
    content_type = request.headers.get('Accept', '')
    real_ip = request.headers.get('X-Real-Ip', '')
    args = format_args(request.args)
    log.info(' '.join([request.path, args, real_ip, content_type]))
