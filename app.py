from flask import Flask, render_template, redirect, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = "do*not*tell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

def session_update():
    """ Updates session data for games played and high score """
    session['games_played'] = boggle_game.games_played
    session['high_score'] = boggle_game.high_score

@app.route('/')
def render_index():
    return redirect('/gameboard')

def check_for_board():
    """ Check session storage to see if there is a currently valid board.
        If not, create a new board and add to session storage. """
    if not session.get('board'):
        boggle_game.board = boggle_game.make_board()
        session['board'] = boggle_game.board

@app.route('/gameboard')
def render_gameboard():
    check_for_board()
    session_update()
    return render_template('gameplay.html', board = session['board'], games_played = session['games_played'], high_score = session['high_score'])

@app.route('/make-guess')
def return_guess():
    response = boggle_game.check_valid_word(session['board'], request.args['guess'])
    return jsonify(response)

@app.route('/end-game', methods=['POST'])
def get_endgame_score():
    # increments games played total by 1
    boggle_game.games_played += 1
    # updates score array and high score
    new_score = request.json['score']
    boggle_game.scores.append(new_score)
    boggle_game.high_score = max(boggle_game.scores)
    # should update original jinja gameboard template via passed in args
    return redirect('/post-game')

@app.route('/post-game')
def show_endgame():
    return render_template('gameover.html', board = session['board'], games_played = session['games_played'], high_score = session['high_score'])