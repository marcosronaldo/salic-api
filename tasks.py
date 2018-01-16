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


@task
def run(ctx):
    "Run flask application."

    env = {
        'FLASK_APP': 'salic_api.app.default',
        'PYTHONPATH': '.:' + ':'.join(sys.path),
    }
    ctx.run(sys.executable + ' -m flask run', env=env)


@task(
    help={'reset': 'delete sqlite database'}
)
def db(ctx, reset=False):
    """
    Populate test db.
    """

    from salic_api.fixtures import populate

    if reset:
        ctx.run('rm db.sqlite3 -f')
    populate()
    print('Db created successfully!')
