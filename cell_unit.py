from cell_state import CellState

class CellUnit():
  def __init__(self, cell_state = CellState.DEAD, cell_age = 0):
    self.__state__ = cell_state
    self.__num_neighbors__ = 0
    self.__age__ = cell_age
    self.__frame__ = 0

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

  def get_age(self):
    return self.__age__

  def set_age(self, age):
    self.__age__ = age
    if self.__age__ % 4 == 0 and self.__age__ != 0:
      if self.__frame__ == 3:
        self.__frame__ = 0
      else:
        self.__frame__ += 1
      
  def get_frame(self):
    return self.__frame__

  def set_frame(self, frame):
    self.__frame__ = frame

  def __str__(self):
    return str(f"Cell: Stage={self.__state__} Age={self.__age__}, Neighbors={self.__num_neighbors__}")