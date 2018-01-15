from flask.ext.limiter import HEADERS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def limiter(app):
    limiter = Limiter(app,
                      key_func=get_remote_address,
                      headers_enabled=True)

    limiter.header_mapping = {
        HEADERS.LIMIT: "X-My-Limit",
        HEADERS.RESET: "X-My-Reset",
        HEADERS.REMAINING: "X-My-Remaining"
    }

    return limiter.shared_limit(
        app.config['GLOBAL_RATE_LIMITS'], scope="salic_api")
