from cell_state import CellState
from cell_unit import CellUnit
import random
from itertools import product

class CellMatrix():
  def __init__(self, height = 15, width = 15):
    self.num_rows = height
    self.num_cols = width
    self.matrix = [[CellUnit() for _ in range(self.num_cols)] for _ in range(self.num_rows)]

  def __str__(self):
    return self.get_values_grid()

  def update_cell_unit(self, row_idx, col_idx, cell_state, cell_age = 0, cell_frame = 0):
    cell_unit = self.get_cell_unit(row_idx, col_idx)
    cell_unit.state = cell_state
    cell_unit.frame = cell_frame
    cell_unit.age = cell_age
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

  def get_neighbor_count(self, row_idx, col_idx):
    n_count = 0

    if row_idx > 0:
      north_cell = self.matrix[row_idx - 1][col_idx]
      if north_cell.state is CellState.ALIVE:
        n_count += 1
    
    if row_idx < self.num_rows - 1:
      south_cell = self.matrix[row_idx + 1][col_idx]
      if south_cell.state is CellState.ALIVE:
        n_count += 1
    
    if col_idx < self.num_cols - 1:
      east_cell = self.matrix[row_idx][col_idx + 1]
      if east_cell.state is CellState.ALIVE:
        n_count += 1

    if col_idx > 0:
      west_cell = self.matrix[row_idx][col_idx - 1]
      if west_cell.state is CellState.ALIVE:
        n_count += 1

    if row_idx > 0 and col_idx > 0:
      north_west_cell = self.matrix[row_idx - 1][col_idx - 1]
      if north_west_cell.state is CellState.ALIVE:
        n_count += 1

    if row_idx > 0 and col_idx < self.num_cols - 1:
      north_east_cell = self.matrix[row_idx - 1][col_idx + 1]
      if north_east_cell.state is CellState.ALIVE:
        n_count += 1
    
    if row_idx < self.num_rows - 1 and col_idx > 0:
      south_west_cell = self.matrix[row_idx + 1][col_idx - 1]
      if south_west_cell.state is CellState.ALIVE:
        n_count += 1
    
    if row_idx < self.num_rows - 1 and col_idx < self.num_cols - 1:
      south_east_cell = self.matrix[row_idx + 1][col_idx + 1]
      if south_east_cell.state is CellState.ALIVE:
        n_count += 1
    
    return n_count

  def evolve(self):
    new_cell_matrix = CellMatrix(self.num_rows, self.num_cols)

    for row_idx in range(self.num_rows):
      for col_idx in range(self.num_cols):

        cell_unit = self.matrix[row_idx][col_idx]
        is_alive = cell_unit.state == CellState.ALIVE
        n_count = self.get_neighbor_count(row_idx, col_idx)
        
        if is_alive:
          if n_count not in [2, 3]:
            new_cell_unit = CellUnit(CellState.DEAD)
            new_cell_matrix.matrix[row_idx][col_idx] = new_cell_unit
          else:
            new_cell_unit = CellUnit(CellState.ALIVE)
            new_cell_unit.age = cell_unit.age + 1
            new_cell_matrix.matrix[row_idx][col_idx] = new_cell_unit
        else:
          if n_count == 3:
            new_cell_unit = CellUnit(CellState.ALIVE)
            new_cell_matrix.matrix[row_idx][col_idx] = new_cell_unit
          
    return new_cell_matrix