from sqlalchemy import func

from ..database.connector import SqlConnector


class ModelsBase:
    def __init__(self):
        self.sql_connector = SqlConnector()

    def count(self, q):
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count or 0
