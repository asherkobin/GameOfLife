import os
import time
import curses
import random
from curses.textpad import rectangle
from cell_matrix_with_state import CellMatrixWithState

predefined_patterns = {
  "Cross":
    [[1, 0, 0, 0, 1],
     [0, 1, 0, 1, 0],
     [0, 0, 1, 0, 0],
     [0, 1, 0, 1, 0],
     [1, 0, 0, 0, 1]],
  "R-pentomino":
    [[0, 1, 1],
     [1, 1, 0],
     [0, 1, 0]],
  "Diehard":
    [[0, 0, 0, 0, 0, 0, 1, 0],
     [1, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 1, 1, 1]],
  "Acorn":
    [[0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0],
     [1, 1, 0, 0, 1, 1, 1]],
  "Glider":
    [[0, 1, 0],
     [0, 0, 1],
     [1, 1, 1]],
  "Line Goes Crazy":
    [[1, 1, 1, 1, 1, 0, 0, 1, 1, 1]]
}

menu_choices = [key for key in predefined_patterns.keys()]
menu_choices.append("Random Pattern")
menu_choices.append("Custom Pattern")

def get_menu_choces():
  return menu_choices

def setup_initial_pattern(cell_matrix, shape_name, display_area):
  if shape_name == "Random Pattern":
    design_width = display_area[1][0]
    design_height = display_area[1][1]
    pattern_matrix = [[0 for _ in range(design_height)] for _ in range(design_width)]
    for row_idx in range(design_width):
      for col_idx in range(design_height):
        if 1 == random.randint(1, 10):
          pattern_matrix[row_idx][col_idx] = 1
    start_row = 0
    start_col = 0
  else:
    pattern_matrix = predefined_patterns[shape_name]
    design_width = len(pattern_matrix)
    design_height = len(pattern_matrix[0])

    start_row = cell_matrix.num_rows // 2 - design_height // 2
    start_col = cell_matrix.num_cols // 2 - design_width // 2

  for row_idx in range(design_width):
    for col_idx in range(design_height):
      if pattern_matrix[row_idx][col_idx] == 1:
        cell_matrix.create_cell_unit(start_row + row_idx, start_col + col_idx)

def print_matrix(stdscr, cell_matrix, display_area):
  drew_cell = False

  # Various 4-frame animations
  
  char_chars_letters     = ["A", "B", "C", "D"]
  char_chars_cross_ticks = [chr(0x2540), chr(0x253E), chr(0x2541), chr(0x253D)]
  char_chars_tees        = [chr(0x253B), chr(0x2523), chr(0x2533), chr(0x252B)]
  char_chars_maze_lines  = [chr(0x2594), chr(0x2595), chr(0x2581), chr(0x258F)]
  char_chars_honey_comb  = [chr(0x259A), chr(0x259E), chr(0x259A), chr(0x259E)]
  char_chars_spinner     = [chr(0x007C), chr(0x002F), chr(0x002D), chr(0x005C)]

  # Other glyphs
  # Blocks: https://www.unicode.org/charts/PDF/U2580.pdf
  cell_char_circle_with_dot = u"\u2609"
  cell_char_star_burst = u"\u2600"
  cell_char_plus = u"\U0000254B"
  cell_char_block = u"\u25FC"
  cell_char_star = "*"

  use_frames = True
  
  cell_char = cell_char_block
  char_chars_animation = char_chars_letters
  
  # This is where CellMatrix is drawn to the display buffer
  
  for row_idx, row in enumerate(cell_matrix.matrix):
    for col_idx, cell_unit in enumerate(row):
      if col_idx < display_area[1][1] - 1 and row_idx < display_area[1][0] - 1:
        if cell_unit == True:
          cell_state = cell_matrix.get_cell_state(row_idx, col_idx)
          cell_age = cell_state.age
          if use_frames:
            cell_frame = cell_state.frame
            cell_char = char_chars_animation[cell_frame]

          if cell_age > 200:
            stdscr.attron(curses.color_pair(8))
            stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
            stdscr.attroff(curses.color_pair(8))
          elif cell_age > 100:
            stdscr.attron(curses.color_pair(7))
            stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
            stdscr.attroff(curses.color_pair(7))
          elif cell_age > 20:
            stdscr.attron(curses.color_pair(6))
            stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
            stdscr.attroff(curses.color_pair(6))
          elif cell_age > 10:
            stdscr.attron(curses.color_pair(5))
            stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
            stdscr.attroff(curses.color_pair(5))
          else:
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
            stdscr.attroff(curses.color_pair(4))
          drew_cell = True
  
  return drew_cell

