from Utilities.Constants import CellStates
from random import shuffle
from math import inf
from heapdict import heapdict

movement_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]


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

    if distance.get(end, None) is not None:
        current = end
        while previous.get(current, False):
            if not current == end:
                yield [current, CellStates.ShortestPath]

            current = previous[current]


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

    if distance.get(end, None) is not None:
        current = end
        while previous.get(current, False):
            if not current == end:
                yield [current, CellStates.ShortestPath]

            current = previous[current]


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

    if distance.get(end, None) is not None:
        current = end
        while previous.get(current, False):
            if not current == end:
                yield [current, CellStates.ShortestPath]

            current = previous[current]


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

    if g_score.get(end, None) is not None:
        current = end
        while previous.get(current, False):
            if not current == end:
                yield [current, CellStates.ShortestPath]

            current = previous[current]


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


class Algorithms:
    BreadthFirstSearch = breadth_first_search
    DepthFirstSearch = depth_first_search
    Dijkstra = dijkstra
    AStar = a_star
    ClearGrid = clear_grid


def h_score(pa, pb):
    return abs(pb[0] - pa[0]) + abs(pb[1] - pa[1])
