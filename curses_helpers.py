import curses
from starting_patterns import starting_patterns
from curses_colors import ColorPair
import time

class DisplayArea():
  def __init__(self, start_row_idx, start_col_idx, num_rows, num_cols):
    self.__start_row_idx__ = start_row_idx
    self.__start_col_idx__ = start_col_idx
    self.__num_rows__ = num_rows
    self.__num_cols__ = num_cols

  def get_top(self):
    return self.__start_row_idx__
  
  def get_left(self):
    return self.__start_col_idx__

  def get_height(self):
    return self.__num_rows__

  def get_width(self):
    return self.__num_cols__

  def get_num_rows(self):
    return self.get_height()

  def get_num_cols(self):
    return self.get_width()

  def get_start_row(self):
    return self.get_top()

  def get_start_col(self):
    return self.get_left()

class CursesScreen():
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

  def rectangle(self, start_row, start_col, num_rows, num_cols, color_pair = ColorPair.WHITE_ON_BLACK, print_bg = False):
    self.stdscr.attron(curses.color_pair(color_pair))

    self.stdscr.addch(start_row, start_col, curses.ACS_ULCORNER)
    self.stdscr.hline(start_row, start_col + 1, curses.ACS_HLINE, num_cols - 1)
    self.stdscr.addch(start_row, num_cols + start_col, curses.ACS_URCORNER)

    if print_bg:
      bg_num_lines = num_rows - 2
      bg_start_idx = 0
      while bg_num_lines > 0:
        self.stdscr.hline(start_row + 1 + bg_start_idx, start_col + 1, " ", num_cols - 1)
        bg_start_idx += 1
        bg_num_lines -= 1

    self.stdscr.vline(start_row + 1, start_col, curses.ACS_VLINE, num_rows - 2)
    self.stdscr.vline(start_row + 1, start_col + num_cols, curses.ACS_VLINE, num_rows - 2)
    

    self.stdscr.addch(start_row + num_rows -1, start_col, curses.ACS_LLCORNER)
    self.stdscr.hline(start_row + num_rows - 1, start_col + 1, curses.ACS_HLINE, num_cols - 1)
    self.stdscr.addch(start_row + num_rows - 1, start_col + num_cols, curses.ACS_LRCORNER)    
    
    self.stdscr.attroff(curses.color_pair(color_pair))

  def modal_popup(self, text, display_area, delay_secs = 5):
    text_len = len(text)
    text_row_start = display_area.get_num_rows() // 2
    text_col_start = display_area.get_num_cols() // 2 - text_len // 2

    self.rectangle(text_row_start - 2, text_col_start - 4, 5, text_len + 7, ColorPair.WHITE_ON_BLACK, True)
    self.print(text, ColorPair.CYAN_ON_BLACK, text_row_start, text_col_start)
    
    self.stdscr.refresh()

    time.sleep(delay_secs)

class RleException(Exception):
    def __init__(self, message):
      super().__init__(message)
      self.message = message

