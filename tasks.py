import sys

from invoke import task

if '.' not in sys.path:
    sys.path.append('.')


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
    ctx.run('{} -m flask run'.format(sys.executable), env=env)


@task
def db(ctx, reset=False):
    """
    Populate test db.
    """

    from salic_api.fixtures import populate

    if reset:
        ctx.run('rm db.sqlite -f')
    populate()
