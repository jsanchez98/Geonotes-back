import pytest
import tempfile
import os
from App import application
from App.db import get_db, init_db
from werkzeug.security import generate_password_hash
from tests.csrf_wrapper import NewFlaskClient

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

with open(os.path.join(os.path.dirname(__file__), 'teardown.sql'), 'rb') as f:
    _teardown_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    '''
    setup
    '''
    db_fd, db_path = tempfile.mkstemp()

    application.test_client_class = NewFlaskClient

    application.config.update({
        "TESTING": True,
        "DATABASE": db_path
    })

    with application.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield application

    '''
    teardown
    '''
    with application.app_context():
        get_db().executescript(_teardown_sql)

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
