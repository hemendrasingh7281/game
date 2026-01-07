

import random
from dataclasses import dataclass
from typing import Optional, Literal


def tool(fn):
    fn.is_tool = True
    return fn


@dataclass
class GameState:
    round_number: int = 0
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    game_over: bool = False



@tool
def validate_move(move: str, bomb_used: bool) -> bool:
    valid_moves = {"rock", "paper", "scissors", "bomb"}
    if move not in valid_moves:
        return False
    if move == "bomb" and bomb_used:
        return False
    return True


@tool
def resolve_round(user_move: str, bot_move: str) -> Literal["user", "bot", "draw"]:
    if user_move == bot_move:
        return "draw"
    if user_move == "bomb":
        return "user"
    if bot_move == "bomb":
        return "bot"

    rules = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }
    return "user" if rules[user_move] == bot_move else "bot"


@tool
def update_game_state(state: GameState, winner: Optional[str]) -> None:
    state.round_number += 1
    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1

    if state.round_number >= 3:
        state.game_over = True



class RefereeAgent:
    def __init__(self):
        self.state = GameState()

    def explain_rules(self):
        print(
            "\nRules:\n"
            "- Best of 3 rounds\n"
            "- Moves: rock, paper, scissors, bomb (once)\n"
            "- Bomb beats all; bomb vs bomb = draw\n"
            "- Invalid input wastes the round\n"
        )

    def get_bot_move(self):
        moves = ["rock", "paper", "scissors"]
        if not self.state.bot_bomb_used:
            moves.append("bomb")
        return random.choice(moves)

    def play_round(self, user_input: str):
        if self.state.game_over:
            return

        user_move = user_input.strip().lower()
        valid = validate_move(user_move, self.state.user_bomb_used)
        bot_move = self.get_bot_move()

        if user_move == "bomb":
            self.state.user_bomb_used = True
        if bot_move == "bomb":
            self.state.bot_bomb_used = True

        print(f"\nRound {self.state.round_number + 1}")

        if not valid:
            print("Invalid input. Round wasted.")
            update_game_state(self.state, None)
            return

        winner = resolve_round(user_move, bot_move)
        update_game_state(self.state, winner)

        print(f"You played: {user_move}")
        print(f"Bot played: {bot_move}")
        print(f"Winner: {winner.upper()}")

    def conclude(self):
        print("\n=== GAME OVER ===")
        print(f"Final Score → You: {self.state.user_score} | Bot: {self.state.bot_score}")
        if self.state.user_score > self.state.bot_score:
            print("YOU WIN 🎉")
        elif self.state.bot_score > self.state.user_score:
            print("BOT WINS 🤖")
        else:
            print("DRAW 🤝")



def run_game():
    print("ROCK-PAPER-SCISSORS-PLUS REFEREE")
    print("=" * 44)

    agent = RefereeAgent()
    agent.explain_rules()

    while not agent.state.game_over:
        move = input("Enter your move: ")
        agent.play_round(move)

    agent.conclude()


if __name__ == "__main__":
    run_game()
s
