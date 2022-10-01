import random
from verify_input import SMART, RANDOM, ADVISOR
import verify_input as vi
import positions as p

GAME_OVER = "GAME_OVER"
USER_WIN = "YOU WIN!!!"
SPOILER_WIN = "SPOILER WINS"
SPOILER = "spoiler"
DUPLICATOR = "duplicator"

DAY = 18
MONTH = 2
YEAR = 2001


def give_advice(current_pos: int, step: int, limit: int, final_positions: set):
    print("Well ! it seems that you can win this game!!")
    move = spoiler_random(current_pos, step, limit)
    print("My move does not change the fact that you have a winning strategy now !!")
    user_move = find_next_optimal_move(current_pos + move, step, limit, final_positions)
    print(f"I will move to {str(current_pos + move)}. Make sure you move to the position {str(user_move)}")
    return move


def save_log(current_pos: int, move: int, player_name: str, log: dict):
    data = f"{player_name}: ({str(current_pos)}, {str(move)} -> {str(current_pos + move)})"
    if not log:
        log[1] = data
    else:
        last_move = max(list(log.keys()))
        log[last_move + 1] = data


def display_log(log: dict):
    for key, value in log.items():
        print(f"Move number {key}: {value}")


def find_next_optimal_move(current_pos: int, step: int, limit: int, final_positions: set):
    found = True
    for i in range(1, step + 1):
        if current_pos + i not in final_positions:
            for j in range(1, min(limit - current_pos - i, step) + 1):
                if current_pos + i + j not in final_positions:
                    found = False
                    break
            if found:
                return current_pos + i
    try:
        assert found
    except AssertionError as msg:
        print("YOUR FINAL POSITIONS ARE WRONG !!!")
        print(msg)


def spoiler_advisory(current_pos: int, step: int, limit: int, final_positions: set):
    if current_pos not in final_positions:
        return give_advice(current_pos, step, limit, final_positions)
    else:
        return spoiler_smart(current_pos, step, limit, final_positions)


def spoiler_smart(current_pos: int, step: int, limit: int, final_positions: set):
    # check if the current position is a final position
    # if it is not the next move is random
    if current_pos not in final_positions:
        return spoiler_random(current_pos, step, limit)
    else:
        # find the next final position
        return find_next_optimal_move(current_pos, step, limit, final_positions) - current_pos


def spoiler_random(current_pos: int, step: int, limit: int):
    possible_values = (list(range(1, min(limit - current_pos, step) + 1)))
    # print(possible_values)
    move = random.choice(possible_values)

    return move


def spoiler_play(current_pos: int, step: int, limit: int, final_positions: set, mode: str, log: dict):
    move = None
    if mode == SMART:
        move = spoiler_smart(current_pos, step, limit, final_positions)

    elif mode == RANDOM:
        move = spoiler_random(current_pos, step, limit)

    elif mode == ADVISOR:
        move = spoiler_advisory(current_pos, step, limit, final_positions)

    save_log(current_pos, move, SPOILER, log)
    return current_pos + move


def user_play(current_pos: int, step: int, limit: int, log: dict):
    # receive the move's value from the user
    move = vi.get_move(current_pos, step, limit)
    # save to the log of the user
    save_log(current_pos, move, DUPLICATOR, log)
    return current_pos + move


def play(start_pos: int, step: int, limit: int, final_positions: set, mode):
    current_pos = start_pos
    log = {}  # an empty dictionary that will serve as a log for the game
    while True:
        current_pos = user_play(current_pos, step, limit, log)
        if current_pos == limit:
            print(GAME_OVER)
            print(USER_WIN)
            break
        current_pos = spoiler_play(current_pos, step, limit, final_positions, mode, log)

        if current_pos == limit:
            print(GAME_OVER)
            print(SPOILER_WIN)
            break
    
    print("Would you like to inspect the log ?")
    print("Please enter Y if it is the case, and N otherwise")
    choice = input()
    if choice.strip().lower() == 'y':
        display_log(log)


def game():
    step, limit, w0, final_positions = p.initiate_game(DAY, MONTH, YEAR)
    mode = vi.get_mode()
    start_pos = vi.get_starting_pos(1, limit)
    play(start_pos, step, limit, final_positions, mode)


if __name__ == "__main__":
    game()
