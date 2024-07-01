import random

def roll():
    return random.randint(1, 6)

def initialize_game(players):
    return {
        "players": players,
        "player_scores": [0] * players,
        "current_player": 0,
        "current_score": 0
    }

def roll_dice(game_state):
    value = roll()
    if value == 1:
        game_state["current_score"] = 0
        next_turn(game_state)
        return "You rolled a 1! Turn done!", game_state
    else:
        game_state["current_score"] += value
        return f"You rolled a {value}. Your score this turn is {game_state["current_score"]}", game_state
    
def next_turn(game_state):
    game_state["player_scores"][game_state["current_player"]] += game_state["current_score"]
    game_state["current_player"] = (game_state["current_player"] + 1) % game_state["players"]
    game_state["current_score"] = 0

def end_turn(game_state):
    player_scores = game_state["player_scores"]
    current_player = game_state["current_player"]
    current_score = game_state["current_score"]

    player_scores[current_player] += current_score
    game_state["player_scores"] = player_scores

    if max(player_scores) >= 50:
        return f"Player {current_player + 1} wins with a score of {player_scores[current_player]}!", game_state
    
    next_turn(game_state)
    return f"Turn ended.  Player {current_player + 1} total score is {player_scores[current_player]}", game_state