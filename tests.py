#
# def init_board(length):
#     if length not in [8, 10]:
#         return ValueError("The Board should be have 8 or 10 length!")
#
#     l_middle = length // 2
#
#     def get_num(i, j):
#         if i < l_middle - 1:
#             return 2
#         if i <= l_middle:
#             return 1
#         return 3
#
#     return [[get_num(i, j) if (i + j) % 2 else 0 for j in range(length)] for i in range(length)]
#
#
# if __name__ == '__main__':
#     import json
#
#     for line in init_board(8):
#         print(line)