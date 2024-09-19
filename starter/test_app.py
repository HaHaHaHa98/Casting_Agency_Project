import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Actor, Movie, setup_db
from settings import CASTING_ASSISTANT, CASTING_DIRECTOR, DATABASE_TEST_URL, EXECUTIVE_PRODUCER


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = DATABASE_TEST_URL

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def get_headers(self, role):
        """Helper function to get Auth0 token based on role."""
        tokens = {
            "assistant": f"Bearer {CASTING_ASSISTANT}",
            "director": f"Bearer {CASTING_DIRECTOR}",
            "producer": f"Bearer {EXECUTIVE_PRODUCER}"
        }
        return {'Authorization': tokens[role]}

    # Test for casting assistant
    def test_retreive_movies_for_casting_assistant(self):
        res = self.client().get("/movies", headers=self.get_headers('assistant'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])
        self.assertTrue(len(data["movies"]))

    def test_retreive_actors_for_executive_producer(self):
        res = self.client().get("/actors", headers=self.get_headers('assistant'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])
        self.assertTrue(len(data["actors"]))

    # Test for casting director
    def test_update_movies_for_casting_director(self):
        movie = Movie.query.first()
        res = self.client().patch(f"/movies/{movie.id}", json={
            "genre": "Fantasy",
            "rating": 9,
        }, headers=self.get_headers('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["movie"])

    def test_update_actors_for_casting_director(self):
        actor = Actor.query.first()
        res = self.client().patch(f"/actors/{actor.id}", json={
            "gender": "Female",
        }, headers=self.get_headers('director'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    # Test for casting director
    def test_retreive_movies_for_executive_producer(self):
        res = self.client().get("/movies", headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])
        self.assertTrue(len(data["movies"]))

    # def test_404_if_retreive_movies_not_allowed_for_executive_producer(self):
    #     res = self.client().get("/movies/100", headers=self.get_headers('producer'))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    def test_create_movies_for_executive_producer(self):
        res = self.client().post("/movies", json={
            "title": "Spirited Away",
            "genre": "Animation, Fantasy",
            "rating": 8.6,
            "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts."
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["movie"])

    def test_400_if_movie_creation_not_allowed_for_executive_producer(self):
        res = self.client().post("/movies", json={
            "rating": '',
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_update_movies_for_executive_producer(self):
        movie = Movie.query.first()
        res = self.client().patch(f"/movies/{movie.id}", json={
            "genre": "Fantasy",
            "rating": 9,
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["movie"])

    def test_404_if_movie_update_not_allowed_for_executive_producer(self):
        movie = Movie.query.first()
        res = self.client().patch(f"/movies/{movie.id}", json={
            "rating": "",
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movies_for_executive_producer(self):
        movie = Movie.query.first()
        res = self.client().delete(
            f"/movies/{movie.id}", headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_if_movie_deletion_not_allowed_for_executive_producer(self):
        res = self.client().delete("/movies/1000", headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_retreive_actors_for_executive_producer(self):
        res = self.client().get("/actors", headers=self.get_headers('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])
        self.assertTrue(len(data["actors"]))

    def test_create_actors_for_executive_producer(self):
        res = self.client().post("/actors", json={
            "name": "Keanu Reeves",
            "year_of_birth": 1964,
            "gender": "Male",
            "nationality": "Beirut, Lebanon",
            "bio": "Keanu Reeves is a Canadian actor, producer, and musician."
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["actor"])

    def test_400_if_actor_creation_not_allowed_for_executive_producer(self):
        res = self.client().post("/actors", json={
            "name": "Keanu Reeves",
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_update_actors_for_executive_producer(self):
        actor = Actor.query.first()
        res = self.client().patch(f"/actors/{actor.id}", json={
            "gender": "Female",
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_if_movie_update_not_allowed_for_executive_producer(self):
        res = self.client().patch("/actors/1000", json={
            "name": "Keanu Reeves",
        }, headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actors_for_executive_producer(self):
        actor = Actor.query.first()
        res = self.client().delete(
            f"/actors/{actor.id}", headers=self.get_headers('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["deleted"], actor.id)

    def test_404_if_movie_delete_not_allowed_for_executive_producer(self):
        res = self.client().delete("/actors/1000", headers=self.get_headers('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
