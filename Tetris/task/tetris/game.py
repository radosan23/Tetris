import numpy as np


class Block:
    types = {'O': [[4, 14, 15, 5]],
             'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
             'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
             'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
             'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
             'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
             'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]],
             '': [[]]}

    def __init__(self, b_type, size, b_state=0):
        self.type = b_type
        self.m = size[0]
        self.n = size[1]
        self.state = b_state
        self.list = Block.types[self.type]
        self.array = self.set_array()

    def set_array(self):
        ar = np.array([['0 ' if (row * self.m + col in self.list[self.state]) else '- ' for col in range(self.m)]
                       for row in range(self.n)])
        return ar

    def rotate_block(self):
        self.state = (self.state + 1) % len(self.list)
        self.array = self.set_array()

    def move_right(self):
        self.list = [[(x // self.m * self.m) + (x + 1) % self.m for x in row] for row in self.list]
        self.array = self.set_array()

    def move_left(self):
        self.list = [[(x // self.m * self.m) + (x - 1) % self.m for x in row] for row in self.list]
        self.array = self.set_array()

    def move_down(self):
        self.list = [[((x // self.m + 1) * self.m) + x % self.m for x in row] for row in self.list]
        self.array = self.set_array()

    def print_block(self):
        print()
        for row in self.array:
            print(''.join(cell for cell in row))


def main():
    block_type = input()
    size = [int(x) for x in input().split()]
    empty = Block('', size)
    block = Block(block_type, size)
    empty.print_block()
    block.print_block()
    while True:
        cmd = input()
        if cmd == 'exit':
            break
        elif cmd == 'right':
            block.move_right()
        elif cmd == 'left':
            block.move_left()
        elif cmd == 'rotate':
            block.rotate_block()
        block.move_down()
        block.print_block()


if __name__ == '__main__':
    main()
