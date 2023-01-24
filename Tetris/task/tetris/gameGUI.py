import tkinter as tk
from game import Block, Board
from os.path import isfile
import sys
import math

board = None
height = 17
name = ''
score = 0
h_scores = []


def exit_g():
    sys.exit()


def change():
    board.change_next()
    update_interface()


def move_left(event):
    if not board.g_over:
        board.move_block('l')
        check_state()
        update_interface()


def move_right(event):
    if not board.g_over:
        board.move_block('r')
        check_state()
        update_interface()


def move_down(event):
    if not board.g_over:
        board.move_block('d')
        check_state()
        update_interface()


def auto_down():
    if board.autodown and not board.g_over:
        board.move_block('d')
        check_state()
        update_interface()
        time = int(100 + 600 / math.ceil(len(board.blocks)/5))
        window.after(time, auto_down)


def turn_ad():
    board.autodown = not board.autodown
    auto_down()


def rotate(event):
    if not board.g_over:
        board.move_block('o')
        check_state()
        update_interface()


def check_state():
    board.check_d_border()
    game_over()
    if board.curr_block.static and not board.g_over:
        board.remove_rows()
        board.add_block()
        board.check_d_border()


def update_interface():
    lbl_next['text'] = 'next block: '+board.queue[0]
    lbl_change['text'] = 'changes: '+str(board.changes)
    for i in range(board.n):
        for j in range(board.m):
            if board.array[i][j] == '0 ':
                lbl[i][j]['bg'] = 'blue'
            else:
                lbl[i][j]['bg'] = 'lightgray'


def game_over():
    global score
    if [x for x in board.frozen if x < board.m]:
        score = 10 * board.rem_rows + 3 * len(board.blocks)
        lbl_info['text'] = 'Game Over!    Score: '+str(score)
        board.g_over = True
        check_highscore()


def new_game():
    global board
    del board
    board = Board(height)
    board.add_block()
    update_interface()
    lbl_info['text'] = 'controls: left, right, down, up(rotate)'
    board.autodown = True
    board.g_over = False
    auto_down()


def check_highscore():
    global h_scores
    check_hs_file()
    with open('highscores.bin', 'r') as f:
        text = ''.join([chr(int(x)) for x in f.read().split()])
        h_scores = [line.split() for line in text.splitlines()]
    if len(h_scores) < 10 or score > int(h_scores[9][1]):
        entry_name()


def entry_name():
    def get_name():
        global name
        name = ent_name.get()
        win_name.destroy()
        save_hscore()

    win_name = tk.Toplevel(window)
    lbl_name = tk.Label(master=win_name, text='Highscore! Enter your name:')
    lbl_name.grid(row=0, column=0, padx=5, pady=5)
    ent_name = tk.Entry(master=win_name)
    ent_name.grid(row=1, column=0, padx=5, pady=5)
    btn_name = tk.Button(master=win_name, text='submit', command=get_name)
    btn_name.grid(row=2, column=0, padx=5, pady=5)
    win_name.focus_force()


def save_hscore():
    global h_scores
    h_scores.append([name + ':', str(score)])
    h_scores.sort(key=lambda x: int(x[1]), reverse=True)
    with open('highscores.bin', 'w') as f:
        text = '\n'.join(['\t\t'.join(x) for x in h_scores[:10]])
        f.write(' '.join(str(ord(x)) for x in text))


def show_hscore():
    check_hs_file()
    with open('highscores.bin', 'r') as f:
        hs = ''.join([chr(int(x)) for x in f.read().split()])
    win_hs = tk.Toplevel(window)
    lbl_hs = tk.Label(master=win_hs, text=hs)
    lbl_hs.grid(row=0, column=0, padx=5, pady=5)
    btn_hs = tk.Button(master=win_hs, text='close', command=win_hs.destroy)
    btn_hs.grid(row=1, column=0, padx=5, pady=5)
    win_hs.focus_force()


def check_hs_file():
    if not isfile('highscores.bin'):
        with open('highscores.bin', 'w') as f:
            f.write('')


board = Board(height)
board.add_block()
board.autodown = True

window = tk.Tk()
window.title('Tetris')
window.columnconfigure(0, weight=1, minsize=240)
window.bind('<Left>', move_left)
window.bind('<Right>', move_right)
window.bind('<Down>', move_down)
window.bind('<Up>', rotate)

frm_next = tk.Frame(relief=tk.RAISED, borderwidth=2)
frm_next.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
frm_next.columnconfigure([0, 1], weight=1)
lbl_next = tk.Label(master=frm_next, text='next block: '+board.queue[0])
lbl_next.grid(row=0, column=0, sticky='w', padx=5, pady=5)
lbl_change = tk.Label(master=frm_next, text='changes: '+str(board.changes))
lbl_change.grid(row=0, column=1, sticky='e', padx=5, pady=5)

frm_board = tk.Frame(relief=tk.RIDGE, borderwidth=2)
frm_board.grid(row=1, column=0)
frm_board.rowconfigure(list(range(board.n)), minsize=20)
frm_board.columnconfigure(list(range(board.m)), minsize=20)
lbl = [[None for x in range(board.m)] for row in range(board.n)]
for i in range(board.n):
    for j in range(board.m):
        if board.array[i][j] == '0 ':
            lbl[i][j] = tk.Label(master=frm_board, text='', bg='blue')
        else:
            lbl[i][j] = tk.Label(master=frm_board, text='', bg='lightgray')
        lbl[i][j].grid(row=i, column=j, sticky='nsew')

frm_info = tk.Frame()
frm_info.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
lbl_info = tk.Label(master=frm_info, text='controls: left, right, down, up(rotate)')
lbl_info.grid(row=0, column=0, sticky='ew')

frm_btn = tk.Frame()
frm_btn.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
frm_btn.columnconfigure([0, 1, 2], weight=1)
btn_change = tk.Button(master=frm_btn, text='change', command=change)
btn_change.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
btn_exit = tk.Button(master=frm_btn, text='exit', command=exit_g)
btn_exit.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
btn_new = tk.Button(master=frm_btn, text='new', command=new_game)
btn_new.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
btn_ad = tk.Button(master=frm_btn, text='autodown', command=turn_ad)
btn_ad.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
btn_hs = tk.Button(master=frm_btn, text='highscore', command=show_hscore)
btn_hs.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

window.after(500, auto_down)
window.mainloop()
