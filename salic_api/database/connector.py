import logging
import urllib.error
import urllib.parse
import urllib.request
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__file__)

ENGINE_MAPPER = {}
register_engine = (lambda name: lambda f: ENGINE_MAPPER.setdefault(name, f))


class SqlConnector:
    def __init__(self):
        driver = current_app.config['SQL_DRIVER']
        try:
            engine = ENGINE_MAPPER[driver](current_app.config)
        except KeyError:
            msg = 'Unknown SQL driver: %r' % driver
            log.error(msg)
            raise RuntimeError(msg)

        # Start session
        session_class = sessionmaker(bind=engine)
        try:
            self.session = session_class()
            log.info('Connection Openned')
        except:
            log.error('Can\'t create database session')
            raise

        def __del__(self):
            # Close session after query executes
            self.session.close()
            log.info('Database connection closed')


#
# Register SQL engines
#
@register_engine('pymssql')
def pymssql_engine(config):
    uri = "mssql+pymssql://{user}:{pasword}@{host}:{port}/{name}".format(
        user=config['DATABASE_USER'],
        password=config['DATABASE_PASSWORD'],
        host=config['DATABASE_HOST'],
        port=config['DATABASE_PORT'],
        name=config['DATABASE_NAME'],
    )
    return create_engine(uri)


@register_engine('sqlite')
def sqlite_engine(config):
    return create_engine('sqlite:///db.sqlite3')


@register_engine('memory')
def sqlite_engine(config):
    return create_engine('sqlite://')


@register_engine('pyodbc')
def pymssql_uri(config):
    quoted = urllib.parse.quote_plus(
        'DRIVER={FreeTDS};Server=%s;Database=%s;UID=%s;PWD=%s;'
        'TDS_Version=8.0;CHARSET=UTF8;Port=1433;'
        % (current_app.config['DATABASE_HOST'],
           current_app.config['DATABASE_NAME'],
           current_app.config['DATABASE_USER'],
           current_app.config['DATABASE_PASSWORD']))
    return create_engine(
        'mssql+pyodbc:///?odbc_connect={}'.format(quoted),
        connect_args={'convert_unicode': True})


@register_engine('postgres')
def postgres_engine(config):
    uri = "postgresql://{user}:{pasword}@{host}:{port}/{name}".format(
        user=config['DATABASE_USER'],
        password=config['DATABASE_PASSWORD'],
        host=config['DATABASE_HOST'],
        port=config['DATABASE_PORT'],
        name=config['DATABASE_NAME'],
    )
    return create_engine(uri)
