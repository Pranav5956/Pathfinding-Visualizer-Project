# Enums
class Orientations:
    Horizontal = 0
    Vertical = 1


class Colors:
    White = (255, 255, 255, 255)
    Black = (0, 0, 0, 255)
    BlackHalfAlpha = (0, 0, 0, 80)
    Teal = (0, 255, 255, 255)
    Yellow = (255, 255, 0, 255)
    Red = (255, 0, 0, 255)
    Green = (0, 255, 0, 255)
    Blue = (0, 0, 255, 255)


class CellStates:
    Free = 0
    Block = 1
    Start = 2
    End = 3
    Neighbor = 4
    ShortestPath = 5


class Actions:
    Block = 0
    Start = 1
    End = 2


class GridStates:
    Edit = 0
    StartAlgorithm = 1
    RunAlgorithm = 2


# Macros
CELL_SIZE = 28
SIZE = (WIDTH, HEIGHT) = CELL_SIZE * 49, CELL_SIZE * 32
GRID_WIDTH, GRID_HEIGHT = CELL_SIZE * 33, CELL_SIZE * 27
