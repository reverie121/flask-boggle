from unittest import TestCase
from flask import jsonify
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
            self.assertEqual(resp.status_code, 302)

    def test_gameboard(self):
        with app.test_client() as client:
            client.get('/') # DELETE ME WHEN SESSION FUNCTIONALITY ADDED
            resp = client.get('/gameboard')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<table id="gameboard">', html)

    def test_make_guess(self):
        with app.test_client() as client:
            client.get('/') # DELETE ME WHEN SESSION FUNCTIONALITY ADDED
            client.get('/gameboard')
            resp1 = client.get('/make-guess?guess=asdf')
            resp_str1 = resp1.get_data(as_text=True)
            resp2 = client.get('/make-guess?guess=wordy')
            resp_str2 = resp2.get_data(as_text=True)
            self.assertEqual(resp1.status_code, 200)
            self.assertEqual('"not-word"\n', resp_str1)
            self.assertEqual('"not-on-board"\n', resp_str2)