class PatternHelper():
  def __init__(self, max_rows, max_cols):
    self.max_rows = max_rows
    self.max_cols = max_cols
    self.patterns = starting_patterns

  def get_pattern_names(self):
    return self.patterns.keys()

  def get(self, name):
    return self.patterns[name]

  def add(self, pattern_name, pattern_matrix, create_file = False):
    self.patterns[pattern_name] = pattern_matrix

    if create_file:
      pattern_name = pattern_name.replace(" ", "_")
      with open(pattern_name + ".gol", "w") as pattern_file:
        for row in pattern_matrix:
          pattern_file.write(str(row) + "\n")
  
  def conwaylife_to_matrix(self, cl_string, max_rows, max_cols):
    matrix = None
    cl_lines = cl_string.splitlines()

    num_rows = 0
    num_cols = 0

    for _ in cl_lines:
      num_rows += 1

    for _ in cl_lines[0].strip():
      num_cols += 1

    matrix = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    row_num = 0
    col_num = 0

    for cl_line in cl_lines:
      cl_line = cl_line.strip()
      for cl_char in cl_line:
        if cl_char == 'O':
          matrix[row_num][col_num] = 1
        col_num += 1
      row_num += 1
      col_num = 0

    return matrix
  
  def rle_to_matrix(self, rle_string, max_rows, max_cols):
    matrix = None

    try:
      rle_lines = rle_string.splitlines()
      rle_start = 0

      for rle_line in rle_lines:
        if rle_line[0] == "#":
          rle_start += 1
        else:
          break

      rle_info_line = rle_lines[rle_start]
      rle_info_parts = rle_info_line.split(", ")
      rle_info = {}

      for rle_part in rle_info_parts:
        name_value = rle_part.split(" = ")
        rle_info[name_value[0]] = name_value[1]

      num_rows = int(rle_info["y"])
      num_cols = int(rle_info["x"])

      if num_rows >= max_rows:
        raise RleException(f"Height of {rle_info['y']} is too large")
      
      if num_cols >= max_cols:
        raise RleException(f"Width of {rle_info['x']} is too large")

      if rle_info["rule"] != "B3/S23":
        raise RleException(f"Invalid format: {rle_info['rule']}")

      rle_start += 1

      rle_lines = rle_lines[rle_start:]
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
    except RleException:
      raise
    except Exception:
      raise RleException("Invalid Format")

    return matrix

  def make_matrix_from_coords(self, cell_coordinate_sets):
    if len(cell_coordinate_sets) == 0:
      return None
    
    min_row, min_col = cell_coordinate_sets[0]
    max_row, max_col = cell_coordinate_sets[0]

    for row, col in cell_coordinate_sets:
      if row < min_row:
        min_row = row
      if col < min_col:
        min_col = col
      if row > max_row:
        max_row = row
      if col > max_col:
        max_col = col

    adj_rows = max_row - min_row + 1
    adj_cols = max_col - min_col + 1
    adj_cell_coordinate_sets = []
    
    for row, col in cell_coordinate_sets:
      adj_cell_coordinate_sets.append((row - min_row, col - min_col))

    matrix = [[0 for _ in range(adj_cols)] for _ in range(adj_rows)]

    for row_idx in range(adj_rows):
      for col_idx in range(adj_cols):
        if (row_idx, col_idx) in adj_cell_coordinate_sets:
          matrix[row_idx][col_idx] = 1
    
    return matrix

