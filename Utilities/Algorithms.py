from Utilities.Constants import CellStates, Orientations
from random import shuffle, randint, randrange
from math import inf
from heapdict import heapdict
import time

movement_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def retrace_path(distance, previous, end):
    path = []
    if distance.get(end, None) is not None:
        current = end
        while previous.get(current, False):
            if not current == end:
                path.append([current, CellStates.ShortestPath])

            current = previous[current]

    path.append({'Cells': len(distance), 'Cost': len(path), 'Success': distance.get(end, False) & True})
    return path


def breadth_first_search(grid, start, end, cells_per_row, cells_per_col):
    visited = {start: True}
    queue = [start]
    previous = {}
    distance = {start: 0}

    while queue:
        current = cx, cy = queue.pop(0)
        found = False

        shuffle(movement_offsets)
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if 0 <= cx + x_offset < cells_per_row
            and 0 <= cy + y_offset < cells_per_col
            and grid[cy + y_offset][cx + x_offset] in (CellStates.Free, CellStates.Start, CellStates.End)
        ]

        for neighbor in neighbors:
            if not visited.get(neighbor, False):
                yield [neighbor, CellStates.Neighbor]

                visited[neighbor] = True
                distance[neighbor] = distance[current] + 1
                previous[neighbor] = current
                queue.append(neighbor)

                if neighbor == end:
                    found = True
                    break

        if found:
            break

    path = retrace_path(distance, previous, end)[::-1]
    for cell in path:
        yield cell


def depth_first_search(grid, start, end, cells_per_row, cells_per_col):
    visited = {start: True}
    stack = [start]
    previous = {}
    distance = {start: 0}

    while stack:
        current = cx, cy = stack.pop()
        found = False

        shuffle(movement_offsets)
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if 0 <= cx + x_offset < cells_per_row
            and 0 <= cy + y_offset < cells_per_col
            and grid[cy + y_offset][cx + x_offset] in (CellStates.Free, CellStates.Start, CellStates.End)
        ]

        for neighbor in neighbors:
            if not visited.get(neighbor, False):
                yield [neighbor, CellStates.Neighbor]

                visited[neighbor] = True
                distance[neighbor] = distance[current] + 1
                previous[neighbor] = current
                stack.append(neighbor)

                if neighbor == end:
                    found = True
                    break

        if found:
            break

    path = retrace_path(distance, previous, end)[::-1]
    for cell in path:
        yield cell


def dijkstra(grid, start, end, cells_per_row, cells_per_col):
    visited = {}
    distance = {start: 0}
    queue = [start]
    previous = {}

    while queue:
        current = cx, cy = queue.pop(0)

        shuffle(movement_offsets)
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if 0 <= cx + x_offset < cells_per_row
            and 0 <= cy + y_offset < cells_per_col
            and grid[cy + y_offset][cx + x_offset] is not CellStates.Block
        ]

        for neighbor in neighbors:
            if not visited.get(neighbor, False):
                queue.append(neighbor)
                visited[neighbor] = True
                yield [neighbor, CellStates.Neighbor]

                hop = distance.get(current, inf) + 1
                if hop < distance.get(neighbor, inf):
                    distance[neighbor] = hop
                    previous[neighbor] = current

    path = retrace_path(distance, previous, end)[::-1]
    for cell in path:
        yield cell


