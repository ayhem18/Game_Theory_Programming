import random


class Solver:
    # there is no class attributes
    def __init__(self, min_pos: int, step: int, limit: int):
        self.min_pos = min_pos
        self.step = step
        self.limit = limit

    def next_final_positions(self, w_current):
        """This function performs one step in the backward induction: it finds the final positions
        out of the current final positions.
        param w_current: the last set of final positions
        :return: the new set of final positions after one step of backward induction
        """
        # theoretically, the next final positions produced out of the current ones must be reachable
        # in at most two steps. Thus, theoretically they belong to the interval specified below
        new_pos_final = range(max(w_current) - 2, max(min(w_current) - 2 * self.step, self.min_pos) - 1, -1)
        # remove elements that are already final positions
        new_pos_final = [x for x in new_pos_final if x not in w_current]
        new_final = []  # list to save the new final positions
        # iterate through the new possible final positions
        for pos in new_pos_final:
            # iterate through the possible first steps:
            for i in range(1, self.step + 1):
                # proceed only if the intermediate position is not a final position
                if pos + i not in w_current:
                    add = True  # a flag to know whether to add the position or not.

                    # check that all moves the 2nd player make would put the first player in a winning position
                    for j in range(1, self.step + 1):
                        if pos + i + j not in w_current:
                            # if this code block is executed, it means a move "i" from the first player and
                            # a move "j" from the 2nd player, the 1st player will be in a non-final position
                            add = False
                            break
                    if add:
                        new_final.append(pos)  # the existence of a single "i" is sufficient, break form the loop
                        break
        return new_final

    def final_positions(self, w0: set):
        """
        This function finds the complete set of final positions using the values
        1. min_pos: the minimum valid position
        2. step: the maximum value a position can increase in a single turn
        3. limit: the limit value
        :param w0:
        :return: the set of all final positions for the general described problem.
        """
        # make a copy of the initial set of final positions
        w = w0.copy()
        next_w = self.next_final_positions(w)
        i = 0
        while True:
            # add the newly found final positions to the set of all final positions
            w.update(next_w)
            # stop only when the backward induction does not generate new final positions
            if not next_w:
                break
            i += 1
            # print(f"W{str(i)}: +{str(w)}")
            next_w = self.next_final_positions(w)
        # return 'w' the variable saving all the final positions
        return w


RANDOM = 'random'
SMART = 'smart'
ADVISOR = 'advisor'


class SpoilerBot:
    modes = [SMART, RANDOM, ADVISOR]

    @staticmethod
    def set_mode(mode: str):
        if mode.strip().lower() in SpoilerBot.modes:
            return mode
        return SMART

    def __init__(self, mode: str, step: int, limit: int, final_positions: set):
        self.step = step
        self.limit = limit
        self.final_positions = final_positions
        self.mode = SpoilerBot.set_mode(mode)

    def __spoiler_random(self, current_pos: int):
        """
        This method returns a random move in the possible range
        :param current_pos: the current position
        :return: a random number that will keep the position in the valid range.
        """
        # determine the range of possible values
        possible_values = (list(range(1, min(self.limit - current_pos, self.step) + 1)))
        return random.choice(possible_values)

    def __find_next_optimal_move(self, current_pos: int):
        found = True
        for i in range(1, self.step + 1):
            if current_pos + i not in self.final_positions:
                for j in range(1, min(self.limit - current_pos - i, self.step) + 1):
                    if current_pos + i + j not in self.final_positions:
                        found = False
                        break
                if found:
                    return current_pos + i
        # try:
        #     assert found
        # except AssertionError as msg:
        #     print("YOUR FINAL POSITIONS ARE WRONG !!!")
        #     print(msg)

    def __spoiler_smart(self, current_pos: int):
        """
        This method plays randomly if the current position is not favorable, and follows
        a winning strategy otherwise
        :param current_pos: the current position
        :return: either a random move, if the current position is not final position, otherwise
        the move putting the opponent in non-final position
        """
        # check if the current position is a final position
        # if it is not the next move is random
        if current_pos not in self.final_positions:
            return self.__spoiler_random(current_pos)
        else:
            # find the next final position
            return self.__find_next_optimal_move(current_pos) - current_pos

    def __give_advice(self, current_pos: int):
        """
        This method makes a random move for the spoiler anc calculates the winning position that the user
        should move to as part of a winning strategy.
        param current_pos: the current position
        :return: a tuple: the random_move, and the next position the duplicator should move to.
        """
        move = self.__spoiler_random(current_pos)
        user_move = self.__find_next_optimal_move(current_pos + move)
        return move, user_move

    def __spoiler_advisory(self, current_pos: int):
        """
        This method puts two parts together, if the spoiler can win it plays smart.
        Otherwise, it advises the user on their best next move.
        param current_pos: current position
        """
        if current_pos not in self.final_positions:
            return self.__give_advice(current_pos)
        else:
            return self.__spoiler_smart(current_pos)

    def spoiler_play(self, current_pos: int):
        move = None
        if self.mode == SMART:
            move = self.__spoiler_smart(current_pos)

        elif self.mode == RANDOM:
            move = self.__spoiler_random(current_pos)

        elif self.mode == ADVISOR:
            move = self.__spoiler_advisory(current_pos)

        return move
