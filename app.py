from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random

MAX_SCORE = 25

app = Flask(__name__)
app.secret_key = "your_secret_key"


def roll():
    return random.randint(1, 6)


def start_game(players):
    return {
        "players": players,
        "scores": [0] * players,
        "current_player": 0,
        "current_score": 0,
        "winner": None,
    }


def roll_dice(state):
    value = roll()
    if value == 1:
        state["current_score"] = 0
        end_turn(state)
        return state, value
    else:
        state["current_score"] += value
        return state, value


def end_turn(state):
    state["scores"][state["current_player"]] += state["current_score"]
    state["current_score"] = 0
    if state["scores"][state["current_player"]] >= MAX_SCORE:
        state["winner"] = state["current_player"] + 1
        return state
    else:
        state["current_player"] = (state["current_player"] + 1) % state["players"]
        return state


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start-game", methods=["POST"])
def start_game_route():
    players = int(request.form["players"])
    state = start_game(players)
    session["game_state"] = state
    return redirect(url_for("game"))


@app.route("/game")
def game():
    state = session.get("game_state", None)
    if not state:
        return redirect(url_for("index"))
    return render_template("game.html", state=state)


@app.route("/roll-dice", methods=["POST"])
def roll_dice_route():
    state = session.get("game_state", None)
    if not state:
        return jsonify({"error": "Game state not found"}), 400
    state, value = roll_dice(state)
    session["game_state"] = state
    return jsonify(
        {
            "value": value,
            "current_score": state["current_score"],
            "current_player": state["current_player"],
            "scores": state["scores"],
        }
    )


@app.route("/end-turn", methods=["POST"])
def end_turn_route():
    try:
        state = session.get("game_state")
        if not state:
            return jsonify({"error": "Game state not found"}), 400

        state = end_turn(state)
        session["game_state"] = state

        if "winner" in state and state["winner"] is not None:
            return jsonify(
                {
                    "winner": state["winner"],
                    "score": state["scores"][state["winner"] - 1],
                    "scores": state["scores"],
                }
            )
        else:
            next_player = (state["current_player"] + 1) % state["players"]
            print(
                f"current_player: {state['current_player']} next_player: {next_player}"
            )
            return jsonify(
                {
                    "current_player": state["current_player"],
                    "next_player": next_player,
                    "scores": state["scores"],
                    "winner": None,
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
