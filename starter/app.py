import os
from auth import AuthError, requires_auth
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException


from models import Actor, Movie, setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Headers",
                             "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(payload):
        try:
            selection = Movie.query.all()

            movies = [movie.format() for movie in selection]

            if len(selection) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "movies": movies,
                    "total_movies": len(movies)
                }), 200
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        try:
            body = request.get_json()

            title = body.get('title', None)
            genre = body.get('genre', None)
            rating = body.get('rating', None)
            description = body.get('description', None)
            if not title or not genre or not rating or not description:
                abort(400)

            movie = Movie(title=title, genre=genre,
                          rating=rating, description=description)
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except HTTPException as e:
            raise e
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if not movie:
                abort(404)

            body = request.get_json()

            movie.title = body.get('title', movie.title)
            movie.genre = body.get('genre', movie.genre)
            movie.rating = body.get('rating', movie.rating)
            movie.description = body.get('description', movie.description)
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            abort(422)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(payload):
        try: 
            selection = Actor.query.all()

            actors = [actor.format() for actor in selection]

            if len(selection) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "actors": actors,
                    "total_actors": len(actors)
                }), 200
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        try:
            body = request.get_json()

            name = body.get('name', None)
            year_of_birth = body.get('year_of_birth', None)
            gender = body.get('gender', None)
            nationality = body.get('nationality', None)
            bio = body.get('bio', None)

            if not name or not year_of_birth or not gender or not nationality or not bio:
                abort(400)

            actor = Actor(
                name=name,
                year_of_birth=year_of_birth,
                gender=gender,
                nationality=nationality,
                bio=bio)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not actor:
                abort(404)

            body = request.get_json()

            actor.name = body.get('name', actor.name)
            actor.year_of_birth = body.get(
                'year_of_birth', actor.year_of_birth)
            actor.gender = body.get('gender', actor.gender)
            actor.nationality = body.get('nationality', actor.nationality)
            actor.bio = body.get('bio', actor.bio)
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except HTTPException as e:
            raise e
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not actor:
                abort(404)

            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor_id
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}), 404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}), 422,
        )

    @app.errorhandler(AuthError)
    def auth_error(error):
        return (
            jsonify({
                "success": False,
                "error": error.status_code,
                "message": error.error['description']
            }), error.error
        )

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)