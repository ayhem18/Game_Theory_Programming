def next_final_positions(min_position: int, step: int, w_current: set):
    """This function performs one step in the backward induction: it finds the final positions
    out of the current final positions

    Args:
        min_position (int): the minimal position in the valid range
        step (int): the maximal value of a step
        w_current (list): the current  final positions
    """
    # a range of values including the theoretically possible values
    # new_pos_final = range(max(min(w_current) - 2 * step, min_position), max(w_current) - 1)
    new_pos_final = range(max(w_current) - 2, max(min(w_current) - 2 * step, min_position) - 1, -1)
    # remove elements that are already final positions
    new_pos_final = [x for x in new_pos_final if x not in w_current]

    new_final = []  # list to save the new final positions

    # iterate through the new possible final positions
    for pos in new_pos_final:
        # iterate through the possible first steps:
        for i in range(1, step + 1):
            # proceed only if the intermediate position is not a final position
            if pos + i not in w_current:
                add = True  # a flag to know whether to add the position or not.

                # check that all moves the 2nd player make would put the first player in a winning position
                for j in range(1, step + 1):
                    if pos + i + j not in w_current:
                        # if this condition is false, this means that the second player can put the first player
                        # in a non-final position
                        add = False
                        break

                if add:
                    new_final.append(pos)
                    # the existence of a single "i" is sufficient, break form the loop
                    break
    return new_final


def final_positions(min_position: int, step: int, w0: set):
    """This

    Args:
        min_position (int): _description_
        step (int): _description_
        w0 (list): _description_
    """
    w = w0.copy()
    next_w = next_final_positions(min_position, step, w)
    i = 0
    while True:
        w.update(next_w)
        if not next_w:
            break
        i += 1
        # print(f"W{str(i)}: +{str(w)}")
        next_w = next_final_positions(min_position, step, w)
    # return 'w' the variable saving all the final positions
    return w


def initiate_game(day: int, month: int, year: int):
    # the limit value
    limit = day + month + year
    # the step:
    step = day + month
    # initial final positions: positions that from which the limit value can be reached within only one step
    w0 = set(list(range(limit - step, limit)))
    f_p = final_positions(1, step, w0)

    return step, limit, w0, f_p
