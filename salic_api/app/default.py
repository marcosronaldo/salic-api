import os

if os.environ.get('TESTING', 'false').lower() == 'true':
    app = None
else:
    from . import create_app

    app = create_app()
    del create_app
