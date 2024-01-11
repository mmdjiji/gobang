from gmcts.mcts import Agent
from gmcts.board import ChessBoard
import os
import copy
import time

pre_visits = 0
avg_visits = 0

def run_onetime(chess_board, agent, i, j):
    global pre_visits
    global avg_visits
    # os.system('cls')
    move = (i, j)
    chess_board.play_stone(move)
    chess_board.display_board()
    t0 = time.time()
    pre_visits, avg_visits = agent.update_root(move)
    print()
    if pre_visits != 0:
        print("-" * 40)
        print(f"Pre Visits: {pre_visits:.0f}")
        print(f"Avg Visits: {avg_visits:.0f}")
        print("-" * 40 + "\n")

    agent_loc, agent_win_rate, l = agent.search()
    chess_board.play_stone(agent_loc)
    chess_board.display_board()

    t1 = time.time()
    dt = t1 - t0
    print("\n"+"-"*40)
    print(f"AI play a stone at {agent_loc}")
    print(f"AI Win Rate: {agent_win_rate*100:.6f}%")
    print(f"  Time Cost: {dt:.6f}s")
    print("-"*40+"\n")

    return chess_board, agent_loc, agent_win_rate, l

def run():
    chess_board = ChessBoard()
    print("You will play the fist stone if typing in `1` and AI first if you type in `0`")
    sente = int(input("Sente?  "))
    if sente == 0:
        chess_board.play_stone((8, 8))
        chess_board.display_board()
    agent = Agent(chess_board=copy.deepcopy(chess_board), max_searches=10000)
    while not chess_board.is_ended():
        i = int(input('Abscissa: '))
        j = int(input('Ordinate: '))
        while not chess_board.is_legal((i, j)):
            print(f'Cannot play a stone at {(i, j)}. Try again.')
            i = int(input('Abscissa: '))
            j = int(input('Ordinate: '))
        chess_board, agent_loc, agent_win_rate = run_onetime(chess_board, agent, i, j)
        if chess_board.is_ended():
            break


def one_time_try(chess_board, agent, i, j):
    if not chess_board.is_ended():
        chess_board, agent_loc, agent_win_rate, l = run_onetime(chess_board, agent, i, j)
        return chess_board, agent_loc, agent_win_rate, l
    else:
        pass


chess_board = ChessBoard()
# print("You will play the fist stone if typing in `1` and AI first if you type in `0`")
# sente = int(input("Sente?  "))
sente = 1
if sente == 0:
    chess_board.play_stone((5, 5))
    chess_board.display_board()
agent = Agent(chess_board=copy.deepcopy(chess_board), max_searches=2000)

# i = int(input('Abscissa: '))
# j = int(input('Ordinate: '))
# while not chess_board.is_legal((i, j)):
#     print(f'Cannot play a stone at {(i, j)}. Try again.')
#     i = int(input('Abscissa: '))
#     j = int(input('Ordinate: '))

# chess_board, agent_loc, agent_win_rate = one_time_try(chess_board, agent, i, j)
# x, y = agent_loc
# print(x, y)

def createit():
    global chess_board
    global agent
    chess_board = ChessBoard()
    agent = Agent(chess_board=copy.deepcopy(chess_board), max_searches=10000)

def execute(x, y):
    global chess_board
    global agent
    global pre_visits
    global avg_visits
    chess_board, agent_loc, agent_win_rate, l = one_time_try(chess_board, agent, x, y)
    aix, aiy = agent_loc
    return aix, aiy, agent_win_rate, pre_visits, avg_visits, l

# print(execute(5, 5))