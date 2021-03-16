from Utilities.Constants import CellStates, Orientations
from random import shuffle, randint, randrange
from math import inf, sqrt
from heapdict import heapdict
import heapq
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

    path.append({'Cells': len(distance), 'Cost': len(path), 'Success': distance.get(end, None) is not None})
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
        found = False

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

                if neighbor == end:
                    found = True

                hop = distance.get(current, inf) + 1
                if hop < distance.get(neighbor, inf):
                    distance[neighbor] = hop
                    previous[neighbor] = current

        if found:
            break

    path = retrace_path(distance, previous, end)[::-1]
    for cell in path:
        yield cell


def a_star(grid, start, end, cells_per_row, cells_per_col):
    g = {start: 0}

    open_set = [(h_score(start, end), start)]
    closed_set = set([])

    previous = {}

    while list(open_set):
        _, current = heapq.heappop(open_set)

        if current == end:
            break

        shuffle(movement_offsets)
        cx, cy = current
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if 0 <= cx + x_offset < cells_per_row
            and 0 <= cy + y_offset < cells_per_col
            and grid[cy + y_offset][cx + x_offset] is not CellStates.Block
        ]

        for neighbor in neighbors:
            if neighbor not in open_set and neighbor not in closed_set:
                yield [neighbor, CellStates.Neighbor]
                g[neighbor] = g[current] + 1
                previous[neighbor] = current
                f = g[neighbor] + h_score(neighbor, end)
                heapq.heappush(open_set, (f, neighbor))
            else:
                if g[neighbor] > g[current] + 1:
                    g[neighbor] = g[current] + 1
                    previous[neighbor] = current

                    if neighbor in closed_set:
                        closed_set.remove(neighbor)
                        f = g[neighbor] + h_score(neighbor, end)
                        heapq.heappush(open_set, (f, neighbor))

        closed_set.add(current)

    path = retrace_path(g, previous, end)[::-1]
    for cell in path:
        yield cell


def weighted_a_star(grid, start, end, cells_per_row, cells_per_col):
    g = {start: 0}

    open_set = [(h_score(start, end), start)]
    closed_set = set([])

    previous = {}
    w = 1.2

    while list(open_set):
        _, current = heapq.heappop(open_set)

        if current == end:
            break

        shuffle(movement_offsets)
        cx, cy = current
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if 0 <= cx + x_offset < cells_per_row
            and 0 <= cy + y_offset < cells_per_col
            and grid[cy + y_offset][cx + x_offset] is not CellStates.Block
        ]

        for neighbor in neighbors:
            if neighbor not in open_set and neighbor not in closed_set:
                yield [neighbor, CellStates.Neighbor]
                g[neighbor] = g[current] + 1
                previous[neighbor] = current
                f = g[neighbor] + h_score(neighbor, end, w)
                heapq.heappush(open_set, (f, neighbor))
            else:
                if g[neighbor] > g[current] + 1:
                    g[neighbor] = g[current] + 1
                    previous[neighbor] = current

                    if neighbor in closed_set:
                        closed_set.remove(neighbor)
                        f = g[neighbor] + h_score(neighbor, end, w)
                        heapq.heappush(open_set, (f, neighbor))

        closed_set.add(current)

    path = retrace_path(g, previous, end)[::-1]
    for cell in path:
        yield cell


def astar_bidirectional_helper(grid, open_set, closed_set, g, previous, target, cells_per_row, cells_per_col):
    if open_set:
        _, current = heapq.heappop(open_set)
        shuffle(movement_offsets)
        cx, cy = current
        neighbors = [
            (cx + x_offset, cy + y_offset) for x_offset, y_offset in movement_offsets  # 4-Dir
            if 0 <= cx + x_offset < cells_per_row
            and 0 <= cy + y_offset < cells_per_col
            and grid[cy + y_offset][cx + x_offset] is not CellStates.Block
        ]

        for neighbor in neighbors:
            if neighbor not in open_set and neighbor not in closed_set:
                yield [neighbor, CellStates.Neighbor]
                g[neighbor] = g[current] + 1
                previous[neighbor] = current
                f = g[neighbor] + h_score(neighbor, target)
                heapq.heappush(open_set, (f, neighbor))
            else:
                if g[neighbor] > g[current] + 1:
                    g[neighbor] = g[current] + 1
                    previous[neighbor] = current

                    if neighbor in closed_set:
                        closed_set.remove(neighbor)
                        f = g[neighbor] + h_score(neighbor, target)
                        heapq.heappush(open_set, (f, neighbor))

        closed_set.add(current)
        yield current


def check_intersecting(start_open_list, start_closed_list, end_open_list, end_closed_list):
    start_considered_nodes = [*start_open_list, *list(start_closed_list)]
    end_considered_nodes = [*end_open_list, *list(end_closed_list)]

    return list(set(start_considered_nodes).intersection(set(end_considered_nodes)))


def bidirectional_path(intersect, start_parent, end_parent, start_open_list, start_closed_list, end_open_list, end_closed_list):
    path = []
    if intersect:
        path1, path2 = [], []
        current = intersect

        while current:
            path1.append([current, CellStates.ShortestPath])
            current = start_parent.get(current, None)

        current = intersect

        while current:
            path2.append([current, CellStates.ShortestPath])
            current = end_parent.get(current, None)

        path = path1[::-1] + path2[1:]

    cells_considered = {*start_open_list, *list(start_closed_list), *end_open_list, *list(end_closed_list)}
    path_length = len(path)
    path.append({'Cells': len(cells_considered), 'Cost': path_length - 2, 'Success': intersect is not None})
    return path


def astar_bidirectional_search(grid, start, end, cells_per_row, cells_per_col):
    start_open_list = [(0, start)]
    start_closed_list = set([])
    start_g = {start: 0}
    start_parent = {}

    end_open_list = [(0, end)]
    end_closed_list = set([])
    end_g = {end: 0}
    end_parent = {}

    intersect = None
    target = end

    while start_open_list and end_open_list:
        for output in astar_bidirectional_helper(grid, start_open_list, start_closed_list, start_g, start_parent, target, cells_per_row, cells_per_col):
            if type(output) == tuple:
                target = output
            else:
                yield output
        for output in astar_bidirectional_helper(grid, end_open_list, end_closed_list, end_g, end_parent, target, cells_per_row, cells_per_col):
            if type(output) == tuple:
                target = output
            else:
                yield output

        intersect = check_intersecting(start_open_list, start_closed_list, end_open_list, end_closed_list)
        if intersect:
            intersect = intersect[0]
            break

    for cell in bidirectional_path(intersect, start_parent, end_parent, start_open_list, start_closed_list, end_open_list, end_closed_list):
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
    Bidirectional = astar_bidirectional_search
    BreadthFirstSearch = breadth_first_search
    DepthFirstSearch = depth_first_search
    Dijkstra = dijkstra
    AStar = a_star
    WAStar = weighted_a_star
    ClearGrid = clear_grid
    RecursiveDivision = recursive_division
    DFSMaze = dfs_maze


def h_score(pa, pb, w=1.0):
    return w * sqrt((pb[0] - pa[0]) ** 2 + (pb[1] - pa[1]) ** 2)
