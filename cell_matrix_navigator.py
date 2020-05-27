from cell_neighbor_counter import CellNeighborCounter

class CellMatrixNavigator():
  def __init__(self, cell_matrix, num_rows, num_cols):
    self.cell_matrix = cell_matrix
    self.num_rows = num_rows
    self.num_cols = num_rows
  
  def get_north_cell(self, row_idx, col_idx):
    north_cell = None
    if row_idx > 0:
      north_cell = self.cell_matrix.get_cell_unit(row_idx - 1, col_idx)
    return north_cell

  def get_south_cell(self, row_idx, col_idx):
    south_cell = None
    if row_idx < self.num_rows - 1:
      south_cell = self.cell_matrix.get_cell_unit(row_idx + 1, col_idx)
    return south_cell

  def get_east_cell(self, row_idx, col_idx):
    east_cell = None
    if col_idx < self.num_cols - 1:
      east_cell = self.cell_matrix.get_cell_unit(row_idx, col_idx + 1)
    return east_cell

  def get_west_cell(self, row_idx, col_idx):
    west_cell = None
    if col_idx > 0:
      west_cell = self.cell_matrix.get_cell_unit(row_idx, col_idx - 1)
    return west_cell

  def get_north_west_cell(self, row_idx, col_idx):
    north_west_cell = None
    if row_idx > 0 and col_idx > 0:
      north_west_cell = self.cell_matrix.get_cell_unit(row_idx - 1, col_idx - 1)
    return north_west_cell

  def get_north_east_cell(self, row_idx, col_idx):
    north_east_cell = None
    if row_idx > 0 and col_idx < self.num_cols - 1:
      north_east_cell = self.cell_matrix.get_cell_unit(row_idx - 1, col_idx + 1)
    return north_east_cell

  def get_south_west_cell(self, row_idx, col_idx):
    south_west_cell = None
    if row_idx < self.num_rows - 1 and col_idx > 0:
      south_west_cell = self.cell_matrix.get_cell_unit(row_idx + 1, col_idx - 1)
    return south_west_cell

  def get_south_east_cell(self, row_idx, col_idx):
    south_east_cell = None
    if row_idx < self.num_rows - 1 and col_idx < self.num_cols - 1:
      south_east_cell = self.cell_matrix.get_cell_unit(row_idx + 1, col_idx + 1)
    return south_east_cell