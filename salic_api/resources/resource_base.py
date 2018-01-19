import logging

from flask import Response
from flask import current_app
from flask import request
from flask_cache import Cache
from flask_restful import Resource

from .serialization import serialize, listify_queryset
from ..app.security import md5hash

log = logging.getLogger('salic-api')

# Formats and mime types
VALID_FORMATS = {'json', 'xml', 'csv'}
JSON_MIME = 'application/hal+json; charset=utf-8'
CSV_MIME = 'text/csv; charset=utf-8'
XML_MIME = 'application/xml; charset=utf-8'

# Mime map
ACCEPT_HEADERS = {
    'application/xml': 'xml',
    'text/csv': 'csv',
    'application/hal+json': 'json',
    'application/json': 'json',
}

# Headers
ACCESS_CONTROL_HEADERS = (
    "Content-Length, Content-Type, Date, Server, "
    "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, "
    "Retry-After, "
    "X-Total-Count, "
    "Content-Disposition"
)


class SalicResource(Resource):
    """
    Base class for List and Detail resources.
    """

    # Basics
    resource_path = None
    query_class = None

    # Pre-defined error messages
    INTERNAL_ERROR = {
        'message': 'internal error',
        'code': 13,
    }
    INVALID_FORMAT = {
        'message': 'invalid format',
        'code': 55,
    }

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
        if getattr(current_app, 'cache', None) is None:
            current_app.cache = Cache(current_app)
            current_app.cache.clear()
            current_app.before_request(on_request_start)

        self.to_hal = self.build_hal

    #
    # Error factories
    #
    def internal_error(self, status_code=500):
        """
        Default 500 internal error.
        """
        log.info('invalid request (%s, code=13)' % status_code)
        return InvalidResult(self.INTERNAL_ERROR, status_code)

    #
    # HAL links
    #
    def build_hal(self, data, args):
        """
        Insert HAL info on output data.

        HAL info usually comprises of a _links and a _embedded fields
        """
        links = self.hal_links(data, args)
        embedded = self.hal_embedded(data, args)

        if isinstance(data, dict):
            result = data
        else:
            result = {}

        if links:
            result['_links'] = links
        if embedded:
            result['_embedded'] = embedded
        return result

    def hal_links(self, data, args):
        """
        Return the link dictionary that is stored on '_links' field of a
        JSON+HAL response.
        """
        path = self.resource_path

        if path is None:
            return None
        else:
            return {'self': self.url('/%s/' % path)}

    #
    # Utility functions
    #
    def url(self, path):
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

    def hal_embedded(self, data, args):
        """
        Return a dictionary of embedded resources stored at the '_embedded'
        field of a JSON+HAL response.
        """
        return None

    def unique_cgccpf(self, cgccpf, elements):
        """
        Given a cgc/cpf/cnpj, makes sure it return only elements with exact match
        Used to correct the use of SQL LIKE statement
        """
        return [e for e in elements if e['cgcpf'] == cgccpf]

    def last_offset(self, n_records, limit):
        if n_records % limit == 0:
            return (n_records / limit - 1) * limit
        else:
            return n_records - (n_records % limit)

    #
    # Creating response
    #
    def get(self, **kwargs):
        """
        Default response to a GET request.
        """

        try:
            result = self.fetch_result(**kwargs)
            result = self.prepare_result(result)
            self.fetch_related(result, **kwargs)
            return self.render(result)

        # Expected errors
        except InvalidResult as error:
            if current_app.testing:
                raise
            return error.render(self)

        # Unexpected errors
        except Exception as ex:
            if current_app.testing:
                raise
            fmt = (type(self).__name__, type(ex).__name__, ex)
            log.error('%s: unhandled exception, %s: %s' % fmt)
            return self.internal_error().render(self)

    def fetch_result(self, **kwargs):
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

    def prepare_result(self, result):
        """
        Prepare result obtained from .fetch_result() to be ready for JSON
        serialization.
        """
        return listify_queryset(result)

    def fetch_related(self, result, **kwargs):
        """
        Fetch all related and embedded data from other models and add it to the
        current result.

        The default implementation does nothing, but can be overridden in
        subclasses.
        """

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
            data = dict(self.INVALID_FORMAT)
            status_code = 405

        if content_type == 'xml':
            if not raw:
                data = serialize(data, 'xml')
            response = Response(data, content_type=XML_MIME)

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
            response = Response(data, content_type=CSV_MIME)

        else:
            if not raw:
                if status_code == 200:
                    args = {}
                    if 'X-Total-Count' in headers:
                        args['total'] = headers['X-Total-Count']
                    data = self.to_hal(data, args=args)
                data = serialize(data, 'json')
            response = Response(data, content_type=JSON_MIME)

        headers['Access-Control-Expose-Headers'] = ACCESS_CONTROL_HEADERS
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
            return format if format in VALID_FORMATS else None
        except KeyError:
            accept = request.headers.get('Accept', 'application/hal+json')
            json_values = ('application/hal+json', 'application/json', '*/*')
            if any(v in accept for v in json_values):
                return 'json'
            elif 'text/csv' in accept:
                return 'csv'
            elif 'application/xml' in accept:
                return 'xml'
            else:
                return None


class ListResource(SalicResource):
    """
    Base class for all Salic-API end points that return lists.
    """


class DetailResource(SalicResource):
    """
    Base class for all end points that return dictionaries.
    """


def format_args(args: dict):
    return '&'.join('%s=%s' % item for item in args.items())


def on_request_start():
    content_type = request.headers.get('Accept', '')
    real_ip = request.headers.get('X-Real-Ip', '')
    args = format_args(request.args)
    log.info(' '.join([request.path, args, real_ip, content_type]))


class InvalidResult(Exception):
    """
    Exception raised for invalid errors
    """

    def __init__(self, message, status_code=500):
        super().__init__(message, status_code)

    def render(self, resource):
        """
        Render error message using the supplied resource renderer.
        """
        payload, status_code = self.args
        return resource.render(payload, status_code=status_code)
