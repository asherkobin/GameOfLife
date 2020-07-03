import os
import time
import curses
import curses.textpad
import curses.ascii
import random
from cell_matrix import CellMatrix
from curses_colors import ColorPair, CursesColorHelper
from curses_helpers import CursesScreen, PatternHelper, DisplayArea, PatternHelper, RleException
from edit_mode import EditMode

class GameOfLife():
  def __init__(self):
    self.stdscr = None
    self.curses_color_helper = CursesColorHelper()
    self.curses_screen = None
    self.display_area = None
    self.pattern_helper = None
    self.current_menu_choices = None
    self.edit_mode = None

  def start(self):
    os.environ.setdefault("ESCDELAY", "0")
    curses.wrapper(self.curses_wrapper)
  
  def curses_init(self, stdscr):
    self.stdscr = stdscr
    self.curses_color_helper.init_color_pairs()
    self.curses_screen = CursesScreen(stdscr)
    self.display_area = DisplayArea(0, 0, self.stdscr.getmaxyx()[0] - 2, self.stdscr.getmaxyx()[1] - 1)
    self.pattern_helper = PatternHelper(self.display_area.get_num_rows(), self.display_area.get_num_cols())
    self.edit_mode = EditMode(self.curses_screen, self.display_area, self.pattern_helper)

    self.main_menu_choices = ["Popular Patterns", "Random Pattern", "Create New Pattern", "Saved Patterns", "Load from RLE", "Quit"]
    self.pattern_menu_choices = [*self.pattern_helper.get_pattern_names()]
    self.current_menu_choices = self.main_menu_choices
    self.custom_pattern_menu_choices = []

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
          menu_idx = len(self.current_menu_choices) - 1
      elif key == curses.KEY_DOWN:
        if menu_idx < len(self.current_menu_choices) - 1:
          menu_idx += 1
        else:
          menu_idx = 0
      elif key == curses.KEY_ENTER or key in [10, 13] or key == curses.ascii.SP:
        if self.current_menu_choices is self.main_menu_choices:
          if self.main_menu_choices[menu_idx] == "Quit":
            break

          elif self.main_menu_choices[menu_idx] == "Create New Pattern":
            new_pattern_name = self.edit_mode.start(custom_pattern_menu_idx, False) # edit mode
            if new_pattern_name != None:
              self.curses_screen.modal_popup("Your new design is available under the 'Saved Patterns' menu item.", self.display_area, 3)
              self.custom_pattern_menu_choices.append(new_pattern_name)
              custom_pattern_menu_idx += 1
      
          elif self.main_menu_choices[menu_idx] == "Random Pattern":
            self.show_evolution(self.main_menu_choices[menu_idx]) # start with random pattern
        
          elif self.main_menu_choices[menu_idx] == "Popular Patterns":
            self.current_menu_choices = self.pattern_menu_choices
            menu_idx = 0
          
          elif self.main_menu_choices[menu_idx] == "Saved Patterns":
            if len(self.custom_pattern_menu_choices) > 0:
              self.current_menu_choices = self.custom_pattern_menu_choices
              menu_idx = 0

          elif self.main_menu_choices[menu_idx] == "Load from RLE":
            self.curses_screen.modal_popup("Load from RLE Not Implemented", self.display_area, 2)
          
        elif self.current_menu_choices is self.pattern_menu_choices:
          self.show_evolution(self.pattern_menu_choices[menu_idx])

        elif self.current_menu_choices is self.custom_pattern_menu_choices:
          self.show_evolution(self.custom_pattern_menu_choices[menu_idx])
      
      elif key == curses.ascii.ESC:
        if self.current_menu_choices is self.main_menu_choices: # exit
          break
        else: # back to main menu
          self.current_menu_choices = self.main_menu_choices
          menu_idx = 0

      self.print_menu(menu_idx)

      self.stdscr.refresh()

  def print_menu(self, selected_menu_idx):
    self.stdscr.erase()
    
    num_rows = self.display_area.get_num_rows()
    num_cols = self.display_area.get_num_cols()

    welcome_msg = "Welcome to the Game of Life"
    author_msg = "Implemented in Python by Asher Kobin"
    instructions_msg = "Choose from a list of popular patterns, generate a random pattern, or create your own."
    
    if num_rows < 30:
      start_row = 2
    else:
      start_row = 10

    welcome_msg_row = start_row
    author_msg_row = start_row + 2
    instructions_msg_row = start_row + 8
    
    # calculate the starting column to center the mesage
    welcome_msg_col = num_cols // 2 - len(welcome_msg) // 2
    author_msg_col = num_cols // 2 - len(author_msg) // 2
    instructions_msg_col = num_cols // 2 - len(instructions_msg) // 2

    self.curses_screen.rectangle(start_row - 2, author_msg_col - 2, start_row + 4, author_msg_col + len(author_msg) + 1, ColorPair.WHITE_ON_BLACK)

    self.curses_screen.print(welcome_msg, ColorPair.GREEN_ON_BLACK, welcome_msg_row, welcome_msg_col)
    self.curses_screen.print(author_msg, ColorPair.YELLOW_ON_BLACK, author_msg_row, author_msg_col)

    self.curses_screen.print(instructions_msg, ColorPair.WHITE_ON_BLACK, instructions_msg_row, instructions_msg_col)

    menu_start_row = start_row + 12
    
    for idx, menu_item in enumerate(self.current_menu_choices):
      menu_item_row = menu_start_row + idx
      menu_item_col = num_cols // 2 - len(menu_item) // 2
      
      if idx == selected_menu_idx:
        self.curses_screen.print(" " + menu_item + " ", ColorPair.WHITE_ON_BLUE, menu_item_row, menu_item_col - 1)
      else:
        self.curses_screen.print(menu_item, ColorPair.WHITE_ON_BLACK, menu_item_row, menu_item_col)
    
    # status bar
    status_bar_text = " Use ARROW keys to Select Option | Press ESC to Quit"
    self.curses_screen.print(status_bar_text, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, 0)
    status_bar_padding = " " * ((self.display_area.max_col_idx + 2) - len(status_bar_text) - 1)
    self.curses_screen.insert(status_bar_padding, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, len(status_bar_text))

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

    self.curses_screen.print(goodbye_msg, ColorPair.RED_ON_BLACK, goodbye_msg_row, goodbye_msg_col)

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
    # display screen border
    self.curses_screen.rectangle(
      self.display_area.start_row_idx,
      self.display_area.start_col_idx,
      self.display_area.max_row_idx,
      self.display_area.max_col_idx)

    # status bar
    status_bar_text = f" Press ESC to Quit | Use ARROW UP or ARROW DOWN to Change Speed | SPACE to Pause (Any KEY for One Evolution) | Interval: {interval_speed} | Generations: {num_of_evolutions}"
    self.curses_screen.print(status_bar_text, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, 0)
    status_bar_padding = " " * ((self.display_area.max_col_idx + 2) - len(status_bar_text) - 1)
    self.curses_screen.insert(status_bar_padding, ColorPair.BLACK_ON_WHITE, self.display_area.max_row_idx + 1, len(status_bar_text))

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
            self.curses_screen.print(cell_char, ColorPair.GRADIENT_1_ON_BLACK, row_idx + 1, col_idx + 1)
          elif cell_age < 20:
            self.curses_screen.print(cell_char, ColorPair.GRADIENT_2_ON_BLACK, row_idx + 1, col_idx + 1)
          elif cell_age < 50:
            self.curses_screen.print(cell_char, ColorPair.GRADIENT_3_ON_BLACK, row_idx + 1, col_idx + 1)
          elif cell_age < 100:
            self.curses_screen.print(cell_char, ColorPair.GRADIENT_4_ON_BLACK, row_idx + 1, col_idx + 1)
          else:
            self.curses_screen.print(cell_char, ColorPair.GRADIENT_5_ON_BLACK, row_idx + 1, col_idx + 1)
          
          drew_cell = True
  
    return drew_cell # if False, then there are no living cells

  """
  WORK IN PROGRESS
  """
  def get_text_input(self):
    #curses.curs_set(0)
    #self.get_text_input()
    #self.screen_text.modal_popup("Help!", self.display_area, 0)
    #self.stdscr.getch()
    #return
    import os
    #self.screen_text.rectangle(15, 19, 19, 70)
    #text_input_win = curses.newwin(1, 50, 20, 20)
    #text_input = curses.textpad.Textbox(text_input_win)
    
    #self.screen_text.rectangle(19, 19, 21, 70)
    
    #curses.curs_set(1)
    #text_input.edit()
    #curses.curs_set(0)
    self.stdscr.clear()
    
    self.stdscr.attron(curses.color_pair(ColorPair.WHITE_ON_BLUE))

    dlg_width = 50
    dlg_title = "Select an RLE File"
    dlg_title_start = dlg_width // 2 - len(dlg_title) // 2 + 1
    dir_entries = os.listdir()
    
    self.stdscr.addch(0, 0, curses.ACS_ULCORNER)
    self.stdscr.hline(0, 1, curses.ACS_HLINE, dlg_width)
    self.stdscr.addch(0, dlg_width + 1, curses.ACS_URCORNER)

    self.stdscr.hline(1, 1, ord(' '), dlg_width)
    self.stdscr.addstr(1, dlg_title_start, dlg_title)

    self.stdscr.vline(1, 0, curses.ACS_VLINE, 1)
    self.stdscr.vline(1, dlg_width + 1, curses.ACS_VLINE, 1)
    
    self.stdscr.addch(2, 0, curses.ACS_LTEE)
    self.stdscr.hline(2, 1, curses.ACS_HLINE, dlg_width)
    self.stdscr.addch(2, dlg_width + 1, curses.ACS_RTEE)

    _, dir_names, file_names = next(os.walk("."))
    cur_row = 3
    
    self.stdscr.addstr(cur_row, 1, "..")
    cur_row += 1
    
    for dir_name in dir_names:
      self.stdscr.addstr(cur_row, 1, "/" + dir_name)
      cur_row += 1
      if cur_row > 12:
        break

    for file_name in file_names:
      stat_info = os.stat(file_name)
      file_size = stat_info.st_size
      self.stdscr.addstr(cur_row, 1, file_name + f"    {file_size}")
      cur_row += 1
      if cur_row > 12:
        break
    
    self.stdscr.vline(3, 0, curses.ACS_VLINE, 10)
    self.stdscr.vline(3, dlg_width + 1, curses.ACS_VLINE, 10)
    
    self.stdscr.addch(13, 0, curses.ACS_LLCORNER)
    self.stdscr.hline(13, 1, curses.ACS_HLINE, dlg_width)
    self.stdscr.addch(13, dlg_width + 1, curses.ACS_LRCORNER)

    self.stdscr.attroff(curses.color_pair(ColorPair.WHITE_ON_BLUE))  
    
    self.stdscr.refresh()
    self.stdscr.getch()
    self.stdscr.clear()
    
    return "HI" #text_input.gather()

if __name__ == "__main__":
  gol = GameOfLife()
  gol.start()