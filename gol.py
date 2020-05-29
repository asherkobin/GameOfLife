import os
import time
import curses
import random
from curses.textpad import rectangle
from cell_matrix import CellMatrix
from cell_state import CellState

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

menu = [key for key in predefined_patterns.keys()]
menu = ["Custom"] + menu
menu.append("Exit")

def setup_initial_pattern(cell_matrix, shape_name):
  pattern_matrix = predefined_patterns[shape_name]
  design_width = len(pattern_matrix)
  design_height = len(pattern_matrix[0])

  start_row = cell_matrix.num_rows // 2 - design_height // 2
  start_col = cell_matrix.num_cols // 2 - design_width // 2

  for row_idx in range(design_width):
    for col_idx in range(design_height):
      if pattern_matrix[row_idx][col_idx] == 1:
        cell_matrix.update_cell_unit(start_row + row_idx, start_col + col_idx, CellState.ALIVE)

def print_matrix(stdscr, cell_matrix, display_area):
  cell_char = "*"
  cell_char =  u"\u220E".encode("utf-8") # BLOCK - TODO: Randomize
  
  stdscr.attron(curses.color_pair(2))
  
  # This is where CellMatrix is drawn to the display buffer
  for row_idx, row in enumerate(cell_matrix.matrix):
    for col_idx, cell_unit in enumerate(row):
      if col_idx < display_area[1][1] - 1 and row_idx < display_area[1][0] - 1:
        if cell_unit.get_state() == CellState.ALIVE:
          stdscr.addstr(row_idx + 1, col_idx + 1, cell_char)
  
  stdscr.attroff(curses.color_pair(2))

def print_display_ui(stdscr, display_area):
  # display rectangle
  rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])

  # status bar
  status_bar_text = " Press ESC to Quit"
  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(display_area[1][0] + 1, 0, status_bar_text)
  stdscr.addstr(display_area[1][0] + 1, 0 + len(status_bar_text), " " * ((display_area[1][1] + 1) - len(status_bar_text) - 1))
  stdscr.attroff(curses.color_pair(1))

def print_edit_ui(stdscr, display_area):
  # display rectangle
  rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])

  # status bar
  status_bar_text = " Press SPACE to create a cell"
  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(display_area[1][0] + 1, 0, status_bar_text)
  stdscr.addstr(display_area[1][0] + 1, 0 + len(status_bar_text), " " * ((display_area[1][1] + 1) - len(status_bar_text) - 1))
  stdscr.attroff(curses.color_pair(1))

def play_gol(stdscr, shape_name, display_area):
  cell_matrix = CellMatrix(display_area[1][0], display_area[1][1])

  setup_initial_pattern(cell_matrix, shape_name)

  print_display_ui(stdscr, display_area)
  print_matrix(stdscr, cell_matrix, display_area)

  stdscr.refresh()
  
  stdscr.nodelay(1) # instruct "getch" to not block
  
  while True:
    key = stdscr.getch()

    time.sleep(0.25) # TODO: make variable
    next_genration = cell_matrix.evolve()
    
    stdscr.clear()    
    
    print_display_ui(stdscr, display_area)
    print_matrix(stdscr, next_genration, display_area)
    
    cell_matrix = next_genration

    if key == curses.ascii.ESC:
      stdscr.nodelay(0) # reset "getch" to block
      break
    
    stdscr.refresh()

def make_matrix_from_coords(cell_coordinate_sets):
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
  predefined_patterns[new_pattern_name] = new_pattern_matrix
  custom_idx += 1
  
  return new_pattern_name

def print_menu(stdscr, selected_menu_idx):
  stdscr.clear()
  h, w = stdscr.getmaxyx()

  for idx, item in enumerate(menu):
    x = w // 2 - len(item) // 2
    y = h // 2 - len(menu) // 2 + idx
    if idx == selected_menu_idx:
      stdscr.attron(curses.color_pair(1))
      stdscr.addstr(y, x, item)
      stdscr.attroff(curses.color_pair(1))
    else:
      stdscr.addstr(y, x, item)

  stdscr.refresh()

def setup_gol(stdscr):
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  menu_idx = 0
  screen_hight, screen_width = stdscr.getmaxyx()
  display_area = [[0, 0], [screen_hight - 2, screen_width - 1]]
  
  # TODO: Display the rules and other interesting info
  
  print_menu(stdscr, menu_idx)

  while True: # Breaking out of this loop will exit the application
    key = stdscr.getch()

    stdscr.clear()

    # Menu Handler
    global menu

    if key == curses.KEY_UP and menu_idx > 0:
      menu_idx -= 1
    elif key == curses.KEY_DOWN and menu_idx < len(menu) - 1:
      menu_idx += 1
    elif key == curses.KEY_ENTER or key in [10, 13]:
      if menu[menu_idx] == "Exit":
        break
      elif menu[menu_idx] == "Custom":
        new_pattern_name = start_pattern_creation(stdscr, display_area) # Edit Mode
        menu = [new_pattern_name] + menu
      else:
        play_gol(stdscr, menu[menu_idx], display_area) # Execute
    elif key == curses.ascii.ESC: # Exit
      break

    print_menu(stdscr, menu_idx)

    stdscr.refresh()

def main():
  os.environ.setdefault("ESCDELAY", "0")
  curses.wrapper(setup_gol)

if __name__ == "__main__":
  main()