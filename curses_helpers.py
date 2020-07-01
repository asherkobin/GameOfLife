import curses
from starting_patterns import starting_patterns

class DisplayArea():
  def __init__(self, start_row_idx, start_col_idx, max_row_idx, max_col_idx):
    self.start_row_idx = start_row_idx
    self.start_col_idx = start_col_idx
    self.max_row_idx = max_row_idx
    self.max_col_idx = max_col_idx

  def get_num_rows(self):
    return self.max_row_idx - self.start_row_idx

  def get_num_cols(self):
    return self.max_col_idx - self.start_col_idx

class ScreenText():
  def __init__(self, stdscr):
    self.stdscr = stdscr

  def print(self, string, color_pair, row_idx, col_idx):
    self.stdscr.attron(curses.color_pair(color_pair))
    self.stdscr.addstr(row_idx, col_idx, string)
    self.stdscr.attroff(curses.color_pair(color_pair))

  def insert(self, string, color_pair, row_idx, col_idx):
    self.stdscr.attron(curses.color_pair(color_pair))
    self.stdscr.insstr(row_idx, col_idx, string)
    self.stdscr.attroff(curses.color_pair(color_pair))

class PatternHelper():
  def __init__(self, max_rows, max_cols):
    self.max_rows = max_rows
    self.max_cols = max_cols
    self.patterns = starting_patterns

  def get_pattern_names(self):
    return self.patterns.keys()

  def get(self, name):
    return self.patterns[name]

  def add(self, name, pattern):
    self.patterns[name] = pattern


  def rle_to_matrix(self, rle_string, max_rows, max_cols):
    rle_lines = rle_string.splitlines()
    rle_info_line = rle_lines[0]
    rle_info_parts = rle_info_line.split(", ")
    rle_info = {}

    for rle_part in rle_info_parts:
      name_value = rle_part.split(" = ")
      rle_info[name_value[0]] = name_value[1]

    num_rows = int(rle_info["y"])
    num_cols = int(rle_info["x"])

    if num_rows >= max_rows:
      raise Exception(f"Height of {rle_info['y']} is too large")
    
    if num_cols >= max_cols:
      raise Exception(f"Width of {rle_info['x']} is too large")

    if rle_info["rule"] != "B3/S23":
      raise Exception(f"Invalid format: {rle_info['rule']}")

    rle_lines = rle_lines[1:]
    rle_data = ""

    for rle_line in rle_lines:
      if rle_line[0] != "#":
        rle_data += rle_line

    matrix = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    num_str = ""
    num_int = None
    row_num = 0
    col_num = 0
    i = 0

    for i in range(len(rle_data)):
      if rle_data[i].isnumeric():
        num_str += rle_data[i]
      else:
        if num_str != "":
          num_int = int(num_str)
          num_str = ""
        if rle_data[i] == "b": # dead
          if num_int == None:
            col_num += 1
          else:
            col_num += num_int
            num_int = None
        elif rle_data[i] == "o": # alive
          if num_int == None:
            matrix[row_num][col_num] = 1
            col_num += 1
          else:
            while num_int > 0:
              matrix[row_num][col_num] = 1
              col_num += 1
              num_int -= 1
            num_int = None
        elif rle_data[i] == "$":
          if num_int == None:
            row_num += 1
          else:
            row_num += num_int
            num_int = None
          col_num = 0
        elif rle_data[i] == "!":
          break

    return matrix
  """
  x = 5, y = 18, rule = B3/S23
  3bo$
  4bo$
  o3bo$
  b4o4$
  o$b2o$
  2bo$
  2bo$
  bo3$
  3bo$
  4bo$
  o3bo$
  b4o!
  """
