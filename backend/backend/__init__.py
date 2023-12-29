from pyramid.config import Configurator
from pyramid.events import NewRequest
from sqlalchemy import engine_from_config
from .models.mymodel import DBSession, Base
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_jwt.policy import JWTAuthenticationPolicy
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        engine = engine_from_config(settings, 'sqlalchemy.')
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine
        config.add_request_method(
        lambda request: DBSession(), 
        'dbsession',
        reify=True
        )
        authn_policy = JWTAuthenticationPolicy('qwert123', http_header='Authorization')
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)
        my_session_factory = SignedCookieSessionFactory('itsaseekreet')
        config.set_session_factory(my_session_factory)
        config.add_route('add_user', '/api/register', request_method="POST")
        config.add_route('login', '/api/login', request_method='POST')
        config.add_route('save_movie', '/api/save_product', request_method='POST')
        config.add_route('get_movies', '/api/get_movies', request_method='GET')
        config.add_route('delete_movie', '/api/delete_movie/{name}')
        # config.add_route('get_products', '/api/get_products',  request_method='GET')
        # config.add_route('hapus_produk', '/api/hapus_produk', request_method='DELETE')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
