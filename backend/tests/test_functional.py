from backend import models
from pyramid.paster import get_app
from webtest import TestApp

def test_my_view_success(testapp, dbsession):
    model = models.MyModel(name='one', value=55)
    dbsession.add(model)
    dbsession.flush()

    res = testapp.get('/', status=200)
    assert res.body

def test_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404


def test_app():
    app = get_app('development.ini')
    testapp = TestApp(app)