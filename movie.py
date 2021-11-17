from flask import make_response, abort
from config import db
from models import Directors, DirectorsSchema, Movies, MoviesSchema

def read_all(): #get all data
    movie_item = Movies.query.order_by(Movies.id).limit(10) #.all() ==> untuk mengambil semua data, diganti limit untuk sementara karena data yang diambil terlalu banyak
    movie_Schema = MoviesSchema(many = True)
    data = movie_Schema.dump(movie_item)
    return data

def read_one(director_id, movie_id): #read one data
    movie = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    if movie is not None:
        movie_Schema = MoviesSchema()
        data = movie_Schema.dump(movie)
        return data

    else:
        abort(404, f"Movie not found for director Id: {director_id} and movie Id: {movie_id}")

def create(director_id, movie):
    director = Directors.query.filter(Directors.id == director_id).one_or_none()

    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    movie_Schema = DirectorsSchema()
    new_Movie = movie_Schema.load(movie, session=db.session)

    director.movies.append(new_Movie)
    db.session.commit()

    data = movie_Schema.dump(new_Movie)
    return data,201

def update(director_id, movie_id, movie):
    update_movie = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    if update_movie is not None:
        movie_Schema = MoviesSchema()
        update = movie_Schema.load(movie, session=db.session)

        update.director_id = update_movie.director_id
        update.movie_id = update_movie.movie_id

        db.session.merge(update)
        db.session.commit()

        data = movie_Schema.dump(update_movie)

        return data,200

    else:
        abort(404, f"Movie not found for Id: {movie_id}")

def delete(director_id, movie_id):
    movie= (        
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {movie_id} deleted", format(movie_id == movie_id)
        )

    else:
        abort(404, f"Movie not found for Id: {movie_id}")