class TextInputDialog():
  def __init__(self, stdscr, display_area):
    self.display_area = display_area
    self.stdscr = stdscr

  def prompt(self, dlg_title):
    self.stdscr.clear()
    
    dlg_edit_height = 1
    
    dlg_rect = DisplayArea(14, 5, dlg_edit_height + 8, 50)
    
    dlg_top = dlg_rect.get_top()
    dlg_left = dlg_rect.get_left()
    dlg_width = dlg_rect.get_width()
    dlg_height = dlg_rect.get_height()
    
    dlg_edit_rect = DisplayArea(dlg_top + 3, dlg_left + 3, dlg_edit_height, dlg_width - 6)
    
    dlg_title = " " + dlg_title + " "
    dlg_title_left = dlg_left

    self.stdscr.attron(curses.color_pair(ColorPair.BLACK_ON_WHITE))
    self.stdscr.hline(dlg_top - 1, dlg_left, ord(' '), dlg_width)
    self.stdscr.addstr(dlg_top - 1, dlg_title_left, dlg_title)
    self.stdscr.attroff(curses.color_pair(ColorPair.BLACK_ON_WHITE))

    self.stdscr.attron(curses.color_pair(ColorPair.WHITE_ON_BLUE))
    
    self.stdscr.hline(dlg_top, dlg_left, ord(' '), dlg_width)
    
    self.stdscr.vline(dlg_top + 1, dlg_left, ord(' '), dlg_height - 1)
    self.stdscr.addch(dlg_top + 1, dlg_left + 1, curses.ACS_ULCORNER)
    self.stdscr.hline(dlg_top + 1, dlg_left + 2, curses.ACS_HLINE, dlg_width - 4)
    self.stdscr.addch(dlg_top + 1, dlg_left + dlg_width - 2, curses.ACS_URCORNER)
    self.stdscr.vline(dlg_top + 1, dlg_left + dlg_width - 1, ord(' '), dlg_height - 1)
    
    self.stdscr.hline(dlg_top + 2, dlg_left + 2, ord(' '), dlg_width - 4)
    
    self.stdscr.vline(dlg_top + 2, dlg_left + 1, curses.ACS_VLINE, dlg_edit_height + 2)
    self.stdscr.vline(dlg_top + 2, dlg_left + 2, ord(' '), dlg_edit_height + 2)
    self.stdscr.vline(dlg_top + 2, dlg_left + dlg_width - 3, ord(' '), dlg_edit_height + 2)
    self.stdscr.vline(dlg_top + 2, dlg_left + dlg_width - 2, curses.ACS_VLINE, dlg_edit_height + 2)

    self.stdscr.hline(dlg_top + dlg_edit_height + 3, dlg_left + 2, ord(' '), dlg_width - 4)

    self.stdscr.addch(dlg_top + dlg_edit_height + 4, dlg_left + 1, curses.ACS_LTEE)
    self.stdscr.hline(dlg_top + dlg_edit_height + 4, dlg_left + 2, curses.ACS_HLINE, dlg_width - 4)
    self.stdscr.addch(dlg_top + dlg_edit_height + 4, dlg_left + dlg_width - 2, curses.ACS_RTEE)
    
    self.stdscr.vline(dlg_top + dlg_edit_height + 5, dlg_left + 1, curses.ACS_VLINE, 1)
    self.stdscr.vline(dlg_top + dlg_edit_height + 5, dlg_left + dlg_width - 2, curses.ACS_VLINE, 1)
    
    self.stdscr.addch(dlg_top + dlg_edit_height + 6, dlg_left + 1, curses.ACS_LLCORNER)
    self.stdscr.hline(dlg_top + dlg_edit_height + 6, dlg_left + 2, curses.ACS_HLINE, dlg_width - 4)
    self.stdscr.addch(dlg_top + dlg_edit_height + 6, dlg_left + dlg_width - 2, curses.ACS_LRCORNER)

    dlg_help_text = "[ESC] to Cancel | [ENTER] to Save"
    dlg_help_text_top = dlg_top + dlg_edit_height + 5
    dlg_help_text_left = dlg_left + (dlg_width // 2 - len(dlg_help_text) // 2)    

    self.stdscr.hline(dlg_help_text_top, dlg_left + 2, ord(' '), dlg_width - 4)
    self.stdscr.addstr(dlg_help_text_top, dlg_help_text_left, dlg_help_text)

    self.stdscr.hline(dlg_top + dlg_edit_height + 7, dlg_left, ord(' '), dlg_width)
    
    self.stdscr.attroff(curses.color_pair(ColorPair.WHITE_ON_BLUE))

    text_input_win = curses.newwin(
      dlg_edit_rect.get_num_rows(),
      dlg_edit_rect.get_num_cols(),
      dlg_edit_rect.get_start_row(),
      dlg_edit_rect.get_start_col())
    
    self.stdscr.refresh()

    text_input = curses.textpad.Textbox(text_input_win)
    
    curses.curs_set(1)
    text_input.edit(self.handle_key_press)
    curses.curs_set(0)

    return text_input.gather().strip()

  def handle_key_press(self, key):
    if key == curses.ascii.NL:
      key = curses.ascii.BEL
    elif key == curses.ascii.ESC:
      key = curses.ascii.BEL

    return key
