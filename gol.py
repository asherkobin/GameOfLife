import os
import time
import curses
import random
from curses.textpad import rectangle
from cell_matrix import CellMatrix
from curses_colors import ColorPair, CursesColorHelper
from curses_helpers import ScreenText, PatternHelper, DisplayArea, PatternHelper
  
class GameOfLife():
  def __init__(self):
    self.stdscr = None
    self.curses_color_helper = CursesColorHelper()
    self.screen_text = None
    self.display_area = None
    self.pattern_helper = None
    self.menu_choices = None

  def start(self):
    os.environ.setdefault("ESCDELAY", "0")
    curses.wrapper(self.curses_wrapper)
  
  def curses_init(self, stdscr):
    self.stdscr = stdscr
    self.curses_color_helper.init_color_pairs()
    self.screen_text = ScreenText(stdscr)
    self.display_area = DisplayArea(0, 0, self.stdscr.getmaxyx()[0] - 2, self.stdscr.getmaxyx()[1] - 1)
    self.pattern_helper = PatternHelper(self.display_area.get_num_rows(), self.display_area.get_num_cols())
    self.menu_choices = [*self.pattern_helper.get_pattern_names()]
    self.menu_choices.append("Random Pattern")
    self.menu_choices.append("Custom Pattern")

  def curses_wrapper(self, stdscr):
    self.curses_init(stdscr)

    # hide cursor
    curses.curs_set(0)
    
    menu_idx = 0
    custom_pattern_menu_idx = 1
    
    self.print_menu(menu_idx)

    while True: # breaking out of this loop will exit the application
      key = self.stdscr.getch()

      self.stdscr.erase()

      # Menu Handler

      if key == curses.KEY_UP:
        if menu_idx > 0:
          menu_idx -= 1
        else:
          menu_idx = len(self.menu_choices) - 1
      elif key == curses.KEY_DOWN:
        if menu_idx < len(self.menu_choices) - 1:
          menu_idx += 1
        else:
          menu_idx = 0
      elif key == curses.KEY_ENTER or key in [10, 13] or key == curses.ascii.SP:
        if self.menu_choices[menu_idx] == "Exit":
          break
        elif self.menu_choices[menu_idx] == "Custom Pattern":
          new_pattern_name = self.start_pattern_creation(custom_pattern_menu_idx) # edit mode
          if new_pattern_name != None:
            self.menu_choices.insert(len(self.menu_choices) - 1, new_pattern_name)
            custom_pattern_menu_idx += 1
        elif self.menu_choices[menu_idx] == "Random Pattern":
          self.show_evolution(self.menu_choices[menu_idx]) # start with random pattern
        else:
          self.show_evolution(self.menu_choices[menu_idx]) # start with predefined pattern
      elif key == curses.ascii.ESC: # exit
        break

      self.print_menu(menu_idx)

      self.stdscr.refresh()

  def print_menu(self, selected_menu_idx):
    self.stdscr.erase()
    
    num_rows = self.display_area.get_num_rows()
    num_cols = self.display_area.get_num_cols()

    welcome_msg = "Welcome to the Game of Life"
    author_msg = "Implemented in Python by Asher Kobin"
    
    if num_rows < 40:
      start_row = 1
    else:
      start_row = 10
    
    welcome_col = num_cols // 2 - len(welcome_msg) // 2
    author_col = num_cols // 2 - len(author_msg) // 2

    self.screen_text.print(welcome_msg, ColorPair.GREEN_ON_BLACK, start_row, welcome_col)
    self.screen_text.print(author_msg, ColorPair.GREEN_ON_BLACK, start_row + 2, author_col)
    
    for idx, menu_item in enumerate(self.menu_choices):
      menu_item_row = num_rows // 2 - len(self.menu_choices) // 2 + idx
      menu_item_col = num_cols // 2 - len(menu_item) // 2
      
      if idx == selected_menu_idx:
        self.screen_text.print(" " + menu_item + " ", ColorPair.WHITE_ON_BLUE, menu_item_row, menu_item_col - 1)
      else:
        self.screen_text.print(menu_item, ColorPair.WHITE_ON_BLACK, menu_item_row, menu_item_col)
    
    # status bar
    status_bar_text = " Use ARROW keys to Select Pattern | Press ESC to Quit"
    self.screen_text.print(status_bar_text, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, 0)
    status_bar_padding = " " * ((self.display_area.max_col_idx + 2) - len(status_bar_text) - 1)
    self.screen_text.insert(status_bar_padding, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, len(status_bar_text))

    self.stdscr.refresh()

  def show_evolution(self, shape_name):
    continue_evolution = True
    paused = False
    num_of_evolutions = 0
    delay_options = { "SLOW": 0.250, "STANDARD": 0.050, "FAST": 0.001 }
    current_delay = "STANDARD"
    num_rows = self.display_area.get_num_rows()
    num_cols = self.display_area.get_num_cols()
    quit_fast = False
    
    # performance counters
    
    frames_per_sec = 0.0
    frames_per_sec_array = []

    # 1) create the matrix
    # 2) load the initial pattern
    # 3) print the ui
    # 4) print the matrix
    # 5) evolve
    # 6) goto step 3
    
    cell_matrix = CellMatrix(num_rows - 1, num_cols - 1)
  
    self.load_pattern(shape_name, cell_matrix)
    self.print_display_ui(current_delay, num_of_evolutions)
    self.print_matrix(cell_matrix)

    self.stdscr.refresh()
    
    time.sleep(0.50) # initial pause to see pattern
    
    self.stdscr.nodelay(1) # instruct "getch" to not block so keys can be captured during the animation

    grid_size = num_rows * num_cols

    while True:
      frame_start_time = time.time()
      
      time.sleep(delay_options[current_delay])
      
      key = self.stdscr.getch()

      if continue_evolution:
        cell_matrix = cell_matrix.evolve()
      else:
        break

      num_of_evolutions += 1
      
      self.stdscr.erase()
      self.print_display_ui(current_delay, num_of_evolutions)

      continue_evolution = self.print_matrix(cell_matrix)
      
      if key == curses.ascii.ESC:
        self.stdscr.nodelay(0) # reset "getch" to block
        quit_fast = True
        break
      elif key == curses.KEY_UP:
        if current_delay == "SLOW":
          current_delay = "STANDARD"
        elif current_delay == "STANDARD":
          current_delay = "FAST"
      elif key == curses.KEY_DOWN:
        if current_delay == "FAST":
          current_delay = "STANDARD"
        elif current_delay == "STANDARD":
          current_delay = "SLOW"
      elif key == curses.ascii.SP:
        paused = not paused
        if paused:
          self.stdscr.nodelay(0) # reset "getch" to block
        else:
          self.stdscr.nodelay(1) # instruct "getch" to not block
      
      self.stdscr.addstr(0, 2, f" Rows: {num_rows} Cols: {num_cols} Cells: {grid_size} FPS: {frames_per_sec} ")
      
      self.stdscr.refresh()

      if len(frames_per_sec_array) > 100:
        frames_per_sec_array = []
      frame_time_taken = time.time() - frame_start_time
      frames_per_sec = 1 / frame_time_taken
      frames_per_sec_array.append(frames_per_sec)
      frames_per_sec = sum(frames_per_sec_array) / len(frames_per_sec_array)
      frames_per_sec = "{:.2f}".format(frames_per_sec)

    if quit_fast:
      return
    
    # print goodbye msg

    goodbye_msg = "All cells have expired :("
    
    goodbye_msg_row = num_rows // 2
    goodbye_msg_col = num_cols // 2 - len(goodbye_msg) // 2

    self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
    self.stdscr.addstr(goodbye_msg_row, goodbye_msg_col, goodbye_msg)
    self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
    self.stdscr.refresh()

    time.sleep(2)

  def load_pattern(self, pattern_name, cell_matrix):
    if pattern_name == "Random Pattern":

      # create a pattern matix that will fill up the cell matrix based on living cell density
      
      pattern_matrix = [[0 for _ in range(cell_matrix.num_cols)] for _ in range(cell_matrix.num_rows)]
      
      design_rows = cell_matrix.num_rows
      design_cols = cell_matrix.num_cols
      
      start_row = 0
      start_col = 0
      
      living_cell_density = 1/10
      
      # populate the cell_matrix
      
      for row_idx in range(cell_matrix.num_rows):
        for col_idx in range(cell_matrix.num_cols):
          if 1 == random.randint(1, living_cell_density * 100):
            pattern_matrix[row_idx][col_idx] = 1
    else:

      # load a predefined pattern
      
      pattern_matrix = self.pattern_helper.get(pattern_name)
      
      design_rows = len(pattern_matrix)
      design_cols = len(pattern_matrix[0])

      # center the pattern
      
      start_row = cell_matrix.num_rows // 2 - design_rows // 2
      start_col = cell_matrix.num_cols // 2 - design_cols // 2

    for row_idx in range(design_rows):
      for col_idx in range(design_cols):
        if pattern_matrix[row_idx][col_idx] == 1:
          cell_matrix.create_cell_unit(start_row + row_idx, start_col + col_idx)

  def print_display_ui(self, interval_speed, num_of_evolutions):
    # display rectangle
    rectangle(self.stdscr,
      self.display_area.start_row_idx,
      self.display_area.start_col_idx,
      self.display_area.max_row_idx,
      self.display_area.max_col_idx)

    # status bar
    status_bar_text = f" Press ESC to Quit | Use ARROW UP or ARROW DOWN to Change Speed | SPACE to Pause (Any KEY for One Evolution) | Interval: {interval_speed} | Generations: {num_of_evolutions}"
    self.screen_text.print(status_bar_text, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, 0)
    status_bar_padding = " " * ((self.display_area.max_col_idx + 2) - len(status_bar_text) - 1)
    self.screen_text.insert(status_bar_padding, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, len(status_bar_text))

  def print_matrix(self, cell_matrix):
    drew_cell = False
    use_frames = False
    
    # various 4-frame animations
    
    char_chars_letters     = ["A", "B", "C", "D"]
    # char_chars_cross_ticks = [chr(0x2540), chr(0x253E), chr(0x2541), chr(0x253D)]
    # char_chars_tees        = [chr(0x253B), chr(0x2523), chr(0x2533), chr(0x252B)]
    # char_chars_maze_lines  = [chr(0x2594), chr(0x2595), chr(0x2581), chr(0x258F)]
    # char_chars_honey_comb  = [chr(0x259A), chr(0x259E), chr(0x259A), chr(0x259E)]
    # char_chars_spinner     = [chr(0x007C), chr(0x002F), chr(0x002D), chr(0x005C)]

    # other glyphs:
    # blocks: https://www.unicode.org/charts/PDF/U2580.pdf
    # cell_char_circle_with_dot = u"\u2609"
    # cell_char_star_burst = u"\u2600"
    # cell_char_plus = u"\U0000254B"
    # cell_char_star = "*"
    cell_char_block = u"\u25FC"

    
    char_chars_animation = char_chars_letters
    cell_char = cell_char_block
    
    # print the CellMatrix to the display buffer
    
    for row_idx, row in enumerate(cell_matrix.matrix):
      for col_idx, cell_unit in enumerate(row):
        if cell_unit == True:
          cell_state = cell_matrix.get_cell_state(row_idx, col_idx)
          cell_age = cell_state.age
          
          if use_frames:
            cell_frame = cell_state.frame
            cell_char = char_chars_animation[cell_frame]

          if cell_age == 0:
            self.screen_text.print(cell_char, ColorPair.GRADIENT_1_ON_BLACK, row_idx + 1, col_idx + 1)
          elif cell_age < 20:
            self.screen_text.print(cell_char, ColorPair.GRADIENT_2_ON_BLACK, row_idx + 1, col_idx + 1)
          elif cell_age < 50:
            self.screen_text.print(cell_char, ColorPair.GRADIENT_3_ON_BLACK, row_idx + 1, col_idx + 1)
          elif cell_age < 100:
            self.screen_text.print(cell_char, ColorPair.GRADIENT_4_ON_BLACK, row_idx + 1, col_idx + 1)
          else:
            self.screen_text.print(cell_char, ColorPair.GRADIENT_5_ON_BLACK, row_idx + 1, col_idx + 1)
          
          drew_cell = True
  
    return drew_cell # if False, then there are no living cells

  def start_pattern_creation(self, custom_pattern_menu_idx):
    new_pattern_name = "User Generated"
    num_rows = self.display_area.get_num_rows()
    num_cols = self.display_area.get_num_cols()
    cursor_row = num_rows // 2 
    cursor_col = num_cols // 2
    prev_cursor_row = cursor_row
    prev_cursor_col = cursor_col
    cursor_char_on = u"\u258A" # block
    cursor_char_off = " "
    cell_char = "*"
    cell_coordinate_list = []
    discard_work = False
    add_remove_cell = False  
    cursor_moved = False
    cursor_was_on_cell = False
    cursor_currently_on_cell = False
    
    self.print_edit_ui()

    self.screen_text.print(cursor_char_on, ColorPair.WHITE_ON_BLACK, cursor_row, cursor_col)
    self.stdscr.refresh()
    
    while True:
      key = self.stdscr.getch()

      ignore_key_press = False

      prev_cursor_col = cursor_col
      prev_cursor_row = cursor_row

      if key == curses.KEY_UP:
        if cursor_row > 1:
          cursor_row -= 1
          cursor_moved = True
      elif key == curses.KEY_DOWN:
        if cursor_row < num_rows - 1:
          cursor_row += 1
          cursor_moved = True
      elif key == curses.KEY_LEFT:
        if cursor_col > 1:
          cursor_col -= 1
          cursor_moved = True
      elif key == curses.KEY_RIGHT:
        if cursor_col < num_cols - 1:
          cursor_col += 1
          cursor_moved = True
      elif key == curses.ascii.SP:
        add_remove_cell = True
        cursor_was_on_cell = True
      elif key == curses.KEY_ENTER or key in [10, 13]:
        break
      elif key == curses.ascii.ESC:
        discard_work = True
        break
      elif key == 115: # 's'
        self.save_pattern(cell_coordinate_list)
        ignore_key_press = True
      elif key == 108: # 'l'
        matrix = self.load_rle_file()
        for row_idx in range(len(matrix)):
          for col_idx in range(len(matrix[0])):
            if matrix[row_idx][col_idx] == 1:
              cell_coordinate_list.append((row_idx + 1, col_idx + 1))
              self.screen_text.print(cell_char, ColorPair.WHITE_ON_BLACK, row_idx + 1, col_idx + 1)
      else:
        ignore_key_press = True

      if not ignore_key_press:
        if cursor_was_on_cell:
          self.screen_text.print(cursor_char_on, ColorPair.WHITE_ON_BLACK, prev_cursor_row, prev_cursor_col)

        if (cursor_row, cursor_col) in cell_coordinate_list:
          cursor_currently_on_cell = True

        if cursor_moved:      
          if not cursor_currently_on_cell and not cursor_was_on_cell:
            self.screen_text.print(cursor_char_on, ColorPair.WHITE_ON_BLACK, cursor_row, cursor_col)
            self.screen_text.print(cursor_char_off, ColorPair.WHITE_ON_BLACK, prev_cursor_row, prev_cursor_col)
          elif cursor_currently_on_cell and not cursor_was_on_cell:
            self.screen_text.print(cell_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)
            self.screen_text.print(cursor_char_off, ColorPair.WHITE_ON_BLACK, prev_cursor_row, prev_cursor_col)
            cursor_currently_on_cell = False
            cursor_was_on_cell = True
          elif not cursor_currently_on_cell and cursor_was_on_cell:
            self.screen_text.print(cursor_char_on, ColorPair.WHITE_ON_BLACK, cursor_row, cursor_col)
            self.screen_text.print(cell_char, ColorPair.WHITE_ON_BLACK, prev_cursor_row, prev_cursor_col)
            cursor_was_on_cell = False
          elif cursor_currently_on_cell and cursor_was_on_cell:
            self.screen_text.print(cell_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)
            self.screen_text.print(cell_char, ColorPair.WHITE_ON_BLACK, prev_cursor_row, prev_cursor_col)
            cursor_currently_on_cell = False
          
          cursor_moved = False
        
        elif add_remove_cell:
          if cursor_currently_on_cell:
            cell_coordinate_list.remove((cursor_row ,cursor_col))
            self.screen_text.print(cursor_char_on, ColorPair.WHITE_ON_BLACK, cursor_row, cursor_col)
            cursor_was_on_cell = False
            cursor_currently_on_cell = False
          else:
            cell_coordinate_list.append((cursor_row ,cursor_col))
            self.screen_text.print(cell_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)

    if discard_work:
      new_pattern_name = None
    else:
      new_pattern_name = new_pattern_name + " " + str(custom_pattern_menu_idx)
      new_pattern_matrix = self.make_matrix_from_coords(cell_coordinate_list)
      if new_pattern_matrix != None:
        self.pattern_helper.add(new_pattern_name, new_pattern_matrix)
      else:
        new_pattern_name = None
    
    return new_pattern_name

  def print_edit_ui(self):
    # display rectangle
    rectangle(self.stdscr,
      self.display_area.start_row_idx,
      self.display_area.start_col_idx,
      self.display_area.max_row_idx,
      self.display_area.max_col_idx)

    # status bar
    status_bar_text = " Use ARROW keys to Move | Press SPACE to toggle Cell | Press ENTER to Save | Press ESC to Discard | Press L to Load RLE File"
    self.screen_text.print(status_bar_text, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, 0)
    status_bar_padding = " " * ((self.display_area.max_col_idx + 2) - len(status_bar_text) - 1)
    self.screen_text.insert(status_bar_padding, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, len(status_bar_text))

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

  def save_pattern(self, cell_coordinate_list):
    pattern_matrix = self.make_matrix_from_coords(cell_coordinate_list)
    pattern_file = open("pattern.txt", "w")
    for row in pattern_matrix:
      pattern_file.write(str(row) + "\n")
    pattern_file.close()

  def load_rle_file(self):
    s = "x = 5, y = 18, rule = B3/S23\n3bo$4bo$o3bo$b4o4$o$b2o$2bo$2bo$bo3$3bo$4bo$o3bo$b4o!"
    s = "x = 76, y = 59, rule = B3/S23\n12bo$13b2o$12b2o2$5bo$3bobo4bo$4b2o5b2o$10b2o2$3bo$bobo$2b2o2$73bobo$73b2o$74bo11$30bo$31b2o$30b2o24$63b3o$63bo$64bo2$34b2o$35b2o$34bo!"
    pattern = self.pattern_helper.rle_to_matrix(s, self.display_area.max_row_idx, self.display_area.max_col_idx)

    return pattern

if __name__ == "__main__":
  gol = GameOfLife()
  gol.start()