#! /usr/bin/usr python3
import random

class Player:
    def __init__(self, name, starting_balance=100):
        self.name = name
        self.balance = starting_balance

    def bet(self, amount):
        if amount > self.balance:
            print(f"{self.name} does not have enough balance to bet that amount!")
            return False
        self.balance -= amount
        return True

    def win_bet(self, amount):
        self.balance += amount

    def is_bankrupt(self):
        return self.balance <= 0

# Function to roll three dice
def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

# Function to determine the score of a roll
def determine_score(roll):
    roll.sort()
    if roll[0] == roll[1] == roll[2]:
        return ('Triple', roll[0], roll)
    if roll == [4, 5, 6]:
        return ('Automatic Win', 0, roll)
    if roll == [1, 2, 3]:
        return ('Automatic Loss', 0, roll)
    if roll[0] == roll[1]:
        return ('Point', roll[2], roll)
    if roll[1] == roll[2]:
        return ('Point', roll[0], roll)
    if roll[0] == roll[2]:
        return ('Point', roll[1], roll)
    return ('No Result', 0, roll)

# Function to play a turn for a player
def player_turn(player):
    print(f"\n{player.name}'s turn:")
    input("Press Enter to roll the dice...")
    while True:
        roll = roll_dice()
        outcome, score, dice = determine_score(roll)
        print(f"Rolled: {dice}")
        if outcome == 'No Result':
            print("No scoring combination. Roll again.")
            input("Press Enter to roll again...")
            continue
        else:
            print(f"{outcome}! {'Score: ' + str(score) if score else ''}")
            return (outcome, score)

# Function to compare scores and determine the winner
def compare_scores(player_scores):
    highest_score = None
    winners = []
    for player, (outcome, score) in player_scores.items():
        if outcome == 'Automatic Loss':
            continue
        if outcome == 'Automatic Win':
            winners = [player]
            break
        if outcome == 'Triple':
            score += 6  # Give higher weight to triples
        if highest_score is None or score > highest_score:
            highest_score = score
            winners = [player]
        elif score == highest_score:
            winners.append(player)
    return winners

# Main game function
def play_cee_lo():
    print("Welcome to Multiplayer Cee-lo with Gambling!")
    
    num_players = int(input("Enter the number of players: "))
    players = []
    
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ")
        players.append(Player(name))
    
    while len(players) > 1:
        # Collect bets from players
        player_bets = {}
        total_pot = 0
        for player in players:
            while True:
                print(f"\n{player.name} has {player.balance} points.")
                try:
                    bet = int(input(f"{player.name}, enter your bet: "))
                    if player.bet(bet):
                        player_bets[player] = bet
                        total_pot += bet
                        break
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # Each player takes a turn
        player_scores = {}
        for player in players:
            outcome, score = player_turn(player)
            player_scores[player] = (outcome, score)
        
        # Determine the winner(s)
        winners = compare_scores(player_scores)
        
        if len(winners) == 0:
            print("\nNo valid score this round. No winners.")
        elif len(winners) == 1:
            winner = winners[0]
            print(f"\n{winner.name} wins the round!")
            winner.win_bet(total_pot)
        else:
            print("\nIt's a tie between: " + ", ".join([player.name for player in winners]))
            split_pot = total_pot // len(winners)
            for winner in winners:
                winner.win_bet(split_pot)
        
        # Remove players who are bankrupt
        players = [player for player in players if not player.is_bankrupt()]
        if len(players) == 1:
            print(f"\n{players[0].name} is the last player standing and wins the game with {players[0].balance} points!")
            break
        elif len(players) == 0:
            print("All players are bankrupt! The game ends with no winner.")
            break

    # Option to play again
    play_again = input("\nDo you want to play another round? (y/n): ").lower()
    if play_again == 'y':
        play_cee_lo()
    else:
        print("Thanks for playing!")

# Start the game
if __name__ == "__main__":
    play_cee_lo()

