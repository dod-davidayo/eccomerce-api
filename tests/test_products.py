import pytest
from app import create_app
from app.extension import db


@pytest.fixture
def app():
    # create test app WITH test config first
    app = create_app()

    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
        "JWT_SECRET_KEY": "test-secret",
        "WTF_CSRF_ENABLED": False
    })

    # IMPORTANT: rebind db to test config
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()