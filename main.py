from Utilities.Grid import Grid, pygame
from Utilities.Constants import SIZE, CELL_SIZE, Colors
from Utilities.Algorithms import Algorithms


def main():
    pygame.init()
    window = pygame.display.set_mode(size=SIZE)

    running = True
    is_dragging = False
    dragged_cells = []
    grid = Grid(window=window, row=0, col=0)

    while running:
        window.fill(Colors.White)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_dragging = True
                row, col = (pos // CELL_SIZE for pos in event.pos)
                dragged_cells.append((row, col))
                grid.on_click(row=row, col=col)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_dragging = False
                dragged_cells = []

            if event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    row, col = (pos // CELL_SIZE for pos in event.pos)
                    if (row, col) not in dragged_cells:
                        dragged_cells.append((row, col))
                        grid.on_click(row=row, col=col)

            # Execute the algorithm
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                grid.run_algorithm(algorithm=Algorithms.BreadthFirstSearch)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                grid.run_algorithm(algorithm=Algorithms.ClearGrid)

            # if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            #     grid.outer_wall_generation()
            #     grid.recursive_division_maze_generation(0, 0, Grid.CellsPerRow, Grid.CellsPerCol)

        grid.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
