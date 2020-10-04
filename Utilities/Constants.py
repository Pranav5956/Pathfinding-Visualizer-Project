# Enums
class Orientations:
    Horizontal = 0
    Vertical = 1


class Colors:
    White = (255, 255, 255, 255)
    Black = (0, 0, 0, 255)
    BlackHalfAlpha = (0, 0, 0, 128)
    Teal = (0, 255, 255, 255)
    Yellow = (255, 255, 0, 255)
    Red = (255, 0, 0, 255)
    Green = (0, 255, 0, 255)


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


# Macros
SIZE = (WIDTH, HEIGHT) = 800, 600
CELL_SIZE = 20
