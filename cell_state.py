from enum import Enum

class CellState(Enum):
  EMPTY     = 1
  DEAD      = 2
  ALIVE     = 3
  WAS_ALIVE = 4

  def __str__(self):
    default_str = super(CellState, self).__str__()
    if default_str == "CellState.EMPTY":
      return "E"
    elif default_str == "CellState.DEAD":
      return "D"
    elif default_str == "CellState.ALIVE":
      return "A"
    elif default_str == "CellState.WAS_ALIVE":
      return "W"
    else:
      return "?"
