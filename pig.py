import random

MAX_SCORE = 50

def roll():
    return random.randint(1, 6)

def start_game(players):
    return {
        'players': players,
        'scores': [0] * players,
        'current_player': 0,
        'current_score': 0
    }

def roll_dice(state):
    value = roll()
    if value == 1:
        state['current_score'] = 0
        end_turn(state)
        return state, value
    else:
        state['current_score'] += value
        return state, value

def end_turn(state):
    state['scores'][state['current_player']] += state['current_score']
    state['current_score'] = 0
    if state['scores'][state['current_player']] >= MAX_SCORE:
        state['winner'] = state['current_player'] + 1
    else:
        state['current_player'] = (state['current_player'] + 1) % state['players']
    return state