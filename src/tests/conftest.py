import os
import pytest

from src import create_app, db  # updated
from src.api.models import User



@pytest.fixture(scope='module')
def test_app():

    os.environ['APP_SETTINGS']= 'src.config.TestingConfig' 
    app = create_app()  # new
    # app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        yield app  # testing happens here
    del os.environ['APP_SETTINGS']


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def add_user():
    def _add_user(username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    return _add_user