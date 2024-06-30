import random


def roll():
    min_value = 1
    max_value = 6
    roll = random.randint(min_value, max_value)

    return roll

def play_turn(player_idx, player_scores):
    # simulates single turn for single player
    print(f"Player {player_idx + 1}'s turn.")
    print(f"Your total score is: {player_scores[player_idx]}")

    current_score = 0
    while True:
        should_roll = input("Would you like to roll? (y/n): ").lower()
        if should_roll != "y":
            break
        value = roll()
        if value == 1:
            print("You rolled a 1! Turn done!")
            current_score = 0
            break
        else:
            current_score += value
            print(f"You rolled a: {value}")
            print(f"Your score for this turn is: {current_score}")
    player_scores[player_idx] += current_score
    print(f"Your total score is now: {player_scores[player_idx]}")

def play_game(players):
    max_score = 50
    player_scores = [0] * players

    while max(player_scores) < max_score:
        for player_idx in range(players):
            play_turn(player_idx, player_scores)
    winning_score = max(player_scores)
    winning_player = player_scores.index(winning_score) + 1
    print(f"Player {winning_player} wins with a score of {winning_score}!")

if __name__ == "__main__":
    players = int(input("Enter the number of players (2-4): "))
    play_game(players)
