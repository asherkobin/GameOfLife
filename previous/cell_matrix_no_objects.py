
import random

class CellMatrix():
  def __init__(self, height = 15, width = 15):
    self.num_rows = height
    self.num_cols = width
    self.matrix = [[False for _ in range(self.num_cols)] for _ in range(self.num_rows)]

  def __str__(self):
    return self.matrix

  def update_cell_unit(self, row_idx, col_idx, is_alive, cell_age = 0, cell_frame = 0):
    self.matrix[row_idx][col_idx] = is_alive

  def get_cell_unit(self, row_idx, col_idx):
    return self.matrix[row_idx][col_idx]

  def get_neighbor_count(self, row_idx, col_idx):
    n_count = 0

    if row_idx > 0:
      north_cell = self.matrix[row_idx - 1][col_idx]
      if north_cell:
        n_count += 1
    
    if row_idx < self.num_rows - 1:
      south_cell = self.matrix[row_idx + 1][col_idx]
      if south_cell:
        n_count += 1
    
    if col_idx < self.num_cols - 1:
      east_cell = self.matrix[row_idx][col_idx + 1]
      if east_cell:
        n_count += 1

    if col_idx > 0:
      west_cell = self.matrix[row_idx][col_idx - 1]
      if west_cell:
        n_count += 1

    if row_idx > 0 and col_idx > 0:
      north_west_cell = self.matrix[row_idx - 1][col_idx - 1]
      if north_west_cell:
        n_count += 1

    if row_idx > 0 and col_idx < self.num_cols - 1:
      north_east_cell = self.matrix[row_idx - 1][col_idx + 1]
      if north_east_cell:
        n_count += 1
    
    if row_idx < self.num_rows - 1 and col_idx > 0:
      south_west_cell = self.matrix[row_idx + 1][col_idx - 1]
      if south_west_cell:
        n_count += 1
    
    if row_idx < self.num_rows - 1 and col_idx < self.num_cols - 1:
      south_east_cell = self.matrix[row_idx + 1][col_idx + 1]
      if south_east_cell:
        n_count += 1
    
    return n_count

  def evolve(self):
    new_cell_matrix = CellMatrix(self.num_rows, self.num_cols)

    for row_idx in range(self.num_rows):
      for col_idx in range(self.num_cols):
        
        is_alive = self.matrix[row_idx][col_idx]
        n_count = self.get_neighbor_count(row_idx, col_idx)
        
        if is_alive == True:
          if n_count not in [2, 3]:
            new_cell_matrix.matrix[row_idx][col_idx] = False
          else:
            new_cell_matrix.matrix[row_idx][col_idx] = True
        else:
          if n_count == 3:
            new_cell_matrix.matrix[row_idx][col_idx] = True
          
    return new_cell_matrix
