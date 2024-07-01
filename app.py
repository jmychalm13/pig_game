from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pig

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    players = int(request.form['players'])
    state = pig.start_game(players)
    session['game_state'] = state
    return redirect(url_for('game'))

@app.route('/game')
def game():
    state = session.get('game_state', None)
    if not state:
        return redirect(url_for('index'))
    return render_template('game.html', state=state)

@app.route('/roll-dice', methods=['POST'])
def roll_dice():
    state = session.get('game_state', None)
    if not state:
        return jsonify({'error': 'Game state not found'}), 400
    state, value = pig.roll_dice(state)
    session['game_state'] = state
    return jsonify({'value': value, 'current_score': state['current_score']})

@app.route('/end-turn', methods=['POST'])
def end_turn():
    state = session.get('game_state', None)
    if not state:
        return jsonify({'error': 'Game state not found'}), 400
    state = pig.end_turn(state)
    session['game_state'] = state
    if 'winner' in state:
        return jsonify({'winner': state['winner'], 'score': state['scores'][state['winner'] - 1]})
    return jsonify({'next_player': state['current_player'] + 1, 'scores': state['scores']})

if __name__ == '__main__':
    app.run(debug=True)