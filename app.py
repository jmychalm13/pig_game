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
        "final_turn": False,  # Flag to indicate the final turn of the game
        "turns_left": players,  # Number of turns left in the final round
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
        state["final_turn"] = True

    if state["final_turn"]:
        state["turns_left"] -= 1
        if state["turns_left"] == 0:
            state["winner"] = determine_winner(state["scores"])
    else:
        state["current_player"] = (state["current_player"] + 1) % state["players"]

    return state


def determine_winner(scores):
    # Find scores that are above MAX_SCORE
    eligible_scores = [score for score in scores if score >= MAX_SCORE]

    if not eligible_scores:
        return None  # No player has reached or exceeded MAX_SCORE

    # Find the highest score among those who exceeded MAX_SCORE
    max_score_above_max = max(eligible_scores)

    # Find the player with the highest score above MAX_SCORE
    for i, score in enumerate(scores):
        if score == max_score_above_max:
            print(f"i:{i} score:{score}")
            return i

    return None  # Fallback, although it should not reach here in a well-formed game


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
