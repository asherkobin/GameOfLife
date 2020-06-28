import os
import time
import curses
import random
from curses.textpad import rectangle
from cell_matrix_no_objects import CellMatrix

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

custom_idx = 1
refresh_timer_default = 0.002
refresh_timer = refresh_timer_default
num_of_evolutions = 0

menu_choices = [key for key in predefined_patterns.keys()]
menu_choices.append("Random Pattern")
menu_choices.append("Custom Pattern")

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
        cell_matrix.update_cell_unit(start_row + row_idx, start_col + col_idx, True)

def print_matrix(stdscr, cell_matrix, display_area):
  cell_char_circle_with_dot = u"\u2609"
  cell_char_star_burst = u"\u2600"
  cell_char_plus = u"\U0000254B"
  cell_char = cell_char_circle_with_dot # TODO: Randomize
  drew_cell = False
  char_chars = [chr(0x2540), chr(0x253E), chr(0x2541), chr(0x253D)]
  char_chars = [chr(0x253B), chr(0x2523), chr(0x2533), chr(0x252B)]
  char_chars = [chr(0x2594), chr(0x2595), chr(0x2581), chr(0x258F)]
  char_chars = [chr(0x259A), chr(0x259E), chr(0x259A), chr(0x259E)]
  char_chars = [chr(0x007C), chr(0x002F), chr(0x002D), chr(0x005C)]
  cell_char_block = u"\u25FC"
  cell_char = cell_char_block
  #cell_char = "@"
  #char_chars = ["A", "B", "C", "D"]

  # Blocks: https://www.unicode.org/charts/PDF/U2580.pdf
  
  # This is where CellMatrix is drawn to the display buffer
  
  for row_idx, row in enumerate(cell_matrix.matrix):
    for col_idx, cell_unit in enumerate(row):
      if col_idx < display_area[1][1] - 1 and row_idx < display_area[1][0] - 1:
        
        # cell_char = char_chars[cell_unit.get_frame()]
        # cell_char = char_chars[random.randint(0, 3)]
        # x = random.randint(1,20)
        # if x == 5:
        #   cell_unit.set_state(CellState.ALIVE)

        if cell_unit == True:
          stdscr.attron(curses.color_pair(20))
          stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
          stdscr.attroff(curses.color_pair(20))
          drew_cell = True
        # else:
        #   stdscr.attron(curses.color_pair(30))
        #   stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #   stdscr.attroff(curses.color_pair(30))
        
        # if cell_unit.get_state() == CellState.ALIVE:
        #   if cell_unit.get_age() > 200:
        #     stdscr.attron(curses.color_pair(8))
        #     stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #     stdscr.attroff(curses.color_pair(8))
        #   elif cell_unit.get_age() > 100:
        #     stdscr.attron(curses.color_pair(7))
        #     stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #     stdscr.attroff(curses.color_pair(7))
        #   elif cell_unit.get_age() > 20:
        #     stdscr.attron(curses.color_pair(6))
        #     stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #     stdscr.attroff(curses.color_pair(6))
        #   elif cell_unit.get_age() > 10:
        #     stdscr.attron(curses.color_pair(5))
        #     stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #     stdscr.attroff(curses.color_pair(5))
        #   else:
        #     stdscr.attron(curses.color_pair(4))
        #     stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #     stdscr.attroff(curses.color_pair(4))
        #   drew_cell = True
        # elif cell_unit.get_state() == CellState.WAS_ALIVE:
        #   stdscr.attron(curses.color_pair(10))
        #   stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #   stdscr.attroff(curses.color_pair(10))
        # elif cell_unit.get_state() == CellState.DEAD:
        #   stdscr.attron(curses.color_pair(10))
        #   stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
        #   stdscr.attroff(curses.color_pair(10))

        #continue
  return drew_cell

def print_display_ui(stdscr, display_area):
  # display rectangle
  rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])

  timer_ms = refresh_timer * 1000

  # status bar
  status_bar_text = f" Press ESC to Quit | Use ARROW UP or ARROW DOWN to Change Speed | SPACE to Pause (Any KEY for One Evolution) | Interval: {timer_ms} ms | Generations: {num_of_evolutions}"
  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(display_area[1][0] + 1, 0, status_bar_text)
  stdscr.addstr(display_area[1][0] + 1, 0 + len(status_bar_text), " " * ((display_area[1][1] + 1) - len(status_bar_text) - 1))
  stdscr.attroff(curses.color_pair(1))

def print_edit_ui(stdscr, display_area):
  # display rectangle
  rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])

  # status bar
  status_bar_text = " Use ARROW keys to Move | Press SPACE to Add Cell | BACKSPACE to Clear"
  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(display_area[1][0] + 1, 0, status_bar_text)
  stdscr.addstr(display_area[1][0] + 1, 0 + len(status_bar_text), " " * ((display_area[1][1] + 1) - len(status_bar_text) - 1))
  stdscr.attroff(curses.color_pair(1))

