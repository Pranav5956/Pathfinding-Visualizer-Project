from Utilities.Grid import pygame
from Utilities.Constants import SIZE
from Utilities.Controller import Controller


def main():
    pygame.init()
    window = pygame.display.set_mode(size=SIZE, flags=pygame.FULLSCREEN)

    Controller(window=window)

    # state = GridStates.Edit
    #
    # running = True
    # is_dragging = False
    # dragged_cells = []
    # grid = GridEdit(x=0, y=0, width=WIDTH, height=HEIGHT, window=window, cell_size=CELL_SIZE)
    #
    # algorithms = [Algorithms.BreadthFirstSearch, Algorithms.BreadthFirstSearch, Algorithms.BreadthFirstSearch, Algorithms.BreadthFirstSearch]
    # grid_run_algorithm = []
    # algorithm_running = False
    #
    # while running:
    #     window.fill(Colors.White)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #         if state is GridStates.Edit and grid is not None:
    #             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    #                 is_dragging = True
    #                 row, col = (pos // CELL_SIZE for pos in event.pos)
    #                 dragged_cells.append((row, col))
    #                 grid.click(row=row, col=col)
    #
    #             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    #                 is_dragging = False
    #                 dragged_cells = []
    #
    #             if event.type == pygame.MOUSEMOTION:
    #                 if is_dragging:
    #                     row, col = (pos // CELL_SIZE for pos in event.pos)
    #                     if (row, col) not in dragged_cells:
    #                         dragged_cells.append((row, col))
    #                         grid.click(row=row, col=col)
    #
    #             # Execute the algorithm
    #             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    #                 state = GridStates.RunAlgorithm
    #
    #                 start, end = grid.start, grid.end
    #
    #                 for i, algorithm in enumerate(algorithms):
    #                     x, y = i % 2, i // 2
    #                     created_grid = grid.grid
    #                     created_grid = [[cell for cell in row] for row in created_grid]
    #                     grid_run_algorithm.append(
    #                         GridDisplayAlgorithm(x=x * WIDTH // 2, y=y * HEIGHT // 2, width=WIDTH // 2, height=HEIGHT // 2, window=window,
    #                                              cell_size=CELL_SIZE // 2, start=start, end=end, algorithm=algorithm, grid=created_grid)
    #                     )
    #
    #                 grid = None
    #
    #         if state is GridStates.RunAlgorithm and not algorithm_running:
    #             if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
    #                 algorithm_running = True
    #
    #                 for g in grid_run_algorithm:
    #                     g.run_pathfinding_algorithm()
    #
    #             if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
    #                 is_dragging = False
    #                 dragged_cells = []
    #                 grid = GridEdit(x=0, y=0, width=WIDTH, height=HEIGHT, window=window, cell_size=CELL_SIZE)
    #
    #                 state = GridStates.Edit
    #                 grid_run_algorithm = []
    #                 algorithm_running = False
    #
    #     if state is GridStates.Edit:
    #         grid.update()
    #
    #     if state is GridStates.RunAlgorithm:
    #         for g in grid_run_algorithm:
    #             algorithm_running &= g.algorithm_running
    #             g.update()
    #
    #     pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
