from flask import Flask, jsonify, render_template, request
from pig import play_game

app = Flask(__name__)

@app.route("/")
def home():
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
    
    play_game(players)
    return jsonify(message="Game finished")

if __name__ == "__main__":
    app.run(debug=True)