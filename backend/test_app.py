from pyramid.paster import get_app
from webtest import TestApp
from .backend.models.mymodel import DBSession, User, Produk, Pembayaran, Pesanan
import pytest
from pyramid import testing

def test_app():
    app = get_app('development.ini')
    testapp = TestApp(app)


def test_homepage(testapp):
    res = testapp.get('/', status=200)
    assert 'Welcome' in res.text

def test_get_products():
    # Setup
    request = testing.DummyRequest()
    
    # Action
    response = get_products(request)
    
    # Assertions
    assert 'products' in response
    assert isinstance(response['products'], list)



def test_create_user():
    # Setup
    user = User(nama="Test User", email="test@example.com", password="testpassword")
    
    # Assertions
    assert user.nama == "Test User"
    assert user.email == "test@example.com"
    assert user.password == "testpassword"

@pytest.fixture(scope='function')
def db_session():
    connection = DBSession.connection()
    transaction = connection.begin()
    DBSession.begin_nested()
    
    yield DBSession

    DBSession.rollback()
    transaction.rollback()
    connection.close()

