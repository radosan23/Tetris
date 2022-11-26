import numpy as np


class Block:
    def __init__(self, b_type, b_state=0):
        self.type = b_type
        self.state = b_state
        self.list = self.set_list()
        self.array = self.set_array()

    def set_list(self):
        if self.type == 'O':
            return [[5, 6, 9, 10]]
        elif self.type == 'I':
            return [[1, 5, 9, 13], [4, 5, 6, 7]]
        elif self.type == 'S':
            return [[6, 5, 9, 8], [5, 9, 10, 14]]
        elif self.type == 'Z':
            return [[4, 5, 9, 10], [2, 5, 6, 9]]
        elif self.type == 'L':
            return [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [4, 5, 6, 8]]
        elif self.type == 'J':
            return [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]]
        elif self.type == 'T':
            return [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]
        else:
            return [[]]

    def set_array(self):
        ar = np.array([['0 ' if (row * 4 + col in self.list[self.state]) else '- ' for col in range(4)]
                       for row in range(4)])
        return ar

    def rotate_block(self):
        self.state = (self.state + 1) % len(self.list)
        self.array = self.set_array()

    def print_block(self):
        print()
        for row in self.array:
            print(''.join(cell for cell in row))


def main():
    block_type = input()
    empty = Block('')
    block = Block(block_type)
    empty.print_block()
    block.print_block()
    for _ in range(4):
        block.rotate_block()
        block.print_block()


if __name__ == '__main__':
    main()
