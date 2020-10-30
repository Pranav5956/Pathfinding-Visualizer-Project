import pygame
from Utilities.Constants import CellStates, Actions, Colors, Orientations
from Utilities.Algorithms import Algorithms


class GridParent:
    def __init__(self, x, y, width, height, window, cell_size, grid=None):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.cells_per_row, self.cells_per_col, self.cell_size = width // cell_size, height // cell_size, cell_size
        if grid is None:
            self.grid = [[CellStates.Free for _ in range(self.cells_per_row)] for _ in range(self.cells_per_col)]
        else:
            self.grid = grid
        self.grid_copy = [[cell for cell in row] for row in self.grid]

        self.window = window

        # Create a grid at half transparency
        self.grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for cell in range(self.cells_per_row):
            pygame.draw.line(
                self.grid_surface,
                Colors.BlackHalfAlpha,
                (cell * self.cell_size, 0),
                (cell * self.cell_size, height)
            )
        for cell in range(self.cells_per_col):
            pygame.draw.line(
                self.grid_surface,
                Colors.BlackHalfAlpha,
                (0, cell * self.cell_size),
                (width, cell * self.cell_size)
            )

    def update(self):
        self.draw()

    def set_grid(self, grid):
        self.grid = [[cell for cell in row] for row in grid]

    def draw(self):
        # Draw the squares
        for col in range(self.cells_per_col):
            for row in range(self.cells_per_row):
                if self.grid[col][row] == CellStates.Block:
                    pygame.draw.rect(self.window, Colors.Black,
                                     (self.x + row * self.cell_size, self.y + col * self.cell_size, self.cell_size, self.cell_size))
                elif self.grid[col][row] == CellStates.Start:
                    pygame.draw.rect(self.window, Colors.Teal,
                                     (self.x + row * self.cell_size, self.y + col * self.cell_size, self.cell_size, self.cell_size))
                elif self.grid[col][row] == CellStates.End:
                    pygame.draw.rect(self.window, Colors.Yellow,
                                     (self.x + row * self.cell_size, self.y + col * self.cell_size, self.cell_size, self.cell_size))
                elif self.grid[col][row] == CellStates.Neighbor:
                    pygame.draw.rect(self.window, Colors.Red,
                                     (self.x + row * self.cell_size, self.y + col * self.cell_size, self.cell_size, self.cell_size))
                elif self.grid[col][row] == CellStates.ShortestPath:
                    pygame.draw.rect(self.window, Colors.Green,
                                     (self.x + row * self.cell_size, self.y + col * self.cell_size, self.cell_size, self.cell_size))

        # Draw the grid overlay
        self.window.blit(self.grid_surface, (self.x, self.y))


class GridDisplayAlgorithm(GridParent):
    def __init__(self, x, y, width, height, window, cell_size, start, end, algorithm, grid=None):
        super().__init__(x, y, width, height, window, cell_size, grid)
        self.start, self.end = start, end
        self.algorithm = algorithm
        self.algorithm_execution = None
        self.algorithm_running = False

        (sx, sy), (ex, ey) = start, end
        self.grid[sy][sx] = CellStates.Start
        self.grid[ey][ex] = CellStates.End

        self.attributes = None

    def update(self):
        if self.algorithm_running:
            try:
                algorithm_data = next(self.algorithm_execution)
                if type(algorithm_data) == list:
                    pos, state = algorithm_data

                    if pos != self.start and pos != self.end:
                        px, py = pos
                        self.grid[py][px] = state
                elif type(algorithm_data) == dict:
                    self.attributes = list(algorithm_data.values())
            except StopIteration:
                self.algorithm_running = False

        super().update()

    def get_stats(self):
        if self.attributes:
            return self.attributes
        return None

    def run_pathfinding_algorithm(self):
        if not self.algorithm_running:
            if self.grid != self.grid_copy:
                self.grid = [[cell for cell in row] for row in self.grid_copy]
            self.algorithm_running = True
            self.attributes = None
            self.algorithm_execution = self.algorithm(self.grid, self.start, self.end, self.cells_per_row, self.cells_per_col)


