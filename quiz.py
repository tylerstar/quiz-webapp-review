
"""Quiz 1

Reverse a list without using any built in functions (sorted, reversed, etc.)
Input l is a list which can contain any type of data.
"""


# Method 1, use slicing and return a reversed new list
def reverse_list1(l: list):
    return l[::-1]


# Method 2, use two pointers and modify the list in place
def reverse_list2(l: list):
    left, right = 0, len(l) - 1
    while left < right:
        l[left], l[right] = l[right], l[left]
        left += 1
        right -= 1


"""Quiz 2

Write a programme to solve 9x9 Sudoku board. (9x9)
"""

# [ATTENTION]:
# 1. Assume the input is a 9x9 matrix with "." as empty slot
# 2. All digits in the matrix should be string type, starts from "1" to "9"


def solve_sudoku(matrix):
    # Logic: A valid sudoku means for every row, column and block, the digits
    # from 1 to 9 should be used only once

    # Prepare all the variables for solving the sudoku
    line = [[False] * 9 for _ in range(9)]
    column = [[False] * 9 for _ in range(9)]
    block = [[[False] * 9 for row in range(3)] for col in range(3)]
    slots = []  # Store all empty positions

    # Create a state to check if the sudoku is valid
    valid = False

    # Use backtracing method to check every slot
    def dfs(pos):
        nonlocal valid

        if pos == len(slots):
            valid = True
            return

        i, j = slots[pos]
        for digit in range(9):
            # If the digit has been used in the row, column or block, skip it
            if any([
                line[i][digit],
                column[j][digit],
                block[i // 3][j // 3][digit]
            ]):
                continue

            # Update the state
            line[i][digit] = column[j][digit] = \
                block[i // 3][j // 3][digit] = True

            # Remember to add 1 to the digit because the digit is from 0 to 9
            matrix[i][j] = str(digit + 1)

            # Continue to the next slot until all slots are filled
            dfs(pos + 1)

            # Reverse the state and try another digit
            line[i][digit] = column[j][digit] = \
                block[i // 3][j // 3][digit] = False

            # If the sudoku is valid, return
            if valid:
                return

    for i in range(9):
        for j in range(9):
            # Find all the empty slots
            if matrix[i][j] == ".":
                slots.append((i, j))
            else:
                # Label the digit as used
                digit = int(matrix[i][j]) - 1
                line[i][digit] = column[j][digit] = \
                    block[i // 3][j // 3][digit] = True

    # If the input matrix already filled, return
    if len(slots) == 0:
        return

    # Start to solve the sudoku from the first slot
    dfs(0)


"""Examples & Test Cases
"""
if __name__ == '__main__':

    # Test case for quiz 1, reverse an integer list
    l1 = [3, 4, "Jerry", False, 2, "Jane"]
    print("Original List:", l1)
    reversed_l1 = reverse_list1(l1)  # Get a reversed new list
    reverse_list2(l1)  # Reverse the list in place
    assert reversed_l1 == l1, "Test case 1 failed"
    print("Reversed List:", l1)

    # Test case for quiz 2, solve a sudoku
    matrix = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    solve_sudoku(matrix)
    print("\nSolved Sudoku:")
    for row in matrix:
        print(row)
