import pygame
from random import randint, randrange
from Utilities.Constants import CellStates, Actions, Colors, Orientations
from Utilities.Constants import SIZE, WIDTH, HEIGHT, CELL_SIZE
from Utilities.Algorithms import Algorithms


class Grid:
    CellsPerRow, CellsPerCol = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

    def __init__(self, window, row, col):
        # Initialize the grid
        self.window = window
        self.grid = [[CellStates.Free for _ in range(Grid.CellsPerRow)] for _ in range(Grid.CellsPerCol)]
        self.x, self.y = row * WIDTH, col * HEIGHT

        # Create a grid at half transparency
        self.grid_surface = pygame.Surface(SIZE, pygame.SRCALPHA)
        for cell in range(Grid.CellsPerRow + 1):
            pygame.draw.line(
                self.grid_surface,
                Colors.BlackHalfAlpha,
                (self.x + cell * CELL_SIZE, self.y + 0),
                (self.x + cell * CELL_SIZE, self.y + HEIGHT)
            )
        for cell in range(Grid.CellsPerCol + 1):
            pygame.draw.line(
                self.grid_surface,
                Colors.BlackHalfAlpha,
                (self.x + 0, self.y + cell * CELL_SIZE),
                (self.x + WIDTH, self.y + cell * CELL_SIZE)
            )

        # State initialization
        self.start = None
        self.end = None
        self.action = Actions.Start

        # Algorithm Initialization
        self.algorithm = None

    def draw(self):
        # Execute the algorithm if it is running
        if self.algorithm is not None:
            try:
                pos, state = next(self.algorithm)

                if pos != self.start and pos != self.end:
                    px, py = pos
                    self.grid[py][px] = state
            except StopIteration:
                self.algorithm = None

        # Draw the squares
        for col in range(Grid.CellsPerCol):
            for row in range(Grid.CellsPerRow):
                if self.grid[col][row] == CellStates.Block:
                    pygame.draw.rect(self.window, Colors.Black, (self.x + row * CELL_SIZE, self.y + col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.grid[col][row] == CellStates.Start:
                    pygame.draw.rect(self.window, Colors.Teal, (self.x + row * CELL_SIZE, self.y + col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.grid[col][row] == CellStates.End:
                    pygame.draw.rect(self.window, Colors.Yellow, (self.x + row * CELL_SIZE, self.y + col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.grid[col][row] == CellStates.Neighbor:
                    pygame.draw.rect(self.window, Colors.Red, (self.x + row * CELL_SIZE, self.y + col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.grid[col][row] == CellStates.ShortestPath:
                    pygame.draw.rect(self.window, Colors.Green, (self.x + row * CELL_SIZE, self.y + col * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the grid overlay
        self.window.blit(self.grid_surface, (0, 0))

        # Draw helper squares
        if not self.start:
            row, col = ((pos - offset) // CELL_SIZE for pos, offset in zip(pygame.mouse.get_pos(), [self.x, self.y]))
            pygame.draw.rect(self.window, Colors.Teal, (self.x + row * CELL_SIZE, self.y + col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        elif not self.end:
            row, col = ((pos - offset) // CELL_SIZE for pos, offset in zip(pygame.mouse.get_pos(), [self.x, self.y]))
            pygame.draw.rect(self.window, Colors.Yellow, (self.x + row * CELL_SIZE, self.y + col * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.update()

    def run_algorithm(self, algorithm):
        if self.algorithm is None:
            if algorithm == Algorithms.ClearGrid:
                self.algorithm = algorithm(Grid.CellsPerRow, Grid.CellsPerCol)
            else:
                self.algorithm = algorithm(self.grid, self.start, self.end, Grid.CellsPerRow, Grid.CellsPerCol)

    def clear_grid(self):
        for col in range(Grid.CellsPerCol):
            for row in range(Grid.CellsPerRow):
                if self.grid[col][row] not in (CellStates.Start, CellStates.End):
                    self.grid[col][row] = CellStates.Free

    def on_click(self, row, col):
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

    def outer_wall_generation(self):
        for col, row in [(0, x) for x in range(Grid.CellsPerRow)] + [(y, Grid.CellsPerRow - 1) for y in range(1, Grid.CellsPerCol)] + \
                        [(Grid.CellsPerCol - 1, x) for x in range(Grid.CellsPerRow - 2, -1, -1)] + [(y, 0) for y in range(Grid.CellsPerCol - 2, 0, -1)]:
            if not (row, col) == self.start and not (row, col) == self.end:
                self.grid[col][row] = CellStates.Block
                self.draw()

    def recursive_division_maze_generation(self, x, y, width, height, orientation=Orientations.Horizontal):
        if width < 2 or height < 2:
            return

        wall_x = x + (0 if orientation == Orientations.Horizontal else randint(0, width - 2))
        wall_y = y + (0 if orientation == Orientations.Vertical else randint(0, height - 2))
        print(x, y, wall_x, wall_y)

        passage_x = wall_x + (randrange(0, width) if orientation == Orientations.Horizontal else 0)
        passage_y = wall_y + (randrange(0, height) if orientation == Orientations.Vertical else 0)

        length = width if orientation == Orientations.Horizontal else height

        while length > 0:
            length -= 1
            if (wall_x, wall_y) != (passage_x, passage_y) and (wall_x, wall_y) != self.start and (wall_x, wall_y) != self.end:
                self.grid[wall_y][wall_x] = CellStates.Block
            wall_x, wall_y = wall_x + (orientation == Orientations.Horizontal), wall_y + (orientation == Orientations.Vertical)
            self.draw()

        w = width if orientation == Orientations.Horizontal else wall_x - x + 1
        h = height if orientation == Orientations.Vertical else wall_y - y + 1
        self.recursive_division_maze_generation(
            x, y,
            w, h,
            Orientations.Horizontal if w < h else Orientations.Vertical
        )

        w = width if orientation == Orientations.Horizontal else x + width - wall_x - 1
        h = height if orientation == Orientations.Vertical else y + height - wall_y - 1
        self.recursive_division_maze_generation(
            x if Orientations.Horizontal else wall_x + 1,
            y if Orientations.Vertical else wall_y + 1,
            w, h,
            Orientations.Horizontal if w < h else Orientations.Vertical
        )