class GridEdit(GridParent):
    def __init__(self, x, y, width, height, window, cell_size, grid=None):
        super().__init__(x, y, width, height, window, cell_size, grid)
        self.action = Actions.Start

        self.start, self.end = None, None
        self.algorithm_running = False
        self.algorithm = None

        if grid is not None:
            self.set_grid(grid)

    def set_grid(self, grid):
        self.action = Actions.Start
        self.grid = [[cell for cell in row] for row in grid]
        self.start, self.end = None, None
        start_exists, end_exists = False, False

        if grid is not None:
            for row in range(self.cells_per_col):
                for col in range(self.cells_per_row):
                    if self.grid[row][col] == CellStates.Start and not start_exists:
                        self.start = (col, row)
                        self.action = Actions.End
                        start_exists = True
                    elif self.grid[row][col] == CellStates.End and not end_exists:
                        self.end = (col, row)
                        self.action = Actions.Start
                        end_exists = True

                    if start_exists and end_exists:
                        self.action = Actions.Block
                        break

                if start_exists and end_exists:
                    break

    def update(self):
        if self.algorithm_running:
            try:
                pos, state = next(self.algorithm)

                if pos != self.start and pos != self.end:
                    px, py = pos
                    self.grid[py][px] = state
            except (StopIteration, ValueError):
                self.algorithm_running = False
                self.algorithm = None

        super().update()

        # Draw helper squares
        if not self.start:
            mouse_pos = (mx, my) = pygame.mouse.get_pos()

            if self.x < mx < self.x + self.width and self.y < my < self.y + self.height:
                row, col = ((pos - offset) // self.cell_size for pos, offset in zip(mouse_pos, [self.x, self.y]))
                pygame.draw.rect(self.window, Colors.Teal,
                                 (self.x + row * self.cell_size, self.y + col * self.cell_size, self.cell_size, self.cell_size))
        elif not self.end:
            mouse_pos = (mx, my) = pygame.mouse.get_pos()

            if self.x < mx < self.x + self.width and self.y < my < self.y + self.height:
                row, col = ((pos - offset) // self.cell_size for pos, offset in zip(mouse_pos, [self.x, self.y]))
                pygame.draw.rect(self.window, Colors.Yellow,
                                 (self.x + row * self.cell_size, self.y + col * self.cell_size, self.cell_size, self.cell_size))

    def click(self, row, col):
        if self.action == Actions.Start and self.start is None:
            if not self.grid[col][row] == CellStates.End:
                self.grid[col][row] = CellStates.Start
                self.start = (row, col)

                if self.end is None:
                    self.action = Actions.End
                else:
                    self.action = Actions.Block
        elif self.action == Actions.End and self.end is None:
            if not self.grid[col][row] == CellStates.Start:
                self.grid[col][row] = CellStates.End
                self.end = (row, col)

                if self.start is None:
                    self.action = Actions.Start
                else:
                    self.action = Actions.Block
        elif self.action == Actions.Block:
            if self.grid[col][row] == CellStates.Start:
                self.start = None
                self.grid[col][row] = CellStates.Free
                self.action = Actions.Start
            elif self.grid[col][row] == CellStates.End:
                self.end = None
                self.grid[col][row] = CellStates.Free
                self.action = Actions.End
            else:
                self.grid[col][row] = CellStates.Free if self.grid[col][row] == CellStates.Block else CellStates.Block

    def clear(self):
        self.algorithm_running = True
        self.algorithm = Algorithms.ClearGrid(self.cells_per_row, self.cells_per_col)

    def recursive_maze_generation(self):
        self.algorithm_running = True
        self.grid = [[cell if cell in (CellStates.Start, CellStates.End) else CellStates.Free for cell in row] for row in self.grid]
        self.algorithm = Algorithms.RecursiveDivision(self.grid, self.cells_per_row, self.cells_per_col)

    def dfs_maze_generation(self):
        self.algorithm_running = True
        self.grid = [[cell if cell in (CellStates.Start, CellStates.End) else CellStates.Block for cell in row] for row in self.grid]
        self.algorithm = Algorithms.DFSMaze(self.grid, 1, 1, self.cells_per_row - 2, self.cells_per_col - 2)
