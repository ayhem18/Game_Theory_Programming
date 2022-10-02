from input_output import IO
from SOLVE import SpoilerBot
from SOLVE import Solver
from datetime import datetime


class Game:
    GAME_OVER = "GAME_OVER"
    USER_WIN = "YOU WIN!!!"
    SPOILER_WIN = "SPOILER WINS"
    SPOILER = "spoiler"
    DUPLICATOR = "duplicator"

    @classmethod
    def date_to_feats(cls, day, month, year):
        return day + month, day + month + year

    def __init__(self, day, month, year, mode, start_pos):
        self.step, self.limit = Game.date_to_feats(day, month, year)
        self.start_pos = start_pos
        self.mode = mode

        self.solver = Solver(1, self.step, self.limit)
        w0 = set(list(range(self.limit - self.step, self.limit)))
        self.bot = SpoilerBot(self.mode, self.step, self.limit, self.solver.final_positions(w0))
        self.log = str(datetime.now())
        # add the game information to the file
        self.initiate_log()

    def initiate_log(self):
        with open(self.log, 'a') as f:
            f.write(f"Game started at {self.log}\n")
            f.write(f"step: {str(self.step)}\n")
            f.write(f"range: [1, {self.limit}]\n")
            f.write(f"starting position: {str(self.start_pos)}\n")
            f.write(f"Duplicator's mode: {self.mode}\n")
            f.write(f"Game's log: \n\n")

    def play(self):
        current_pos = self.start_pos

        while True:
            current_pos += IO.get_duplicator_move(current_pos, self.step, self.limit, self.log)
            IO.print_separator()
            if IO.verify_end_game(current_pos, self.limit, self.DUPLICATOR, self.log):
                break
            current_pos += IO.get_spoiler_move(self.bot, current_pos, self.log)
            IO.print_separator()
            if IO.verify_end_game(current_pos, self.limit, self.SPOILER, self.log):
                break

        IO.inspect_log(self.log)


def main():
    IO.welcome()
    IO.print_separator()
    want_to_play = True
    while want_to_play:
        # get the date from the user
        d, m, y = IO.get_date()
        IO.print_separator()
        # get the mode from the user
        mode = IO.get_mode()
        IO.print_separator()
        # convert the date values to the features needed: step and limit
        step, lim = Game.date_to_feats(d, m, y)
        # get the starting position
        start_pos = IO.get_start_pos(1, lim)
        IO.print_separator()
        # initiate a game Object
        game = Game(d, m, y, mode, start_pos)
        # play the game
        game.play()
        IO.print_separator()
        # set if the user want to play again
        want_to_play = IO.play_again()

    # say goodbye to user
    IO.goodbye_user()


if __name__ == "__main__":
    main()
