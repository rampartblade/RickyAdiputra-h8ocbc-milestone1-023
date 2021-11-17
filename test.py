from unittest import result
from app import connex_app
import unittest

BASE_DIRECTORS_URL = 'api/director'
BASE_MOVIES_URL = 'api/movie'

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        connex_app.app.testing = True
        self.app = connex_app.app.test_client()

    def test_get_all_director(self):
        result = self.app.get('/api/director')
        #Make your assertions
        self.assertEqual(result.status_code, 200)

    def test_get_director_by_Id_false(self):
        result = self.app.get('/api/director/-2000')
        self.assertEqual(result.status_code, 404)

    def test_get_director_by_Id_true(self):
        result = self.app.get('/api/director/4762')
        self.assertEqual(result.status_code,200)

    def test_get_director_by_name_true(self):
        result = self.app.get('api/director/kasdan')
        self.assertEqual(result.status_code, 200)

    def test_get_director_by_name_false(self):
        result = self.app.get('api/movie/a11a')
        self.assertEqual(result.status_code, 404)

    def test_delete_director_false(self):
        result = self.app.delete('/api/director/-1')
        self.assertEqual(result.status_code, 404)

    def test_get_all_movie(self):
        result = self.app.get('/api/movie')
        self.assertEqual(result.status_code, 200)

    def test_get_movie_by_Id_false(self):
        result = self.app.get('/api/director/-1/movie/-1')
        self.assertEqual(result.status_code, 404)

    def test_get_movie_by_Id_true(self):
        result = self.app.get('/api/director/4762/movie/43597')
        self.assertEqual(result.status_code, 200)

    def test_get_movie_by_title_true(self):
        result = self.app.get('api/movie/Pirate')
        self.assertEqual(result.status_code, 200)

    def test_get_movie_by_title_false(self):
        result = self.app.get('api/movie/aaaaaa')
        self.assertEqual(result.status_code, 404)

    def test_delete_movie_false(self):
        result = self.app.delete('/api/director/-1/movie/-1')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()