from Utilities.Grid import GridDisplayAlgorithm, GridEdit, pygame
from Utilities.Constants import SIZE, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, Colors, GridStates
from Utilities.Algorithms import Algorithms
import time


class Controller:
    AlgoGridX, AlgoGridY = 2 * CELL_SIZE, 3 * CELL_SIZE
    AlgoGridPadding = 4 * CELL_SIZE

    def __init__(self, window):
        self.window = window
        self.title_font = pygame.font.Font(None, (8 * CELL_SIZE) // 7)
        self.desc_font = pygame.font.Font(None, (4 * CELL_SIZE) // 5)
        self.state = GridStates.Edit

        self.running = True

        # Dragging controllers
        self.current_selected_cell = None

        # Grid
        self.grid_x, self.grid_y = CELL_SIZE * 2, CELL_SIZE * 4
        self.grid = GridEdit(x=self.grid_x, y=self.grid_y, width=GRID_WIDTH, height=GRID_HEIGHT, window=self.window, cell_size=CELL_SIZE)

        # Algorithm controllers
        self.algorithms = [
            Algorithms.DepthFirstSearch,
            Algorithms.BreadthFirstSearch,
            Algorithms.Dijkstra,
            Algorithms.AStar
        ]
        self.algorithm_grids = None
        self.algorithms_completed = True
        self.timer = None
        self.completion_times = [None] * 4

        self._update()

    def _make_grid_copy(self):
        return [[cell for cell in row] for row in self.grid.grid]

    def _get_row_col(self, mouse_pos):
        x, y = mouse_pos
        if not self.grid_x <= x <= self.grid_x + GRID_WIDTH and self.grid_y <= y <= self.grid_y + GRID_HEIGHT:
            return None, None
        return (x - self.grid_x) // CELL_SIZE, (y - self.grid_y) // CELL_SIZE

    def _update(self):
        while self.running:
            self.window.fill(Colors.White)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                if self.state is GridStates.Edit:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        row, col = self._get_row_col(event.pos)

                        if row is not None and col is not None:
                            self.grid.click(row=row, col=col)
                            self.current_selected_cell = (row, col)

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.current_selected_cell = None

                    if event.type == pygame.MOUSEMOTION:
                        if self.current_selected_cell is not None:
                            row, col = self._get_row_col(event.pos)

                            # If dragged inside the grid, check if its a new cell and change it
                            if row is not None and col is not None and not self.current_selected_cell == (row, col):
                                self.grid.click(row=row, col=col)
                                self.current_selected_cell = (row, col)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.state = GridStates.StartAlgorithm

                        self.algorithm_grids = [
                            GridDisplayAlgorithm(x=Controller.AlgoGridX + (i % 2) * (GRID_WIDTH + Controller.AlgoGridPadding) // 2,
                                                 y=Controller.AlgoGridY + (i // 2) * (GRID_HEIGHT + Controller.AlgoGridPadding) // 2,
                                                 width=GRID_WIDTH // 2, height=GRID_HEIGHT // 2,
                                                 window=self.window, cell_size=CELL_SIZE // 2, start=self.grid.start, end=self.grid.end,
                                                 algorithm=algorithm, grid=self._make_grid_copy())
                            for i, algorithm in enumerate(self.algorithms)
                        ]

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                        self.grid.clear()

                if self.state is GridStates.StartAlgorithm:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.state = GridStates.RunAlgorithm
                        self.timer = time.time()
                        self.completion_times = [None] * 4
                        for grid in self.algorithm_grids:
                            grid.run_pathfinding_algorithm()
                        self.algorithms_completed = False

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        self.state = GridStates.Edit
                        self.algorithm_grids = None
                        self.algorithms_completed = True
                        self.completion_times = [None] * 4

            if self.state is GridStates.Edit:
                self.grid.update()
                pygame.draw.rect(self.window, Colors.Black, (
                    self.grid_x, self.grid_y, GRID_WIDTH, GRID_HEIGHT
                ), CELL_SIZE // 4)

            elif self.state is GridStates.RunAlgorithm:
                self.algorithms_completed = True
                for i, grid in enumerate(self.algorithm_grids):
                    grid.update()
                    self.algorithms_completed &= not grid.algorithm_running

                    if not grid.algorithm_running and self.completion_times[i] is None:
                        self.completion_times[i] = time.time()

                    x = Controller.AlgoGridX + (i % 2) * (Controller.AlgoGridPadding + GRID_WIDTH) // 2
                    y = Controller.AlgoGridY + (i // 2) * (Controller.AlgoGridPadding + GRID_HEIGHT) // 2
                    if self.completion_times[i] is not None:
                        text = self.desc_font.render("Finish Time: %.2fs" % (self.completion_times[i] - self.timer), True, Colors.Green)
                    elif self.timer is not None:
                        text = self.desc_font.render("Time Elapsed: %.2fs" % (time.time() - self.timer), True, Colors.Red)
                    self.window.blit(text, (x + GRID_WIDTH // 2 - text.get_width(),
                                            y - Controller.AlgoGridPadding // 10 - text.get_height() // 2))

                if self.algorithms_completed:
                    self.state = GridStates.StartAlgorithm
                    # self.timer = None

            elif self.state is GridStates.StartAlgorithm:
                for i, grid in enumerate(self.algorithm_grids):
                    grid.draw()

                    if self.completion_times[i] is not None:
                        x = Controller.AlgoGridX + (i % 2) * (Controller.AlgoGridPadding + GRID_WIDTH) // 2
                        y = Controller.AlgoGridY + (i // 2) * (Controller.AlgoGridPadding + GRID_HEIGHT) // 2
                        text = self.desc_font.render("Finish Time: %.2fs" % (self.completion_times[i] - self.timer), True, Colors.Green)
                        self.window.blit(text, (x + GRID_WIDTH // 2 - text.get_width(),
                                                y - Controller.AlgoGridPadding // 10 - text.get_height() // 2))

            if self.state in (GridStates.StartAlgorithm, GridStates.RunAlgorithm):
                for row, col in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                    x = Controller.AlgoGridX + row * (Controller.AlgoGridPadding + GRID_WIDTH) // 2
                    y = Controller.AlgoGridY + col * (Controller.AlgoGridPadding + GRID_HEIGHT) // 2

                    pygame.draw.rect(self.window, Colors.Black, (
                        x, y, GRID_WIDTH // 2 + CELL_SIZE // 16, GRID_HEIGHT // 2 + CELL_SIZE // 16), CELL_SIZE // 8)

                    algorithm = self.algorithm_grids[row + 2 * col]
                    if algorithm.algorithm == Algorithms.BreadthFirstSearch:
                        text = self.title_font.render("Breadth-First Search", True, Colors.Blue)
                        text2 = self.desc_font.render("Guarantees shortest-path", True, Colors.BlackHalfAlpha)
                    elif algorithm.algorithm == Algorithms.DepthFirstSearch:
                        text = self.title_font.render("Depth-First Search", True, Colors.Blue)
                        text2 = self.desc_font.render("Does not guarantee shortest-path", True, Colors.BlackHalfAlpha)
                    elif algorithm.algorithm == Algorithms.Dijkstra:
                        text = self.title_font.render("Dijkstra's Algorithm", True, Colors.Blue)
                        text2 = self.desc_font.render("Guarantees shortest-path", True, Colors.BlackHalfAlpha)
                    elif algorithm.algorithm == Algorithms.AStar:
                        text = self.title_font.render("A* Search Algorithm", True, Colors.Blue)
                        text2 = self.desc_font.render("Guarantees shortest-path", True, Colors.BlackHalfAlpha)

                    self.window.blit(text, (x, y - Controller.AlgoGridPadding // 5 - text.get_height()))
                    self.window.blit(text2, (x, y - Controller.AlgoGridPadding // 16 - text.get_height() // 2))

            pygame.display.update()