def play_gol(stdscr, shape_name, display_area):
  
  global refresh_timer
  global num_of_evolutions
  continue_evolution = True
  paused = False
  num_of_evolutions = 0
  refresh_timer = refresh_timer_default
  
  # Performance Counters
  frames_per_sec = 0.0
  frames_per_sec_array = []
  display_updates_sec = 0.0
  display_updates_sec_array = []
  evolution_time_independant_of_grid_size = 0.0
  evolution_time_independant_of_grid_size_array = []

  cell_matrix = CellMatrix(display_area[1][0], display_area[1][1])

  setup_initial_pattern(cell_matrix, shape_name, display_area)

  #print_display_ui(stdscr, display_area)
  print_matrix(stdscr, cell_matrix, display_area)

  stdscr.refresh()
  
  #time.sleep(1)
  stdscr.nodelay(1) # instruct "getch" to not block

  grid_size = display_area[1][1] * display_area[1][0]

  while True:

    frame_start_time = time.time()
    key = stdscr.getch()

    #time.sleep(1)

    if continue_evolution:
      start_time_evolution = time.time()
      cell_matrix = cell_matrix.evolve()
      evolution_time_taken = time.time() - start_time_evolution
      evolution_time_independant_of_grid_size = evolution_time_taken / grid_size
      evolution_time_independant_of_grid_size_array.append(evolution_time_independant_of_grid_size)
      evolution_time_independant_of_grid_size = sum(evolution_time_independant_of_grid_size_array) / len(evolution_time_independant_of_grid_size_array)
      evolution_time_independant_of_grid_size = "{:.2e}".format(evolution_time_independant_of_grid_size)
    else:
      break

    num_of_evolutions += 1
    
    stdscr.erase()
    
    #print_display_ui(stdscr, display_area)

    display_start_time = time.time()
    continue_evolution = print_matrix(stdscr, cell_matrix, display_area)
    display_time_taken = time.time() - display_start_time
    
    if key == curses.ascii.ESC:
      stdscr.nodelay(0) # reset "getch" to block
      break
    elif key == curses.KEY_UP:
      refresh_timer /= 2
    elif key == curses.KEY_DOWN:
      refresh_timer *= 2
    elif key == curses.ascii.SP:
      paused = not paused
      if paused:
        stdscr.nodelay(0) # reset "getch" to block
      else:
        stdscr.nodelay(1) # instruct "getch" to not block

###################
###################    

    
    
    stdscr.addstr(0, 0, 
      f"Rows: {display_area[1][1]} Cols: {display_area[1][0]} Cells: {grid_size}\
        ETi: {evolution_time_independant_of_grid_size} DUPS: {display_updates_sec} FPS: {frames_per_sec}")
    
    
    stdscr.refresh()

    frame_time_taken = time.time() - frame_start_time
    frames_per_sec = 1 / frame_time_taken
    frames_per_sec_array.append(frames_per_sec)
    frames_per_sec = sum(frames_per_sec_array) / len(frames_per_sec_array)
    frames_per_sec = "{:.2f}".format(frames_per_sec)
    
    display_updates_sec = 1 / display_time_taken
    display_updates_sec_array.append(display_updates_sec)
    display_updates_sec = sum(display_updates_sec_array) / len(display_updates_sec_array)
    display_updates_sec = "{:.2f}".format(display_updates_sec)
    

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

def start_pattern_creation(stdscr, display_area): # Edit Mode
  new_pattern_name = "User Generated"
  cursor_row = display_area[1][0] // 2 
  cursor_col = display_area[1][1] // 2
  prev_cursor_row = cursor_row
  prev_cursor_col = cursor_col
  cursor_char_on = u"\u258A"
  cursor_char_off = " "
  cell_char = "*"
  added_cell = False
  cell_coordinate_sets = []
  cursor_moved = False
  cursor_was_on_cell = False
  cursor_currently_on_cell = False

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
      added_cell = True
      cursor_was_on_cell = True
    elif key == curses.ascii.ESC:
      break

    if cursor_moved:
      if cursor_was_on_cell:
        stdscr.addstr(prev_cursor_row, prev_cursor_col, cell_char)

      if (cursor_row, cursor_col) in cell_coordinate_sets:
        cursor_currently_on_cell = True
      
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
    
    elif added_cell:
      cell_coordinate_sets.append((cursor_row ,cursor_col))
      stdscr.attron(curses.color_pair(1))
      stdscr.addstr(cursor_row, cursor_col, cell_char)
      stdscr.attroff(curses.color_pair(1))
      added_cell = False

  global custom_idx
  new_pattern_name = new_pattern_name + " " + str(custom_idx)
  new_pattern_matrix = make_matrix_from_coords(cell_coordinate_sets)
  if new_pattern_matrix != None:
    predefined_patterns[new_pattern_name] = new_pattern_matrix
    custom_idx += 1
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
  
  for idx, menu_item in enumerate(menu_choices):
    x = w // 2 - len(menu_item) // 2
    y = h // 2 - len(menu_choices) // 2 + idx
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

  curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)         # Regular Text
  
  curses.init_color(1, 159, 245, 173)
  curses.init_color(2, 33, 45, 37)
  curses.init_pair(20, 1, curses.COLOR_BLACK)
  curses.init_pair(30, 2, curses.COLOR_BLACK)
  
  menu_idx = 0
  screen_hight, screen_width = stdscr.getmaxyx()
  display_area = [[0, 0], [screen_hight - 2, screen_width - 1]]
  all_cells_are_dead = False
  
  play_gol(stdscr, "Random Pattern", display_area)

  return
  # TODO: Display the rules and other interesting info
  
  print_menu(stdscr, menu_idx, display_area, all_cells_are_dead)

  while True: # Breaking out of this loop will exit the application
    key = stdscr.getch()

    stdscr.erase()

    # Menu Handler
    global menu_choices

    if key == curses.KEY_UP and menu_idx > 0:
      menu_idx -= 1
    elif key == curses.KEY_DOWN and menu_idx < len(menu_choices) - 1:
      menu_idx += 1
    elif key == curses.KEY_ENTER or key in [10, 13] or key == curses.ascii.SP:
      if menu_choices[menu_idx] == "Exit":
        break
      elif menu_choices[menu_idx] == "Custom Pattern":
        new_pattern_name = start_pattern_creation(stdscr, display_area) # Edit Mode
        if new_pattern_name != None:
          menu_choices.insert(len(menu_choices) - 1, new_pattern_name)
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