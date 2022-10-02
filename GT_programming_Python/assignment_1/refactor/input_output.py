from datetime import datetime
import random
from SOLVE import SpoilerBot


class IO:
    GAME_OVER = "GAME OVER!!"
    WELCOME = "WELCOME TO THE DUPLICATOR-SPOILER GAME \n YOU ARE PLAYING AS THE DUPLICATOR."
    DB_INPUT = "Enter your date of birth in the format dd-mm-yyyy: or default\nThe default birth date: 18-02-2001\t"

    DEF_DAY = 18
    DEF_MONTH = 2
    DEF_YEAR = 2001

    RANDOM = "random"
    ADVISOR = 'advisor'
    SMART = 'smart'

    MODES = [SMART, ADVISOR, RANDOM]

    @classmethod
    def print_separator(cls):
        print()
        print("#" * 50)
        print()

    @classmethod
    def welcome(cls):
        print(cls.WELCOME)

    @classmethod
    def get_date(cls):
        while True:
            user_input = input(cls.DB_INPUT)

            if user_input.strip().lower() == 'default':
                return cls.DEF_DAY, cls.DEF_MONTH, cls.DEF_YEAR

            try:
                db_obj = datetime.strptime(user_input, "%d-%m-%Y")
            except ValueError:
                print("INVALID DATE FORMAT")
                continue

            return db_obj.date().day, db_obj.date().month, db_obj.date().year

    @classmethod
    def explain_starting_pos(cls, min_pos, limit):
        return f"Please enter the term '{cls.RANDOM}' for a random staring position " \
               f"or enter a starting position between: " \
               f"{str(min_pos)} (inclusive) and {str(limit)} (exclusive)\n"

    @classmethod
    def get_start_pos(cls, min_pos, limit):
        while True:
            start_pos = input(cls.explain_starting_pos(min_pos, limit))
            try:
                if int(start_pos) in range(min_pos, limit):
                    return int(start_pos)
            except (TypeError, ValueError):
                if start_pos.strip().lower() != cls.RANDOM:
                    continue
                else:
                    # return a random value between min position (inclusive) and limit (exclusive)
                    return random.choice(range(min_pos, limit))

    @classmethod
    def __explain_modes(cls):
        print("The game offers the following modes:\n")
        print("\t- smart (if possible, the program uses a winning strategy against the user)")
        print("\t- random (the program moves randomly)")
        print("\t- advisor (the program uses a winning strategy if possible, and advises the user otherwise")

    @classmethod
    def get_mode(cls):
        cls.__explain_modes()
        while True:
            user_name = input(f"Please enter the mode of your choice: {str(cls.MODES)}\n")
            if user_name.strip().lower() in cls.MODES:
                return user_name.strip().lower()

    @classmethod
    def __game_state(cls, current_pos: int, step: int, limit: int):
        print(f"current position {str(current_pos)}")
        print(f"step's size: {str(step)}")
        print(f"limit value : {str(limit)}")
        return min(limit - current_pos, step)

    @classmethod
    def __save_duplicator_move(cls, current_pos: int, move: int, log: str):
        with open(log, 'a') as f:
            f.write(f"[Duplicator]: {str(current_pos)}, {str(move)} --> {str(current_pos + move)}\n\n")
            f.close()

    @classmethod
    def get_duplicator_move(cls, current_pos: int, step: int, limit: int, log):
        while True:
            max_move = cls.__game_state(current_pos, step, limit)
            i = input(f"Please enter a step value between 1 and {str(max_move)} (inclusive)\n\n")
            try:
                if int(i) in range(1, max_move + 1):
                    cls.__save_duplicator_move(current_pos, int(i), log)
                    return int(i)
            except (TypeError, ValueError):
                continue

    @classmethod
    def __display_bot_move(cls, move: int, prev_pos: int, log):
        print(f"The program moved from {str(prev_pos)} to {str(prev_pos + move)}")
        with open(log, 'a') as f:
            f.write(f"[Spoiler]: {str(prev_pos)}, {str(move)} --> {str(prev_pos + move)}\n\n")
            f.close()
        print()

    @classmethod
    def __display_bot_advice(cls, bot_move: tuple, log):
        print()
        advice = f"THE BOT LEFT YOU THIS MESSAGE:\nWell ! it seems that you can win this game!!\n" \
                 f"Make sure you move to the position {str(bot_move[1])}"
        print(advice)
        with open(log, 'a') as f:
            f.write(f"[Spoiler's advice]: {advice}\n\n")
            f.close()

    @classmethod
    def get_spoiler_move(cls, bot: SpoilerBot, current_pos: int, log: str):
        bot_move = bot.spoiler_play(current_pos)

        if isinstance(bot_move, tuple):
            cls.__display_bot_move(bot_move[0], current_pos, log)
            cls.__display_bot_advice(bot_move, log)
            return bot_move[0]
        else:
            cls.__display_bot_move(bot_move, current_pos, log)
            return bot_move

    @classmethod
    def verify_end_game(cls, current_pos: int, limit: int, player_name: str, log: str):
        if current_pos == limit:
            print(f"{cls.GAME_OVER}")
            print(f"{player_name} WINS!!")
            print()
            with open(log, 'a') as f:
                f.write(f"{cls.GAME_OVER}\n")
                f.write(f"{player_name} WINS!!\n")
                f.close()

            return True
        return False

    @classmethod
    def inspect_log(cls, log: str):
        print("Would you like to inspect the log of the game?")
        print("Please enter Y if it is the case, and N otherwise")
        choice = input()
        if choice.strip().lower() == 'y':
            cls.print_separator()
            with open(log, 'r') as f:
                for line in f.readlines():
                    print(line, end='')

    @classmethod
    def play_again(cls):
        print("Would you like to play again?")
        print("Please enter Y if it is the case, and N otherwise")
        choice = input()
        return choice.strip().lower() == 'y'

    @classmethod
    def goodbye_user(cls):
        print("IT IS SAD TO SEE YOU LEAVE !!")
        print("COME BACK SOON !!")
