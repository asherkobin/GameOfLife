class CellUnit():
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return self.value

class CellMatrix():
  def __init__(self, num_rows = 10, num_cols = 10):
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.matrix = [[CellUnit(0) for _ in range(num_rows)] for _ in range(num_cols)]

  def __str__(self):
    for row in self.matrix:
      print(row)

  def get_north(self, row_idx, col_idx):
    north_value = None
    if row_idx > 0:
      north_value = self.matrix[row_idx - 1][col_idx]
    return north_value

  def get_south(self, row_idx, col_idx):
    south_value = None
    if row_idx < self.num_rows - 1:
      south_value = self.matrix[row_idx + 1][col_idx]
    return south_value

  def get_east(self, row_idx, col_idx):
    east_value = None
    if col_idx < self.num_cols - 1:
      east_value = self.matrix[row_idx][col_idx + 1]
    return east_value

  def get_west(self, row_idx, col_idx):
    west_value = None
    if col_idx > 0:
      west_value = self.matrix[row_idx][col_idx - 1]
    return west_value

  def display(self):
    print("\n")
    for row in self.matrix:
      print(row)

  def populate(self):
    for row_idx in range(self.num_rows):
      for col_idx in range(self.num_cols):
        self.matrix[row_idx][col_idx] = 1


cell_matrix = CellMatrix()

print(cell_matrix)
#
  # if row_idx > 0:
  #   north_value = universe[row_idx - 1][col_idx]
  #   num_neighbors += 1
  #   if col_idx < num_cols - 1:
  #     north_east_value = universe[row_idx][col_idx + 1]
  #     num_neighbors += 1
  #   if col_idx > 0:
  #     north_west_value = universe[row_idx][col_idx - 1]
  #     num_neighbors += 1
  # if row_idx < num_rows - 1:
  #   south_value = universe[row_idx + 1][col_idx]
  #   num_neighbors += 1
  #   if col_idx < num_cols - 1:
  #     south_east_value = universe[row_idx][col_idx + 1]
  #     num_neighbors += 1
  #   if col_idx > 0:
  #     sout_west_value = universe[row_idx][col_idx - 1]
  #     num_neighbors += 1
  # if col_idx < num_cols - 1:
  #   east_value = universe[row_idx][col_idx + 1]
  #   num_neighbors += 1
  # if col_idx > 0:
  #   west_value = universe[row_idx][col_idx - 1]
  #   num_neighbors += 1

  # return num_neighbors



# display(universe)
# populate()
# display(universe)

# val = get_num_neighbors(1, 0)
# print(val)

# for row_idx in range(num_rows):
#   for col_idx in range(num_cols):
#     num_neighbors = get_num_neighbors(row_idx, col_idx)
#     universe[row_idx][col_idx] = num_neighbors
   
# display(universe)
