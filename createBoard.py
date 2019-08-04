""" numpy library """
import numpy as np
import matplotlib.pyplot as plt

def main():
    """ main function """
    gen_board()
    #gen_array()

def gen_board():
    """"Generate board"""
#    chessboard = np.zeros((8, 8))
    chessboard = np.full((8, 8), 0.25)
    chessboard[1::2, 0::2] = 1
    chessboard[0::2, 1::2] = 1

    arr = gen_array()
    print(arr)
    lastnum=""
    for y in range(0, len(arr)):
        for x in range(0, len(arr[y])):
            if not arr[y][x].isdigit():
                x_pos = x - 0.05
                if lastnum.isdigit():
                    x_pos += (int(lastnum)-1)
                char = getChar(arr[y][x])
                color = "black" if arr[y][x].islower() else "white"
                plt.plot(x_pos, y, marker=char, markersize=24, color=color, fillstyle='full')
            lastnum = arr[y][x]
        lastnum=""

    plt.xticks(np.arange(8), ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'))
    plt.yticks(np.arange(8), ('8', '7', '6', '5', '4', '3', '2', '1'))

    plt.imshow(chessboard, cmap="copper", vmin=0, vmax=1)
    plt.show()
    #plt.savefig('test.png')

def getChar(c):
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
    return pieces[c]

def gen_array():
    """" Generate array from FEN """
    example = "rnbqkbnr/pppppppp/7p/8/8/8/PPPPPPPP/RNBQKBNR"
    one_e5 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
    #one_e4="rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR"
    one_e4="2rqr1k1/1p2bp1p/pn4p1/3p1bP1/3B3Q/2NR2R1/PPP1NP1P/1K6"

    slash_index = [pos for pos, char in enumerate(one_e4) if char == '/']
    print(slash_index)
    arr = []
    i = 0
    for el in slash_index:
        if slash_index[-1] == el:
            arr.append(one_e4[i:el])
            arr.append(one_e4[el+1:])
        else:
            arr.append(one_e4[i:el])
            i = el + 1
    print(arr)
    return arr



main()
