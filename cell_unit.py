from cell_state import CellState

class CellUnit():
  def __init__(self, cell_state = CellState.DEAD, cell_age = 0):
    self.state = cell_state
    self.num_neighbors = 0
    self.age = cell_age
    self.frame = 0

  def set_age(self, age):
    self.age = age
    if self.age % 4 == 0 and self.age != 0:
      if self.frame == 3:
        self.frame = 0
      else:
        self.frame += 1

  def __str__(self):
    return str(f"Cell: Stage={self.state} Age={self.age}, Neighbors={self.num_neighbors}")