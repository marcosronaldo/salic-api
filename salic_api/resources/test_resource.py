from datetime import datetime

from .resource import ListResource


class TestResource(ListResource):
    """
    A simple endpoint that return a welcoming message for testing purposes.
    """

    def get(self):
        timestamp = str(datetime.now())
        return {
            'content': 'API is up and running :D',
            'timestamp': timestamp
        }
