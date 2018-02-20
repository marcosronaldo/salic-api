import contextlib

from salic_api.connector import get_session, get_engine

from salic_api.models import Projeto


#
# Populate a test db
#
def make_tables(*, app=None, driver=None, session=None):
    """
    Create tables from schema.
    """
    if session is None:
        session = get_session(driver=driver, app=app)

    # Create tables
    Projeto.metadata.create_all(session.bind)
    session.commit()


def clear_tables():
    """
    Clear all data in tables for the current session.

    Works only with the "memory" connector used in tests.
    """
    meta = Projeto.metadata

    with contextlib.closing(get_engine('memory').connect()) as con:
        trans = con.begin()

        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def populate(*, session=None, app=None, driver=None):
    """
    Populate database with some examples.
    """

    if session is None:
        session = get_session(driver=driver, app=app)

    # Create entities
    for factory in FACTORIES:
        for obj in factory():
            session.add(obj)
    session.commit()


FACTORIES = []