def a_star(grid, start, end, cells_per_row, cells_per_col):
    open_set = [start]
    previous = {}
    g_score = {start: 0}
    f_score = {start: h_score(start, end)}

    while open_set:
        potential_f_scores = heapdict([(x, f_score.get(x, inf)) for x in open_set])     # Heap-based Priority-queue
        current = (cx, cy) = potential_f_scores.popitem()[0]
        if current == end:
            break

        open_set.remove(current)

        shuffle(movement_offsets)
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if 0 <= cx + x_offset < cells_per_row
            and 0 <= cy + y_offset < cells_per_col
            and grid[cy + y_offset][cx + x_offset] is not CellStates.Block
        ]

        for neighbor in neighbors:
            yield [neighbor, CellStates.Neighbor]

            tentative_g_score = g_score.get(current, inf) + 1
            if tentative_g_score < g_score.get(neighbor, inf):
                previous[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h_score(neighbor, end)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    path = retrace_path(g_score, previous, end)[::-1]
    for cell in path:
        yield cell


def clear_grid(cells_per_row, cells_per_col):
    right = True

    for row in range(cells_per_col):
        if right:
            for col in range(cells_per_row):
                yield [(col, row), CellStates.Free]
            right = False
        else:
            for col in range(cells_per_row - 1, -1, -1):
                yield [(col, row), CellStates.Free]
            right = True


def generate_recursive_division(grid, top, bottom, left, right, wall_cells):
    start_range = bottom + 2
    end_range = top - 1
    y = randrange(start_range, end_range, 2)

    for column in range(left + 1, right):
        wall_cells.append([(column, y), CellStates.Block])

    start_range = left + 2
    end_range = right - 1
    x = randrange(start_range, end_range, 2)

    for row in range(bottom + 1, top):
        wall_cells.append([(x, row), CellStates.Block])

    # Make 3 gaps on 4 walls randomly
    wall = randrange(4)
    if wall != 0:
        gap = randrange(left + 1, x, 2)
        wall_cells.append([(gap, y), CellStates.Free])

    if wall != 1:
        gap = randrange(x + 1, right, 2)
        wall_cells.append([(gap, y), CellStates.Free])

    if wall != 2:
        gap = randrange(bottom + 1, y, 2)
        wall_cells.append([(x, gap), CellStates.Free])

    if wall != 3:
        gap = randrange(y + 1, top, 2)
        wall_cells.append([(x, gap), CellStates.Free])

    # Recursively divide the maze
    if top > y + 3 and x > left + 3:
        generate_recursive_division(grid, top, y, left, x, wall_cells)

    if top > y + 3 and x + 3 < right:
        generate_recursive_division(grid, top, y, x, right, wall_cells)

    if bottom + 3 < y and x + 3 < right:
        generate_recursive_division(grid, y, bottom, x, right, wall_cells)

    if bottom + 3 < y and x > left + 3:
        generate_recursive_division(grid, y, bottom, left, x, wall_cells)


def recursive_division(grid, width, height):
    changed_cells = [[(x, 0), CellStates.Block] for x in range(width)] + [[(width - 1, y), CellStates.Block] for y in range(1, height)] + \
                    [[(x, height - 1), CellStates.Block] for x in range(width - 2, -1, -1)] + [[(0, y), CellStates.Block] for y in range(height - 2, 0, -1)]
    generate_recursive_division(grid, height - 1, 0, 0, width - 1, changed_cells)

    for cell in changed_cells:
        yield cell


def dfs_maze(grid, x, y, width, height):
    start = (randrange(x, x + width), randrange(y, y + height))
    visited = {start: True}
    steps = randrange(width * height // 2, (width * height * 3) // 4)
    stack = [start]

    while stack and steps > 0:
        steps -= 1
        current = cx, cy = stack.pop()
        yield [current, CellStates.Free]

        shuffle(movement_offsets)
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if x <= cx + x_offset < x + width
            and y <= cy + y_offset < y + height
            and grid[cy + y_offset][cx + x_offset] not in (CellStates.Start, CellStates.End)
        ]

        for neighbor in neighbors:
            if not visited.get(neighbor, False):
                visited[neighbor] = True
                stack.append(neighbor)


class Algorithms:
    BreadthFirstSearch = breadth_first_search
    DepthFirstSearch = depth_first_search
    Dijkstra = dijkstra
    AStar = a_star
    ClearGrid = clear_grid
    RecursiveDivision = recursive_division
    DFSMaze = dfs_maze


def h_score(pa, pb):
    return (pb[0] - pa[0]) ** 2 + (pb[1] - pa[1]) ** 2
