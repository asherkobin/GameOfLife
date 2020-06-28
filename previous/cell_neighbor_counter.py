from cell_state import CellState

class CellNeighborCounter():
  def __init__(self, cell_matrix_navigator):
    self.navigator = cell_matrix_navigator
  
  def count_neighbors(self, cell_unit, row_idx, col_idx):
    if cell_unit.get_state() == CellState.EMPTY:
      raise ValueError("Encoutered CellState.EMPTY")

    north_cell = self.navigator.get_north_cell(row_idx, col_idx)
    if north_cell and north_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()
      
    north_east_cell = self.navigator.get_north_east_cell(row_idx, col_idx)
    if north_east_cell and north_east_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    east_cell = self.navigator.get_east_cell(row_idx, col_idx)
    if east_cell and east_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()
    
    south_east_cell = self.navigator.get_south_east_cell(row_idx, col_idx)
    if south_east_cell and south_east_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()
    
    south_cell = self.navigator.get_south_cell(row_idx, col_idx)
    if south_cell and south_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    south_west_cell = self.navigator.get_south_west_cell(row_idx, col_idx)
    if south_west_cell and south_west_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    west_cell = self.navigator.get_west_cell(row_idx, col_idx)
    if west_cell and west_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    north_west_cell = self.navigator.get_north_west_cell(row_idx, col_idx)
    if north_west_cell and north_west_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()
    
    return cell_unit.get_neighbor_count()