from sqlalchemy import func

from ..database.connector import SqlConnector


class Query:
    """
    Base class for all query objects for the SALIC api.
    """

    def __init__(self):
        self.sql_connector = SqlConnector()

    def count(self, qs):
        """
        Return the number of elements on queryset.
        """

        count_q = qs.statement.with_only_columns([func.count()]).order_by(None)
        count = qs.session.execute(count_q).scalar()
        return count or 0
