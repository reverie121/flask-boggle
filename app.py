from flask import Flask, render_template, redirect, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = "do*not*tell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def render_index():
    return render_template('welcome.html')

def check_for_board():
    """ Check session storage to see if there is a currently valid board.
        If not, initialize session storage. """
    if not session.get('board'):
        boggle_game = Boggle()
        session['board'] = boggle_game.make_board()
        session['games_played'] = 0
        session['high_score'] = 0

@app.route('/play')
def render_gameboard():
    """ Looks for a current game, makes a new one if needed, and then renders the gameplay template. """
    check_for_board()
    return render_template('gameplay.html', board = session['board'], games_played = session['games_played'], high_score = session['high_score'])

@app.route('/make-guess')
def return_guess():
    """ Checks word submission for validity."""
    response = boggle_game.check_valid_word(session['board'], request.args['guess'])
    return jsonify(response)

@app.route('/end-game', methods=['POST'])
def get_endgame_score():
    """ Updates session data and redirects to start a new game. """
    session['games_played'] += 1
    new_score = int(request.form.get('score'))
    high_score = int(session['high_score'])
    if new_score > high_score:
        session['high_score'] = new_score
    return redirect('/new-game')

@app.route('/new-game')
def show_endgame():
    """ Sets up a new game with a new board. """
    boggle_game.set_up_game()
    session['board'] = boggle_game.make_board()
    return render_template('gameplay.html', board = session['board'], games_played = session['games_played'], high_score = session['high_score'])