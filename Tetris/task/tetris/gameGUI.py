import tkinter as tk
from game import Block, Board
import sys
import math

height = 17


def exit_g():
    sys.exit()


def change():
    board.change_next()
    update_interface()


def move_left(event):
    board.move_block('l')
    check_state()
    update_interface()


def move_right(event):
    board.move_block('r')
    check_state()
    update_interface()


def move_down(event):
    board.move_block('d')
    check_state()
    update_interface()


def auto_down():
    if board.auto_fall:
        board.move_block('d')
        check_state()
        update_interface()
        time = int(100 + 600 / math.ceil(len(board.blocks)/5))
        window.after(time, auto_down)


def turn_ad():
    board.auto_fall = not board.auto_fall
    auto_down()


def rotate(event):
    board.move_block('o')
    check_state()
    update_interface()


def check_state():
    if game_over():
        return
    board.check_d_border()
    if board.curr_block.static:
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
    if [x for x in board.frozen if x < board.m]:
        score = 10 * board.rem_rows + 3 * len(board.blocks)
        lbl_info['text'] = 'Game Over!    Score: '+str(score)
        return True
    return False


def new_game():
    global board
    del board
    board = Board(height)
    board.add_block()
    update_interface()
    lbl_info['text'] = 'controls: left, right, down, up(rotate)'
    board.auto_fall = True


board = Board(height)
board.add_block()
board.auto_fall = True

window = tk.Tk()
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
frm_btn.columnconfigure([0, 1, 2, 3], weight=1)
btn_change = tk.Button(master=frm_btn, text='change', command=change)
btn_change.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
btn_exit = tk.Button(master=frm_btn, text='exit', command=exit_g)
btn_exit.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)
btn_new = tk.Button(master=frm_btn, text='new', command=new_game)
btn_new.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
btn_ad = tk.Button(master=frm_btn, text='ad', command=turn_ad)
btn_ad.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

if board.auto_fall:
    window.after(500, auto_down)
window.mainloop()