def print_display_ui(stdscr, display_area, interval_speed, num_of_evolutions):
  # display rectangle
  rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])

  # status bar
  status_bar_text = f" Press ESC to Quit | Use ARROW UP or ARROW DOWN to Change Speed | SPACE to Pause (Any KEY for One Evolution) | Interval: {interval_speed} | Generations: {num_of_evolutions}"
  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(display_area[1][0] + 1, 0, status_bar_text)
  stdscr.addstr(display_area[1][0] + 1, 0 + len(status_bar_text), " " * ((display_area[1][1] + 1) - len(status_bar_text) - 1))
  stdscr.attroff(curses.color_pair(1))

def print_edit_ui(stdscr, display_area):
  # display rectangle
  rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])

  # status bar
  status_bar_text = " Use ARROW keys to Move | Press SPACE to toggle Cell | Press ESC to Save | Press BACKSPACE to Discard"
  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(display_area[1][0] + 1, 0, status_bar_text)
  stdscr.addstr(display_area[1][0] + 1, 0 + len(status_bar_text), " " * ((display_area[1][1] + 1) - len(status_bar_text) - 1))
  stdscr.attroff(curses.color_pair(1))

def play_gol(stdscr, shape_name, display_area):
  continue_evolution = True
  paused = False
  num_of_evolutions = 0
  delay_options = { "SLOW": 0.250, "STANDARD": 0.050, "FAST": 0.001 }
  current_delay = "STANDARD"
  
  # Performance Counters
  frames_per_sec = 0.0
  frames_per_sec_array = []

  cell_matrix = CellMatrixWithState(display_area[1][0], display_area[1][1])

  setup_initial_pattern(cell_matrix, shape_name, display_area)

  print_display_ui(stdscr, display_area, current_delay, num_of_evolutions)
  print_matrix(stdscr, cell_matrix, display_area)

  stdscr.refresh()
  
  time.sleep(0.25) # initial pause to see pattern
  
  stdscr.nodelay(1) # instruct "getch" to not block

  grid_size = display_area[1][1] * display_area[1][0]

  while True:
    frame_start_time = time.time()
    
    time.sleep(delay_options[current_delay])
    
    key = stdscr.getch()

    if continue_evolution:
      cell_matrix = cell_matrix.evolve()
    else:
      break

    num_of_evolutions += 1
    
    stdscr.erase()
    
    print_display_ui(stdscr, display_area, current_delay, num_of_evolutions)

    continue_evolution = print_matrix(stdscr, cell_matrix, display_area)
    
    if key == curses.ascii.ESC:
      stdscr.nodelay(0) # reset "getch" to block
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
        stdscr.nodelay(0) # reset "getch" to block
      else:
        stdscr.nodelay(1) # instruct "getch" to not block
    
    stdscr.addstr(0, 0, f"Rows: {display_area[1][1]} Cols: {display_area[1][0]} Cells: {grid_size} FPS: {frames_per_sec}")
    
    stdscr.refresh()

    if len(frames_per_sec_array) > 100:
      frames_per_sec_array = []
    frame_time_taken = time.time() - frame_start_time
    frames_per_sec = 1 / frame_time_taken
    frames_per_sec_array.append(frames_per_sec)
    frames_per_sec = sum(frames_per_sec_array) / len(frames_per_sec_array)
    frames_per_sec = "{:.2f}".format(frames_per_sec)
    
def make_matrix_from_coords(cell_coordinate_sets):
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

