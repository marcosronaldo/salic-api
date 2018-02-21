import contextlib

from ..connector import get_session, get_engine
from ..models import Projeto


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


def populate(*, session=None, app=None, driver=None, size=1, factories=None):
    """
    Populate database with some examples.

    Args:
        session:
            The current SQL alchemy session object.
        app:
            Flask application instance.
        driver (str):
            Driver name used to create a connection
        size (int):
            Optional size used to generate values from the factory functions
        factories:
            A list of factory functions. Each factory function is a callable
            that return a list of objects and might accept an optional size
            argument.
    """

    if session is None:
        session = get_session(driver=driver, app=app)

    # Create entities
    if factories is None:
        factories = FACTORIES

    all_objects = []
    for factory in factories:
        if 'size' in factory.__code__.co_varnames:
            objects = factory(size=size)
        else:
            objects = factory()

        for obj in objects:
            session.add(obj)
            all_objects.append(obj)

    session.commit()
    return all_objects


def fixture_for_pytest(name, factories, size=1):
    """
    Create a Pytest fixture from a list of factories.
    """
    import pytest

    def fixture_function():
        try:
            yield populate(factories=factories, size=size)
        finally:
            clear_tables()

    fixture_function.__name__ = name
    return pytest.yield_fixture(fixture_function)


@contextlib.contextmanager
def examples(factories, size=1):
    """
    Populate using the provided factories and remove objects after leaving
    the with block.

    Examples:
        >>> with examples([factory1, factory2]) as objs:
        ...     do_something_with_objects(objs)
        ... # now the database is clean!
    """

    try:
        yield populate(factories=factories, size=size)
    finally:
        clear_tables()


FACTORIES = []
