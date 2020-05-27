from enum import Enum

class CellState(Enum):
  EMPTY = 1
  DEAD  = 2
  ALIVE = 3

  def __str__(self):
    default_str = super(CellState, self).__str__()
    if default_str == "CellState.EMPTY":
      return "E"
    elif default_str == "CellState.DEAD":
      return "D"
    elif default_str == "CellState.ALIVE":
      return "A"
    else:
      return "?"

class CellUnit():
  def __init__(self, value, cell_state = CellState.DEAD):
    self.value = value
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

  def __str__(self):
    return str(self.value)

class CellMatrix():
  def __init__(self, num_rows = 15, num_cols = 15):
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.matrix = [[CellUnit(0) for _ in range(num_rows)] for _ in range(num_cols)]

  def __str__(self):
    return self.get_values_grid()

  def put_cell_unit(self, cell_unit, row_idx, col_idx):
    self.matrix[row_idx][col_idx] = cell_unit

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

  def update_neighbors(self):
    self.foreach(lambda cell_unit, row_idx, col_idx : self.count_neighbors(cell_unit, row_idx, col_idx))
  
  def count_neighbors(self, cell_unit, row_idx, col_idx):
    # if cell_unit.get_state() == CellState.DEAD:
    #   return
    
    north_cell = self.get_north_cell(row_idx, col_idx)
    if north_cell and north_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()
      
    north_east_cell = self.get_north_east_cell(row_idx, col_idx)
    if north_east_cell and north_east_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    east_cell = self.get_east_cell(row_idx, col_idx)
    if east_cell and east_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()
    
    south_east_cell = self.get_south_east_cell(row_idx, col_idx)
    if south_east_cell and south_east_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()
    
    south_cell = self.get_south_cell(row_idx, col_idx)
    if south_cell and south_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    south_west_cell = self.get_south_west_cell(row_idx, col_idx)
    if south_west_cell and south_west_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    west_cell = self.get_west_cell(row_idx, col_idx)
    if west_cell and west_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

    north_west_cell = self.get_north_west_cell(row_idx, col_idx)
    if north_west_cell and north_west_cell.get_state() == CellState.ALIVE:
      cell_unit.add_neighbor()

  def get_north_cell(self, row_idx, col_idx):
    north_cell = None
    if row_idx > 0:
      north_cell = self.matrix[row_idx - 1][col_idx]
    return north_cell

  def get_south_cell(self, row_idx, col_idx):
    south_cell = None
    if row_idx < self.num_rows - 1:
      south_cell = self.matrix[row_idx + 1][col_idx]
    return south_cell

  def get_east_cell(self, row_idx, col_idx):
    east_cell = None
    if col_idx < self.num_cols - 1:
      east_cell = self.matrix[row_idx][col_idx + 1]
    return east_cell

  def get_west_cell(self, row_idx, col_idx):
    west_cell = None
    if col_idx > 0:
      west_cell = self.matrix[row_idx][col_idx - 1]
    return west_cell

  def get_north_west_cell(self, row_idx, col_idx):
    north_west_cell = None
    if row_idx > 0 and col_idx > 0:
      north_west_cell = self.matrix[row_idx - 1][col_idx - 1]
    return north_west_cell

  def get_north_east_cell(self, row_idx, col_idx):
    north_east_cell = None
    if row_idx > 0 and col_idx < self.num_cols - 1:
      north_east_cell = self.matrix[row_idx - 1][col_idx + 1]
    return north_east_cell

  def get_south_west_cell(self, row_idx, col_idx):
    south_west_cell = None
    if row_idx < self.num_rows - 1 and col_idx > 0:
      south_west_cell = self.matrix[row_idx + 1][col_idx - 1]
    return south_west_cell

  def get_south_east_cell(self, row_idx, col_idx):
    south_east_cell = None
    if row_idx < self.num_rows - 1 and col_idx < self.num_cols - 1:
      south_east_cell = self.matrix[row_idx + 1][col_idx + 1]
    return south_east_cell

  def foreach(self, fn):
    for row_idx in range(self.num_rows):
      for col_idx in range(self.num_cols):
        fn(self.matrix[row_idx][col_idx], row_idx, col_idx)

  def evolve(self):
    new_cell_matrix = CellMatrix()

    self.update_neighbors()

    for row_idx in range(self.num_rows):
      for col_idx in range(self.num_cols):
        
        cell_unit = self.matrix[row_idx][col_idx]
        
        if cell_unit.get_state() is CellState.ALIVE:
          if cell_unit.get_neighbor_count() in [2, 3]:
            new_cell_unit = CellUnit(cell_unit.value, CellState.ALIVE)
          else:
            new_cell_unit = CellUnit(cell_unit.value, CellState.DEAD)
          new_cell_matrix.put_cell_unit(new_cell_unit, row_idx, col_idx)
        
        elif cell_unit.get_state() is CellState.DEAD:
          if cell_unit.get_neighbor_count() == 3:
            new_cell_unit = CellUnit(cell_unit.value, CellState.ALIVE)
            new_cell_matrix.put_cell_unit(new_cell_unit, row_idx, col_idx)

    return new_cell_matrix


first_genration = CellMatrix()

first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 0, 0)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 1, 1)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 2, 2)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 3, 3)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 4, 4)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 5, 5)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 6, 6)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 7, 7)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 8, 8)

first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 0, 8)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 1, 7)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 2, 6)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 3, 5)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 4, 4)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 5, 3)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 6, 2)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 7, 1)
first_genration.put_cell_unit(CellUnit(0, CellState.ALIVE), 8, 0)

print(first_genration.get_pretty_grid())

next_generation = first_genration.evolve()
print(next_generation.get_pretty_grid())
next_generation = next_generation.evolve()
print(next_generation.get_pretty_grid())
next_generation = first_genration.evolve()
print(next_generation.get_pretty_grid())
next_generation = next_generation.evolve()
print(next_generation.get_pretty_grid())