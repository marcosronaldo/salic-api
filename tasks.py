import sys

from invoke import task

if '.' not in sys.path:
    sys.path.append('.')


@task
def install(ctx):
    """
    Install dependencies.
    """
    ctx.run(sys.executable + ' -m pip install -e .[dev]')


@task
def test(ctx):
    "Run tests."

    from pytest import main

    main(['tests'])


@task
def cov(ctx):
    "Run coverage analysis."

    from pytest import main

    main(['tests', '--cov'])


@task(
    help={'debug': 'enable debugging warnings.',
          'host': 'set interface to bind to.'}
)
def run(ctx, debug=False, host=None):
    "Run flask application."

    env = {
        'FLASK_APP': 'salic_api.app.default',
        'PYTHONPATH': '.:' + ':'.join(sys.path),
    }
    if debug:
        env['DEBUG'] = 'true'
    args = ''
    if host is not None:
        args += ' -h %s' % host
    ctx.run("%s -m flask run%s" % (sys.executable, args), env=env)


@task(
    help={'force': 'delete sqlite database'}
)
def db(ctx, force=False):
    """
    Populate test db.
    """

    from salic_api.fixtures import populate, make_tables

    if force:
        ctx.run('rm db.sqlite3 -f')
    make_tables()
    populate()
    print('Db created successfully!')