def start_pattern_creation(stdscr, display_area, custom_pattern_menu_idx): # Edit Mode
  new_pattern_name = "User Generated"
  cursor_row = display_area[1][0] // 2 
  cursor_col = display_area[1][1] // 2
  prev_cursor_row = cursor_row
  prev_cursor_col = cursor_col
  cursor_char_on = u"\u258A"
  cursor_char_off = " "
  cell_char = "*"
  add_remove_cell = False
  cell_coordinate_sets = set()
  cursor_moved = False
  cursor_was_on_cell = False
  cursor_currently_on_cell = False
  discard = False

  print_edit_ui(stdscr, display_area)
  stdscr.addstr(cursor_row, cursor_col, cursor_char_on)
  stdscr.refresh()
  
  while True:
    key = stdscr.getch()
    
    prev_cursor_col = cursor_col
    prev_cursor_row = cursor_row

    if key == curses.KEY_UP:
      cursor_row -= 1
      cursor_moved = True
    elif key == curses.KEY_DOWN:
      cursor_row += 1
      cursor_moved = True
    elif key == curses.KEY_LEFT:
      cursor_col -= 1
      cursor_moved = True
    elif key == curses.KEY_RIGHT:
      cursor_col += 1
      cursor_moved = True
    elif key == curses.ascii.SP:
      add_remove_cell = True
      cursor_was_on_cell = True
    elif key == curses.KEY_ENTER or key in [10, 13]:
      break
    elif key == curses.ascii.ESC:
      discard = True
      break

    if cursor_was_on_cell:
      stdscr.addstr(prev_cursor_row, prev_cursor_col, cell_char)

    if (cursor_row, cursor_col) in cell_coordinate_sets:
      cursor_currently_on_cell = True

    if cursor_moved:      
      if not cursor_currently_on_cell and not cursor_was_on_cell:
        stdscr.addstr(cursor_row, cursor_col, cursor_char_on)
        stdscr.addstr(prev_cursor_row, prev_cursor_col, cursor_char_off)
      elif cursor_currently_on_cell and not cursor_was_on_cell:
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(cursor_row, cursor_col, cell_char)
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(prev_cursor_row, prev_cursor_col, cursor_char_off)
        cursor_currently_on_cell = False
        cursor_was_on_cell = True
      elif not cursor_currently_on_cell and cursor_was_on_cell:
        stdscr.addstr(cursor_row, cursor_col, cursor_char_on)
        cursor_was_on_cell = False
      elif cursor_currently_on_cell and cursor_was_on_cell:
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(cursor_row, cursor_col, cell_char)
        stdscr.attroff(curses.color_pair(1))
        cursor_currently_on_cell = False
      
      cursor_moved = False
    
    elif add_remove_cell:
      if cursor_currently_on_cell:
        cell_coordinate_sets.remove((cursor_row ,cursor_col))
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(cursor_row, cursor_col, " ")
        stdscr.attroff(curses.color_pair(1))
        cursor_was_on_cell = False
        cursor_currently_on_cell = False
      else:
        cell_coordinate_sets.add((cursor_row ,cursor_col))
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(cursor_row, cursor_col, cell_char)
        stdscr.attroff(curses.color_pair(1))

  if discard:
    new_pattern_name = None
  else:
    new_pattern_name = new_pattern_name + " " + str(custom_pattern_menu_idx)
    new_pattern_matrix = make_matrix_from_coords(list(cell_coordinate_sets))
    if new_pattern_matrix != None:
      predefined_patterns[new_pattern_name] = new_pattern_matrix
    else:
      new_pattern_name = None
  
  return new_pattern_name

