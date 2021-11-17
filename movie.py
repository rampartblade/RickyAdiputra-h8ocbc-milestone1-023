from flask import make_response, abort, jsonify
from flask.json import tojson_filter
from config import db
from models import Directors, DirectorsSchema, Movies, MoviesPostSchema, MoviesSchema

def read_all(): #get all data
    """
    This function responds to a request for /api/movie
    with the complete list of movies 
    :return:                json list of all movies for all director
    """
    movie_item = Movies.query.order_by(Movies.id).limit(10) #.all() ==> untuk mengambil semua data, diganti limit untuk sementara karena data yang diambil terlalu banyak
    movie_Schema = MoviesSchema(many = True)
    data = movie_Schema.dump(movie_item)

    if len(data) == 0:
        return abort(404,f"Database empty")
    
    return data

def read_one(director_id, movie_id): # read one data
    """
    This function responds to a request for
    /api/director/{director_id}/movie/{movie_id}
    with one matching movie for the associated director by id

    :param director_id:       Id of director the movie is related to
    :param movie_id:         Id of the movie
    :return:                json string of note contents
    """
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

def read_one_name(movie_title): # read one data
    """
    This function responds to a request for
    /api/director/{director_id}/movie/{movie_id}
    with one matching movie for the associated director by id

    :param director_id:       Id of director the movie is related to
    :param movie_id:         Id of the movie
    :return:                json string of note contents
    """
    movie = Movies.query.filter(Movies.title.like(f'%{movie_title}%')).all()

    if movie is not None:
        movie_Schema = MoviesSchema(many=True)
        data = movie_Schema.dump(movie)
        
        if len(data) == 0:
            return abort(404,f"Movie not found for title: {movie_title}")

        return data
    else:
        abort(404, f"Movie not found for movie title: {movie_title}")

def create(director_id, movie):
    """
    This function creates a new movie related to the passed in director id.

    :param director_id:       Id of the director the movie is related to
    :param movie:            The JSON containing the movie data
    :return:                201 on success
    """

    budget = movie.get("budget")
    original_title = movie.get("original_title")
    overview = movie.get("overview")
    popularity = movie.get("popularity")
    release_date = movie.get("release_date")
    revenue = movie.get("revenue")
    tagline = movie.get("tagline")
    title = movie.get("title")
    uid = movie.get("uid")
    vote_average = movie.get("vote_average")
    vote_count = movie.get("vote_count")

    if budget is None or budget is 0:
        abort(409, 'field budget is invalid or required')    

    if original_title is None or original_title is '':
        abort(409, 'field original_title is invalid or required')

    if overview is None or overview is '':
        abort(409, 'field overview is invalid or required')

    if popularity is None or popularity is 0:
        abort(409, 'field popularity is invalid or required')
        
    if release_date is None or release_date is '':
        abort(409, 'field release_date is invalid or required')
        
    if revenue is None or revenue is '':
        abort(409, 'field revenue is invalid or required')
        
    if tagline is None or tagline is '':
        abort(409, 'field tagline is invalid or required')
        
    if title is None or title is '':
        abort(409, 'field title is invalid or required')
        
    if uid is None or uid is 0:
        abort(409, 'field uid is invalid or required')
        
    if vote_average is None or vote_average is 0:
        abort(409, 'field vote_average is invalid or required')
    
    if vote_count is None or vote_count is 0:
        abort(409, 'field vote_count is invalid or required')

    director = Directors.query.filter(Directors.id == director_id).one_or_none()
    
    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    movie_Schema = MoviesPostSchema()
    new_Movie = movie_Schema.load(movie, session=db.session)

    director.movies.append(new_Movie)
    db.session.commit()

    data = movie_Schema.dump(new_Movie)
    return data,201

def update(director_id, movie_id, movie):
    """
    This function updates an existing movie related to the passed in
    director id.

    :param director_id:       Id of the director the movie is related to
    :param movie_id:         Id of the movie to update
    :param movie:            The JSON containing the movie data
    :return:                200 on success
    """
    
    budget = movie.get("budget")
    original_title = movie.get("original_title")
    overview = movie.get("overview")
    popularity = movie.get("popularity")
    release_date = movie.get("release_date")
    revenue = movie.get("revenue")
    tagline = movie.get("tagline")
    title = movie.get("title")
    uid = movie.get("uid")
    vote_average = movie.get("vote_average")
    vote_count = movie.get("vote_count")

    if budget is None or budget is 0:
        abort(409, 'field budget is invalid or required')    

    if original_title is None or original_title is '':
        abort(409, 'field original_title is invalid or required')

    if overview is None or overview is '':
        abort(409, 'field overview is invalid or required')

    if popularity is None or popularity is 0:
        abort(409, 'field popularity is invalid or required')
        
    if release_date is None or release_date is '':
        abort(409, 'field release_date is invalid or required')
        
    if revenue is None or revenue is '':
        abort(409, 'field revenue is invalid or required')
        
    if tagline is None or tagline is '':
        abort(409, 'field tagline is invalid or required')
        
    if title is None or title is '':
        abort(409, 'field title is invalid or required')
        
    if uid is None or uid is 0:
        abort(409, 'field uid is invalid or required')
        
    if vote_average is None or vote_average is 0:
        abort(409, 'field vote_average is invalid or required')
    
    if vote_count is None or vote_count is 0:
        abort(409, 'field vote_count is invalid or required')

    update_movie = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    if update_movie is not None:
        movie_Schema = MoviesPostSchema()
        update = movie_Schema.load(movie, session=db.session)

        update.director_id = update_movie.director_id
        update.id = update_movie.id

        db.session.merge(update)
        db.session.commit()

        data = movie_Schema.dump(update_movie)

        return data,200

    else:
        abort(404, f"Movie not found for Id: {movie_id}")

def delete(director_id, movie_id):
    """
    This function deletes a movie from the movie structure

    :param director_id:   Id of the director the movie is related to
    :param movie_id:     Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    
    movie= (        
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            f"Movie {movie_id} deleted"
        )

    else:
        abort(404, f"Movie not found for Id: {movie_id}")