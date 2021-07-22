

def init_board(length):
    if length not in [8, 10]:
        return ValueError("The Board should be have 8 or 10 length!")

    l_middle = length // 2

    def get_num(i, j):
        if (i + j) % 2 == 0:
            return 0
        if i < l_middle - 1:
            return 2
        if i <= l_middle:
            return 1
        return 3

    return [[get_num(i, j) for j in range(length)] for i in range(length)]