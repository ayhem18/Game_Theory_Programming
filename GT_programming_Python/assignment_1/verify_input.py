import random

RANDOM = 'random'
SMART = 'smart'
ADVISOR = 'advisor'
modes = [SMART, RANDOM, ADVISOR]


def get_starting_pos(min_position: int, limit: int):
    invalid = True
    start_pos = None
    while invalid:
        start_pos = input(f"Please enter the term '{RANDOM}' for a random starting position or enter a starting "
                          f"position between: "
                          f"{str(min_position)} (inclusive) and {str(limit)} (exclusive)\n")
        try:
            invalid = int(start_pos) not in range(min_position, limit)
        except (TypeError, ValueError):
            if start_pos.strip().lower() != RANDOM:
                invalid = True
            else:
                # return a random value between min position (inclusive) and limit (exclusive)
                return random.choice(range(min_position, limit))
    return int(start_pos)


def get_mode():
    invalid = True
    user_mode = None
    while invalid:
        user_mode = input(f"Please enter the mode of your choice: {str(modes)}\n")
        invalid = user_mode.strip().lower() not in modes

    return user_mode


def get_move(current_pos: int, step: int, limit: int):
    invalid = True
    move = None
    while invalid:

        print(f"current position {str(current_pos)}")
        print(f"step's size: {str(step)}")
        print(f"limit value : {str(limit)}")
        max_move = min(limit - current_pos, step)
        i = input(f"Please enter a step value between 1 and {str(max_move)} (inclusive)\n")
        try:
            move = int(i)
        except (TypeError, ValueError):

            continue
        invalid = move not in range(1, max_move + 1)
    return move

#
# if __name__ == "__main__":
#     get_move(1, 20, 2001)
#
