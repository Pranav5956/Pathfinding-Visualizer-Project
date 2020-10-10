from Utilities.Constants import CellStates
from random import shuffle

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
    pass


def dijkstra(grid, start, end, cells_per_row, cells_per_col):
    pass


def a_star(grid, start, end, cells_per_row, cells_per_col):
    pass


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
