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
    self.starting_patterns = starting_patterns

  def get_pattern_names(self):
    return self.starting_patterns.keys()


  def rle_to_matrix(self, rle_string):
    pass
  """
  x = 14, y = 21, rule = B3/S23
  3bo$2bobo$b2o$2bo$bobo$bo$o11bo$obo7b2obo$o4b2o3b2o$b4o4bo$5b2obo$b4o
  4bo$o4b2o3b2o$obo7b2obo$o11bo$bo$bobo$2bo$b2o$2bobo$3bo!
  """
