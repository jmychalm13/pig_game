from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from pig import initialize_game, roll_dice, end_turn

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-game", methods=["POST"])
def start_game():
    players = request.form.get("players")
    if players is None:
        return jsonify(error="Missing 'players' parameter"), 400
    try:
        players = int(players)
    except ValueError:
        return jsonify(error="Invalid 'players' parameter, must be an integer"), 400
    # initialize game state
    session["game_state"] = initialize_game(players)

    return redirect(url_for("game"))

@app.route("/game")
def game():
    if "game_state" not in session:
        return redirect(url_for("index"))
    
    players = session["game_state"]["players"]
    return render_template("game.html", players=players)

@app.route("/roll-dice", methods=["POST"])
def roll_dice_route():
    if "game_state" not in session:
        return jsonify(error="Game not started"), 400
    
    message, session["game_state"] = roll_dice(session["game_state"])
    return jsonify(message=message)

@app.route("/end-turn", methods=["POST"])
def end_turn_route():
    if "game_state" not in session:
        return jsonify(error="Game not started"), 400
    
    message, session["game_state"] = end_turn(session["game_state"])
    return jsonify(message=message)

if __name__ == "__main__":
    app.run(debug=True)