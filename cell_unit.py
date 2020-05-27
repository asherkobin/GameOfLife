from cell_state import CellState

class CellUnit():
  def __init__(self, cell_state = CellState.DEAD, value = None):
    self.__value__ = value # reserved for future use
    self.__state__ = cell_state
    self.__num_neighbors__ = 0

  def add_neighbor(self):
    self.__num_neighbors__ += 1

  def get_neighbor_count(self):
    return self.__num_neighbors__

  def get_state(self):
    return self.__state__

  def set_state(self, cell_state):
    if not isinstance(cell_state, CellState):
        raise TypeError("Invalid CellState")
    self.__state__ = cell_state

  def set_value(self, value):
    self.__value__ = value

  def get_value(self):
    return self.__value__

  def __str__(self):
    return str(self.__value__)