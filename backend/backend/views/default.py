from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
from pyramid.httpexceptions import HTTPBadRequest
import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import DBAPIError
import json
from ..models.mymodel import DBSession, User, Movie
import bcrypt




@view_config(route_name='home', renderer='backend:templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'backend'}

@view_config(route_name='save_movie', request_method='POST', renderer='json')
def save_product(request):
    try:
      
        data = request.POST
        namaFilm = data['movieName']
        gambar = request.POST['image'].file

        save_path = f'../src/assets/img/movie/{namaFilm}.png'
        with open(save_path, 'wb') as f:
            f.write(gambar.read())

    

        
        new_product = Movie(
            movieName=namaFilm,
            image=save_path,
        
        )

        DBSession.add(new_product)
        DBSession.flush()
        DBSession.commit()

        return {"status": "success"}

    except KeyError:
        return Response('Invalid data', status=400, content_type='application/json')
    except DBAPIError:
        return Response('Database error', status=500, content_type='application/json')
    
 
@view_config(route_name='delete_movie', request_method='DELETE', renderer='json')
def delete_movie(request):
    try:
        movie_name = request.matchdict['movieName']
        movie = DBSession.query(Movie).filter(Movie.movieName == movie_name).first()

        if not movie:
            return HTTPNotFound(json_body={"status": "error", "message": "Movie not found"})

        if os.path.exists(movie.image):
            os.remove(movie.image)

        DBSession.delete(movie)
        DBSession.flush()
        DBSession.commit()

        return {"status": "success"}

    except SQLAlchemyError as e:
        return Response('Database error: ' + str(e), status=500)
    
@view_config(route_name='get_movies', renderer='json')
def get_movies(request):
    movies = DBSession.query(Movie).all()
    movie_list = [{'movieName': movie.movieName, 'image': movie.image} for movie in movies]
    return {'movies': movie_list}




@view_config(route_name='add_user', request_method='POST', renderer='json')
def register(request):
    try:
        data = request.json_body
        nama = data['nama']
        email = data['email']
        password = data['password']

        # Hashing password sebelum menyimpan ke database
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        user = DBSession.query(User).filter(User.email == email).first()

        if user:
            return Response('Email Sudah ada', status=400)

        new_user = User(nama=nama, email=email, password=password,
                        hashed_password=hashed_password, status="User")

        DBSession.add(new_user)
        DBSession.flush()
        DBSession.commit()

        return {"status": "success"}

    except KeyError:
        return HTTPBadRequest(json_body={"status": "error", "message": "Invalid data"})
    except DBAPIError:
        return HTTPBadRequest(json_body={"status": "error", "message": "Database error"})


def validate_user(email, password):
    user = DBSession.query(User).filter_by(email=email).first()
    if user and check_password(password, user.hashed_password):
        return user
    return None  # or you could raise an exception or return a specific response


def get_user_by_email(email):
    user = DBSession.query(User).filter_by(email=email).first()
    if not user:
        return Response('User not found', status=400)
    return user


def check_password(provided_password, stored_password_hash):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash.encode('utf-8'))


@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    try:
        email = request.json_body.get('email')
        password = request.json_body.get('password')

        if not email or not password:
            return Response('Missing email or password', status=400)

        user = validate_user(email, password)
        if not user:
            return {'message': 'Invalid username or password'}, 400

        # Buat token
        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {"email": email, "exp": expiration}
        token = jwt.encode(payload, "qwert123", algorithm="HS256")

        return {'token': token}

    except SQLAlchemyError as e:
        return Response('Database error: ' + str(e), status=500)
