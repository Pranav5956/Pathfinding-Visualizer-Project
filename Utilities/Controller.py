from Utilities.Grid import GridDisplayAlgorithm, GridEdit, pygame
from Utilities.Constants import SIZE, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, Colors, GridStates
from Utilities.Algorithms import Algorithms


class Controller:
    AlgoGridX, AlgoGridY = 2 * CELL_SIZE, 3 * CELL_SIZE
    AlgoGridPadding = 4 * CELL_SIZE

    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, CELL_SIZE)
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

                if self.state is GridStates.StartAlgorithm:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.state = GridStates.RunAlgorithm
                        for grid in self.algorithm_grids:
                            grid.run_pathfinding_algorithm()
                        self.algorithms_completed = False

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        self.state = GridStates.Edit
                        self.algorithm_grids = None
                        self.algorithms_completed = True

            if self.state is GridStates.Edit:
                self.grid.update()
                pygame.draw.rect(self.window, Colors.Black, (
                    self.grid_x, self.grid_y, GRID_WIDTH, GRID_HEIGHT
                ), CELL_SIZE // 4)

            elif self.state is GridStates.RunAlgorithm:
                self.algorithms_completed = True
                for grid in self.algorithm_grids:
                    grid.update()
                    self.algorithms_completed &= not grid.algorithm_running

                if self.algorithms_completed:
                    self.state = GridStates.StartAlgorithm
            elif self.state is GridStates.StartAlgorithm:
                for grid in self.algorithm_grids:
                    grid.draw()

            if self.state in (GridStates.StartAlgorithm, GridStates.RunAlgorithm):
                for row, col in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                    x = Controller.AlgoGridX + row * (Controller.AlgoGridPadding + GRID_WIDTH) // 2
                    y = Controller.AlgoGridY + col * (Controller.AlgoGridPadding + GRID_HEIGHT) // 2

                    pygame.draw.rect(self.window, Colors.Black, (
                        x, y, GRID_WIDTH // 2 + CELL_SIZE // 16, GRID_HEIGHT // 2 + CELL_SIZE // 16), CELL_SIZE // 8)

                    algorithm = self.algorithm_grids[row + 2 * col]
                    if algorithm.algorithm == Algorithms.BreadthFirstSearch:
                        text = self.font.render("Breadth-First Search", True, Colors.Red)
                    elif algorithm.algorithm == Algorithms.DepthFirstSearch:
                        text = self.font.render("Depth-First Search", True, Colors.Red)
                    elif algorithm.algorithm == Algorithms.Dijkstra:
                        text = self.font.render("Dijkstra's Algorithm", True, Colors.Red)
                    elif algorithm.algorithm == Algorithms.AStar:
                        text = self.font.render("A* Search Algorithm", True, Colors.Red)

                    self.window.blit(text, (x + GRID_WIDTH // 4 - text.get_width() // 2,
                                            y - Controller.AlgoGridPadding // 8 - text.get_height() // 2))

            pygame.display.update()
