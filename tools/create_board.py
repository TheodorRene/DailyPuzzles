""" numpy library """
import numpy as np
import matplotlib.pyplot as plt

def gen_board(fen):
    """"Generate board"""
    chessboard = np.full((8, 8), 0.35)
    chessboard[1::2, 0::2] = 1
    chessboard[0::2, 1::2] = 1

    arr = gen_array(fen)

    cur_pos = 0
    lastnum = ""
    for y in range(0, len(arr)):
        for x in range(0, len(arr[y])):
            if not arr[y][x].isdigit():
                x_pos = x + cur_pos
                if lastnum.isdigit():
                    cur_pos += int(lastnum)-1
                    x_pos += int(lastnum)-1
                char = get_char(arr[y][x])
                color = "black" if arr[y][x].islower() else "white"
                plt.plot(x_pos-0.05, y, marker=char, markersize=26, color=color, fillstyle='bottom')
            lastnum = arr[y][x]
        cur_pos = 0
        lastnum = ""

    plt.xticks(np.arange(8), ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'))
    plt.yticks(np.arange(8), ('8', '7', '6', '5', '4', '3', '2', '1'))

    plt.imshow(chessboard, cmap="copper", vmin=0, vmax=1)
    plt.savefig('position.png')

def get_char(char):
    """get unicode character"""
    pieces = {
        "r": "$\u265c$",
        "n": "$\u265e$",
        "b": "$\u265d$",
        "q": "$\u265b$",
        "k": "$\u265a$",
        "p": "$\u265f$",
        "R": "$\u2656$",
        "N": "$\u2658$",
        "B": "$\u2657$",
        "Q": "$\u2655$",
        "K": "$\u2654$",
        "P": "$\u2659$",
    }
    return pieces[char]

def gen_array(fen):
    """" Generate array from FEN """

    slash_index = [pos for pos, char in enumerate(fen) if char == '/']
    arr = []
    i = 0
    for el_ in slash_index:
        if slash_index[-1] == el_:
            arr.append(fen[i:el_])
            arr.append(fen[el_+1:])
        else:
            arr.append(fen[i:el_])
            i = el_ + 1
    return arr

