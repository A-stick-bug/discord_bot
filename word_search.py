async def solve(words,g):
    global res, grid
    words = words.split()
    words = [word.upper() for word in words]

    g = g.split()
    grid = [row.upper() for row in g]

    res = []

    for word in words:
        await search(word)
    return res

async def search(word):
    if len(word) > len(grid) and len(word) > len(grid[0]):
        res.append(f"\"{word}\" not in grid.")
        return

    directions = [(0, 1, "right"), (1, 0, "down"), (1, 1, "down-right diagonal"), (-1, 0, "up"), (0, -1, "left"), (-1, -1, "up-left diagonal"), (-1, 1, "up-right diagonal"), (1, -1, "down-left diagonal")]
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == word[0]:
                # check 8 directions
                for r, c, d in directions:
                    i = 1
                    new_r = row + r
                    new_c = col + c
                    while 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]) and i < len(word) and grid[new_r][new_c] == word[i]:
                        i += 1
                        new_r += r
                        new_c += c
                    if i == len(word):
                        res.append(f"\"{word}\" found in grid on row {row + 1} column {col + 1}. Direction: {d}")
                        return

    res.append(f"\"{word}\" not in grid.")
    return
