from Utilities.Grid import GridDisplayAlgorithm, GridEdit, pygame
from Utilities.Constants import SIZE, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, Colors, GridStates, CellStates
from Utilities.Algorithms import Algorithms
import time
import os
from Utilities.Buttons import Button


class Controller:
    AlgoGridX, AlgoGridY = 2 * CELL_SIZE, 2 * CELL_SIZE
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
            Algorithms.BreadthFirstSearch,
            Algorithms.AStar,
            Algorithms.WAStar,
            Algorithms.Bidirectional
        ]
        self.algorithm_grids = None
        self.algorithms_completed = True
        self.timer = None
        self.completion_times = [None] * 4
        self.algorithm_attributes = [None] * 4

        def exit():
            self.running = False

        def save_grid():
            with open("save.txt", 'w') as save_file:
                save_file.write(
                    ''.join([''.join([str(cell) for cell in row]) for row in self.grid.grid])
                )
            save_file.close()

        def load_grid():
            with open("save.txt", 'r') as save_file:
                save_text = save_file.read()
                cells_per_row, cells_per_col = GRID_WIDTH // CELL_SIZE, GRID_HEIGHT // CELL_SIZE
                saved_grid = [[int(save_text[row * cells_per_row + col]) for col in range(cells_per_row)] for row in range(cells_per_col)]

                self.grid.set_grid(saved_grid)

        # Buttons
        self.edit_to_start_btn = Button(2 * self.grid_x + GRID_WIDTH, self.grid_y, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                                        "VIEW ALGORITHMS", ["#57ACFF", "#1b79e9", "#1034a6"], self._edit_to_start_transition)
        self.recursive_maze_btn = Button(2 * self.grid_x + GRID_WIDTH, self.grid_y + 4 * CELL_SIZE, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                                         "RECURSIVE MAZE", ["#D38BFF", "#a020f0", "#6a0dad"], self.grid.recursive_maze_generation)
        self.random_maze_btn = Button(2 * self.grid_x + GRID_WIDTH, self.grid_y + 8 * CELL_SIZE, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                                      "DFS MAZE", ["#D38BFF", "#a020f0", "#6a0dad"], self.grid.dfs_maze_generation)
        self.save_btn = Button(2 * self.grid_x + GRID_WIDTH, self.grid_y + 12 * CELL_SIZE, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                               "SAVE GRID", ["#FF715B", "#e7170c", "#c52820"], save_grid)
        self.load_btn = Button(2 * self.grid_x + GRID_WIDTH, self.grid_y + 16 * CELL_SIZE, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                               "LOAD GRID", ["#FF715B", "#e7170c", "#c52820"], load_grid)
        self.clear_btn = Button(2 * self.grid_x + GRID_WIDTH, self.grid_y + 20 * CELL_SIZE, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                                "CLEAR", ["#FF715B", "#e7170c", "#c52820"], self.grid.clear)
        self.exit_btn = Button(2 * self.grid_x + GRID_WIDTH, self.grid_y + 24 * CELL_SIZE, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                               "EXIT", ["#FF715B", "#e7170c", "#c52820"], exit)

        self.start_to_run_btn = Button(2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH,
                                       Controller.AlgoGridY + 4 * CELL_SIZE, 10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                                       "RUN ALGORITHMS", ["#D38BFF", "#a020f0", "#6a0dad"], self._start_to_run_transition, False)
        self.start_to_edit_btn = Button(2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH, Controller.AlgoGridY,
                                        10 * CELL_SIZE, 3 * CELL_SIZE, 10,
                                        "BACK TO EDITING", ["#57ACFF", "#1b79e9", "#1034a6"], self._start_to_edit_transition, False)

        self.buttons = [
            self.edit_to_start_btn,
            self.recursive_maze_btn,
            self.random_maze_btn,
            self.start_to_edit_btn,
            self.start_to_run_btn,
            self.clear_btn,
            self.exit_btn,
            self.save_btn,
            self.load_btn
        ]

        # Images
        self.title = pygame.image.load(os.path.join('Resources', 'Title.png'))

        self._update()

    def _make_grid_copy(self):
        return [[cell for cell in row] for row in self.grid.grid]

    def _get_row_col(self, mouse_pos):
        x, y = mouse_pos
        if self.grid_x < x < self.grid_x + GRID_WIDTH and self.grid_y < y < self.grid_y + GRID_HEIGHT:
            return (x - self.grid_x) // CELL_SIZE, (y - self.grid_y) // CELL_SIZE
        return None, None

    def _edit_to_start_transition(self):
        if self.grid.start and self.grid.end:
            self.state = GridStates.StartAlgorithm
            self.edit_to_start_btn.toggle(False)
            self.recursive_maze_btn.toggle(False)
            self.random_maze_btn.toggle(False)
            self.clear_btn.toggle(False)
            self.exit_btn.toggle(False)
            self.save_btn.toggle(False)
            self.load_btn.toggle(False)

            self.algorithm_grids = [
                GridDisplayAlgorithm(x=Controller.AlgoGridX + (i % 2) * (GRID_WIDTH + Controller.AlgoGridPadding) // 2,
                                     y=Controller.AlgoGridY + (i // 2) * (GRID_HEIGHT + Controller.AlgoGridPadding) // 2,
                                     width=GRID_WIDTH // 2, height=GRID_HEIGHT // 2,
                                     window=self.window, cell_size=CELL_SIZE // 2, start=self.grid.start, end=self.grid.end,
                                     algorithm=algorithm, grid=self._make_grid_copy())
                for i, algorithm in enumerate(self.algorithms)
            ]

            self.start_to_edit_btn.toggle(True)
            self.start_to_run_btn.toggle(True)

    def _start_to_run_transition(self):
        self.state = GridStates.RunAlgorithm
        self.timer = time.time()
        self.completion_times = [None] * 4
        self.algorithm_attributes = [None] * 4
        for grid in self.algorithm_grids:
            grid.run_pathfinding_algorithm()
        self.algorithms_completed = False

    def _start_to_edit_transition(self):
        self.edit_to_start_btn.toggle(True)
        self.edit_to_start_btn.click_buffer = 20
        self.recursive_maze_btn.toggle(True)
        self.random_maze_btn.toggle(True)
        self.clear_btn.toggle(True)
        self.exit_btn.toggle(True)
        self.save_btn.toggle(True)
        self.load_btn.toggle(True)

        self.start_to_edit_btn.toggle(False)
        self.start_to_run_btn.toggle(False)

        self.state = GridStates.Edit
        self.algorithm_grids = None
        self.algorithms_completed = True
        self.completion_times = [None] * 4
        self.algorithm_attributes = [None] * 4

    def _update(self):
        while self.running:
            self.window.fill(Colors.White)

            # if self.state is GridStates.Edit:
                # self.window.blit(self.title, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                for button in self.buttons:
                    if button.enabled:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            button.click(event.pos)

                        if event.type == pygame.MOUSEMOTION:
                            button.hover(event.pos)

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
                    for i, grid in enumerate(self.algorithm_grids):
                        self.algorithm_attributes[i] = grid.get_stats()
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

                    index = row + 2 * col

                    pygame.draw.rect(self.window, Colors.Black, (
                        x, y, GRID_WIDTH // 2 + CELL_SIZE // 16, GRID_HEIGHT // 2 + CELL_SIZE // 16), CELL_SIZE // 8)

                    algorithm = self.algorithm_grids[index]
                    algorithm_name, algorithm_desc = "", ""
                    if algorithm.algorithm == Algorithms.BreadthFirstSearch:
                        algorithm_name = "Breadth-First Search"
                        algorithm_desc = "Guarantees shortest-path"
                    elif algorithm.algorithm == Algorithms.DepthFirstSearch:
                        algorithm_name = "Depth-First Search"
                        algorithm_desc = "Does not guarantee shortest-path"
                    elif algorithm.algorithm == Algorithms.WAStar:
                        algorithm_name = "Weighted A* (w=1.2)"
                        algorithm_desc = "Guarantees shortest-path"
                    elif algorithm.algorithm == Algorithms.AStar:
                        algorithm_name = "A* Algorithm"
                        algorithm_desc = "Guarantees shortest-path"
                    elif algorithm.algorithm == Algorithms.Bidirectional:
                        algorithm_name = "Bidirectional A*"
                        algorithm_desc = "Guarantees shortest-path"

                    text = self.title_font.render(algorithm_name, True, Colors.Blue)
                    text2 = self.desc_font.render(algorithm_desc, True, Colors.BlackHalfAlpha)

                    self.window.blit(text, (x, y - Controller.AlgoGridPadding // 5 - text.get_height()))
                    self.window.blit(text2, (x, y - Controller.AlgoGridPadding // 16 - text.get_height() // 2))

                    if type(self.algorithm_attributes[index]) == list:
                        cells_considered, cost, reachable = self.algorithm_attributes[index]
                        completion_time = round(self.completion_times[index] - self.timer, 4)
                        algorithm_text = self.title_font.render(algorithm_name, True, Colors.Blue)
                        time_taken_color = get_color_level(self.completion_times[index], min(self.completion_times), max(self.completion_times))
                        time_taken_text = self.desc_font.render("Time Taken: " + str(completion_time) + "s", True, time_taken_color)
                        cells_considered_color = get_color_level(cells_considered, min([val[0] for val in self.algorithm_attributes]),
                                                                 max([val[0] for val in self.algorithm_attributes]))
                        cells_considered_text = self.desc_font.render("Number of cells considered : " + str(cells_considered), True, cells_considered_color)
                        cost_color = get_color_level(cost, min([val[1] for val in self.algorithm_attributes]),
                                                     max([val[1] for val in self.algorithm_attributes]))
                        cost_text = self.desc_font.render("Cost of Path : " + str(cost), True, cost_color)
                        reachable_color = get_color_level(reachable, min([val[2] for val in self.algorithm_attributes]),
                                                          max([val[2] for val in self.algorithm_attributes]))
                        reachable_text = self.desc_font.render("Reachable? : Yes" if reachable else "Reachable? : No", True, reachable_color)

                        analysis_text = self.title_font.render("COMPARATIVE ANALYSIS", True, Colors.Black)
                        self.window.blit(analysis_text, (
                            2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH + 5 * CELL_SIZE - analysis_text.get_width() // 2,
                            Controller.AlgoGridY + 8 * CELL_SIZE))

                        pygame.draw.rect(self.window, Colors.BlackHalfAlpha,
                                         (1.9 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH,
                                          Controller.AlgoGridY + 7.75 * CELL_SIZE + index * 5 * CELL_SIZE + 2 * CELL_SIZE,
                                          10 * CELL_SIZE + 0.2 * Controller.AlgoGridX, 4.5 * CELL_SIZE), 2)
                        self.window.blit(algorithm_text, (2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH + 5 * CELL_SIZE - algorithm_text.get_width() // 2,
                                                          Controller.AlgoGridY + 8 * CELL_SIZE + index * 5 * CELL_SIZE + 2 * CELL_SIZE))
                        self.window.blit(time_taken_text, (2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH,
                                                           Controller.AlgoGridY + 9.25 * CELL_SIZE + index * 5 * CELL_SIZE + 2 * CELL_SIZE))
                        self.window.blit(cells_considered_text, (2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH,
                                                                 Controller.AlgoGridY + 10 * CELL_SIZE + index * 5 * CELL_SIZE + 2 * CELL_SIZE))
                        self.window.blit(cost_text, (2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH,
                                                     Controller.AlgoGridY + 10.75 * CELL_SIZE + index * 5 * CELL_SIZE + 2 * CELL_SIZE))
                        self.window.blit(reachable_text, (2 * Controller.AlgoGridX + Controller.AlgoGridPadding // 4 + GRID_WIDTH,
                                                          Controller.AlgoGridY + 11.5 * CELL_SIZE + index * 5 * CELL_SIZE + 2 * CELL_SIZE))

            for button in self.buttons:
                button.draw(window=self.window)
            pygame.display.update()


def get_color_level(value, minimum, maximum):
    # if minimum == maximum:
    #     return Colors.Black
    # if value == minimum:
    #     return Colors.Green
    # if value == maximum:
    #     return Colors.Red
    return Colors.Black
