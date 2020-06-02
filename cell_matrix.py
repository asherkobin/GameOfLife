from cell_state import CellState
from cell_unit import CellUnit
from cell_matrix_navigator import CellMatrixNavigator
from cell_neighbor_counter import CellNeighborCounter

class CellMatrix():
  def __init__(self, height = 15, width = 15):
    self.num_rows = height
    self.num_cols = width
    self.matrix = [[CellUnit() for _ in range(self.num_cols)] for _ in range(self.num_rows)]
    self.navigator = CellMatrixNavigator(self, self.num_rows, self.num_cols)
    self.counter = CellNeighborCounter(self.navigator)

  def __str__(self):
    return self.get_values_grid()

  def update_cell_unit(self, row_idx, col_idx, cell_state, cell_age = 0):
    cell_unit = self.get_cell_unit(row_idx, col_idx)
    cell_unit.set_state(cell_state)
    cell_unit.set_age(cell_age)
    return cell_unit

  def get_cell_unit(self, row_idx, col_idx):
    return self.matrix[row_idx][col_idx]

  def get_values_grid(self):
    ret_string = ""
    for row in self.matrix:
      ret_string += "["
      for cell_unit in row:
        ret_string += str(cell_unit)
        ret_string += ", "
      ret_string = ret_string[:-2]
      ret_string += "]\n"
    return ret_string

  def get_state_grid(self):
    ret_string = ""
    for row in self.matrix:
      ret_string += "["
      for cell_unit in row:
        ret_string += str(cell_unit.get_state())
        ret_string += ", "
      ret_string = ret_string[:-2]
      ret_string += "]\n"
    return ret_string

  def get_neighbor_count_grid(self):
    ret_string = ""
    for row in self.matrix:
      ret_string += "["
      for cell_unit in row:
        ret_string += str(cell_unit.get_neighbor_count())
        ret_string += ", "
      ret_string = ret_string[:-2]
      ret_string += "]\n"
    return ret_string

  def get_pretty_grid(self):
    ret_string = ""
    for row in self.matrix:
      for cell_unit in row:
        char = " "
        if cell_unit.get_state() is CellState.ALIVE:
          char = "*"
        ret_string += char
      ret_string = ret_string[:-2]
      ret_string += "\n"
    return ret_string

  def update_neighbor_count(self):
    for row_idx in range(self.num_rows):
      for col_idx in range(self.num_cols):
        self.counter.count_neighbors(self.matrix[row_idx][col_idx], row_idx, col_idx)

  def evolve(self):
    new_cell_matrix = CellMatrix(self.num_rows, self.num_cols)

    self.update_neighbor_count()

    for row_idx in range(self.num_rows):
      for col_idx in range(self.num_cols):

        cell_unit = self.matrix[row_idx][col_idx]

        #if cell_unit.get_state() is CellState.ALIVE:
        #  new_cell_matrix.update_cell_unit(row_idx, col_idx, CellState.ALIVE)
        
        if cell_unit.get_state() is CellState.ALIVE:
          if cell_unit.get_neighbor_count() not in [2, 3]:
            new_cell_matrix.update_cell_unit(row_idx, col_idx, CellState.DEAD)
          else:
            new_cell_age = cell_unit.get_age()
            new_cell_matrix.update_cell_unit(row_idx, col_idx, CellState.ALIVE, new_cell_age + 1)
        elif cell_unit.get_state() is CellState.DEAD:
          if cell_unit.get_neighbor_count() == 3:
            new_cell_matrix.update_cell_unit(row_idx, col_idx, CellState.ALIVE)
          
    return new_cell_matrix