def print_menu(stdscr, selected_menu_idx, display_area, all_cells_are_dead):
  stdscr.erase()
  h, w = stdscr.getmaxyx()

  welcome_msg = "Welcome to the Game of Life"
  author_msg = "Implemented in Python by Asher Kobin"
  all_cells_are_dead_msg = "No Living Organisms"
  
  if h < 25:
    y = 1
  else:
    y = 10
  
  welcome_x = w // 2 - len(welcome_msg) // 2
  author_x = w // 2 - len(author_msg) // 2

  stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
  stdscr.addstr(y, welcome_x, welcome_msg)
  stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
  stdscr.attron(curses.color_pair(3))
  stdscr.addstr(y + 2, author_x, author_msg)
  stdscr.attroff(curses.color_pair(3))
  
  for idx, menu_item in enumerate(get_menu_choces()):
    x = w // 2 - len(menu_item) // 2
    y = h // 2 - len(get_menu_choces()) // 2 + idx
    if idx == selected_menu_idx:
      stdscr.attron(curses.color_pair(2))
      stdscr.addstr(y, x - 1, " ") # AKA "padding-left"
      stdscr.addstr(y, x, menu_item)
      stdscr.addstr(y, x + len(menu_item), " ") # AKA "padding-right"
      stdscr.attroff(curses.color_pair(2))
    else:
      stdscr.addstr(y, x, menu_item)

  if all_cells_are_dead:
    x = w // 2 - len(all_cells_are_dead_msg) // 2
    y = y + 5
    stdscr.addstr(y, x, all_cells_are_dead_msg)
  
  # status bar
  status_bar_text = " Use ARROW keys to Select Pattern | Press ESC to Quit"
  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(display_area[1][0] + 1, 0, status_bar_text)
  stdscr.addstr(display_area[1][0] + 1, 0 + len(status_bar_text), " " * ((display_area[1][1] + 1) - len(status_bar_text) - 1))
  stdscr.attroff(curses.color_pair(1))

  stdscr.refresh()

def setup_gol(stdscr):
  
  # hide cursor
  curses.curs_set(0)
  
  # create color sets
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Status Bar (Reversed Text)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Selected Menu Item
  curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Text
  
  curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Cell Age 1
  curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Cell Age 2
  curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Cell Age 3
  curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)     # Cell Age 4
  curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Cell Age 5

  curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Regular Text
  
  # custom colors
  curses.init_color(1, 159, 245, 173)
  curses.init_color(2, 33, 45, 37)
  curses.init_pair(20, 1, curses.COLOR_BLACK)
  curses.init_pair(30, 2, curses.COLOR_BLACK)
  
  menu_idx = 0
  custom_pattern_menu_idx = 0
  screen_hight, screen_width = stdscr.getmaxyx()
  display_area = [[0, 0], [screen_hight - 2, screen_width - 1]]
  all_cells_are_dead = False
  
  # TODO: display the rules and other interesting info
  
  print_menu(stdscr, menu_idx, display_area, all_cells_are_dead)

  while True: # breaking out of this loop will exit the application
    key = stdscr.getch()

    stdscr.erase()

    # Menu Handler

    menu_choices = get_menu_choces()

    if key == curses.KEY_UP and menu_idx > 0:
      menu_idx -= 1
    elif key == curses.KEY_DOWN and menu_idx < len(menu_choices) - 1:
      menu_idx += 1
    elif key == curses.KEY_ENTER or key in [10, 13] or key == curses.ascii.SP:
      if menu_choices[menu_idx] == "Exit":
        break
      elif menu_choices[menu_idx] == "Custom Pattern":
        new_pattern_name = start_pattern_creation(stdscr, display_area, custom_pattern_menu_idx) # Edit Mode
        if new_pattern_name != None:
          menu_choices.insert(len(menu_choices) - 1, new_pattern_name)
          custom_pattern_menu_idx += 1
      elif menu_choices[menu_idx] == "Random Pattern":
        play_gol(stdscr, menu_choices[menu_idx], display_area)
        all_cells_are_dead = True
      else:
        play_gol(stdscr, menu_choices[menu_idx], display_area) # Execute
        all_cells_are_dead = True
    elif key == curses.ascii.ESC: # Exit
      break

    print_menu(stdscr, menu_idx, display_area, all_cells_are_dead)

    stdscr.refresh()

  return all_cells_are_dead

def main():
  os.environ.setdefault("ESCDELAY", "0")
  curses.wrapper(setup_gol)

if __name__ == "__main__":
  main()