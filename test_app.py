from unittest import TestCase
from flask import jsonify, session
from app import app
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleTestCase(TestCase):
    """  """
    def test_root(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span id="bigger-boggle">Boggle</span>', html)

    def test_play(self):
        with app.test_client() as client:
            resp = client.get('/play')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<table id="gameboard">', html)

    def test_make_guess(self):
        with app.test_client() as client:
            client.get('/play')
            resp1 = client.get('/make-guess?guess=asdf')
            resp_str1 = resp1.get_data(as_text=True)
            resp2 = client.get('/make-guess?guess=wordy')
            resp_str2 = resp2.get_data(as_text=True)
            self.assertEqual(resp1.status_code, 200)
            self.assertEqual('"not-word"\n', resp_str1)
            self.assertEqual('"not-on-board"\n', resp_str2)
    
    def test_end_game_scoring(self):
        with app.test_client() as client:
            client.get('/play')
            resp = client.post('/end-game', data={"score": "21"})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/new-game")

    def test_end_game_render(self):
        with app.test_client() as client:
            client.get('/play')
            resp = client.post('/end-game', data={"score": "21"}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Score Word</button>', html)
            self.assertNotIn('<button>New Game</button>', html)