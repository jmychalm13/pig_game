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
        "final_turn": False,
        "turns_left": players,
        "turn_taken": [False] * players,
    }


def roll_dice(state):
    value = roll()
    if value == 1:
        state["current_score"] = 0
        state["turn_taken"][state["current_player"]] = True
        state = advance_turn(state)
        return state, value
    else:
        state["current_score"] += value
        return state, value


def advance_turn(state):
    next_player = (state["current_player"] + 1) % state["players"]
    state["turn_taken"][state["current_player"]] = True

    while state["turn_taken"][next_player]:
        next_player = (next_player + 1) % state["players"]
        if next_player == state["current_player"]:
            state["turn_taken"] = [False] * state["players"]
            break

    state["current_player"] = next_player
    return state


def end_turn(state):
    state["scores"][state["current_player"]] += state["current_score"]
    state["current_score"] = 0

    if (
        state["scores"][state["current_player"]] >= MAX_SCORE
        and not state["final_turn"]
    ):
        state["final_turn"] = True

    if state["final_turn"]:
        state["turns_left"] -= 1
        if state["turns_left"] == 0:
            state["winner"] = determine_winner(state["scores"])

    state = advance_turn(state)
    return state


def determine_winner(scores):
    eligible_scores = [score for score in scores if score >= MAX_SCORE]
    if not eligible_scores:
        return None
    max_score_above_max = max(eligible_scores)
    for i, score in enumerate(scores):
        if score == max_score_above_max:
            return i
    return None


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
            "winner": state["winner"],
        }
    )


@app.route("/end-turn", methods=["POST"])
def end_turn_route():
    state = session.get("game_state", None)
    if not state:
        return jsonify({"error": "Game state not found"}), 400

    state = end_turn(state)
    session["game_state"] = state

    return jsonify(
        {
            "current_player": state["current_player"],
            "scores": state["scores"],
            "winner": state["winner"],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
