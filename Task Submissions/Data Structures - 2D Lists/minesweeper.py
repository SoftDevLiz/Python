grid = [
    ["-", "#", "-", "-", "-"],
    ["-", "-", "-", "#", "-"],
    ["-", "#", "#", "-", "-"],
    ["#", "-", "-", "-", "-"],
    ["-", "-", "#", "-", "#"]
]


def count_mines(grid):
    # Get the number of rows and columns to handle boundary checks
    rows = len(grid)
    cols = len(grid[0])

    # Create a copy or modify the grid in place
    for r, row in enumerate(grid):
        for c, symbol in enumerate(row):

            # Only process spots that are not mines
            if symbol == "-":
                mine_count = 0

                # Check all 8 directions (N, S, E, W, and diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the current cell itself
                        if dr == 0 and dc == 0:
                            continue

                        neighbor_row = r + dr
                        neighbor_col = c + dc

                        # Ensure the neighbor is within the grid
                        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                            # If the neighbor is a mine, increment the count
                            if grid[neighbor_row][neighbor_col] == "#":
                                mine_count += 1

                # Replace the dash with the total count (as a string)
                grid[r][c] = str(mine_count)

    return grid


# Run the function and print the result
result = count_mines(grid)

for row in result:
    print(row)
