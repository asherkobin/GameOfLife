import os
import time
import curses
from curses.textpad import rectangle
from cell_matrix import CellMatrix
from cell_state import CellState

def test_gol():
  first_genration = CellMatrix()

  first_genration.update_cell_unit(0, 0, CellState.ALIVE)
  first_genration.update_cell_unit(1, 1, CellState.ALIVE)
  first_genration.update_cell_unit(2, 2, CellState.ALIVE)
  first_genration.update_cell_unit(3, 3, CellState.ALIVE)
  first_genration.update_cell_unit(4, 4, CellState.ALIVE)


  first_genration.update_cell_unit(0, 4, CellState.ALIVE)
  first_genration.update_cell_unit(1, 3, CellState.ALIVE)
  first_genration.update_cell_unit(2, 2, CellState.ALIVE)
  first_genration.update_cell_unit(3, 1, CellState.ALIVE)
  first_genration.update_cell_unit(4, 0, CellState.ALIVE)

  # print(first_genration.get_values_grid())
  # print(first_genration.get_state_grid())

  print("1")
  print(first_genration.get_pretty_grid())
  next_generation = first_genration.evolve()
  print("2")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("3")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("4")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("5")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("6")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("7")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("8")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("9")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("10")
  print(next_generation.get_pretty_grid())
  next_generation = next_generation.evolve()
  print("11")
  print(next_generation.get_pretty_grid())

def setup_initial_pattern(cell_matrix):
  design_width = 5
  design_height = 5

  start_row = cell_matrix.num_rows // 2 - design_height // 2
  start_col = cell_matrix.num_cols // 2 - design_width // 2
  
  cell_matrix.update_cell_unit(start_row + 0, start_col + 0, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 1, start_col + 1, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 2, start_col + 2, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 3, start_col + 3, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 4, start_col + 4, CellState.ALIVE)

  cell_matrix.update_cell_unit(start_row + 0, start_col + 4, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 1, start_col + 3, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 2, start_col + 2, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 3, start_col + 1, CellState.ALIVE)
  cell_matrix.update_cell_unit(start_row + 4, start_col + 0, CellState.ALIVE)

def print_matrix(stdscr, cell_matrix):
  stdscr.attron(curses.color_pair(2))
  for row_idx, row in enumerate(cell_matrix.matrix):
    for col_idx, cell_unit in enumerate(row):
      if cell_unit.get_state() == CellState.ALIVE:
        stdscr.addstr(row_idx + 1, col_idx + 1, "*")
  stdscr.attroff(curses.color_pair(2))

def play_gol(stdscr):
  sh, sw = stdscr.getmaxyx()
  display_area = [[0, 0], [sh - 2, sw - 1]]
  cell_matrix = CellMatrix(display_area[1][0], display_area[1][1])
  cursor_pos = [5,5]

  setup_initial_pattern(cell_matrix)

  rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])
  print_matrix(stdscr, cell_matrix)
  #stdscr.addstr(cursor_pos[0], cursor_pos[1], "*")

  stdscr.refresh()
  
  while True:
    
    key = stdscr.getch()

    next_genration = cell_matrix.evolve()
    
    stdscr.clear()    
    rectangle(stdscr, display_area[0][0], display_area[0][1], display_area[1][0], display_area[1][1])
    print_matrix(stdscr, next_genration)
    
    cell_matrix = next_genration
    
    if key == curses.KEY_UP:
      cursor_pos[0] -= 1
    elif key == curses.KEY_DOWN:
      cursor_pos[0] += 1
    elif key == curses.KEY_LEFT:
      cursor_pos[1] -= 1
    elif key == curses.KEY_RIGHT:
      cursor_pos[1] += 1
    elif key == curses.ascii.ESC:
      break

    #stdscr.addstr(cursor_pos[0], cursor_pos[1], "*")
    
    stdscr.refresh()

menu = ["Play", "Exit"]

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
  
  print_menu(stdscr, menu_idx)

  while True:
    key = stdscr.getch()

    stdscr.clear()

    if key == curses.KEY_UP and menu_idx > 0:
      menu_idx -= 1
    elif key == curses.KEY_DOWN and menu_idx < len(menu) - 1:
      menu_idx += 1
    elif key == curses.KEY_ENTER or key in [10, 13]:
      if menu[menu_idx] == "Exit":
        break
      elif menu[menu_idx] == "Play":
        play_gol(stdscr)

    print_menu(stdscr, menu_idx)

    stdscr.refresh()





 # h, w = stdscr.getmaxyx()

  # text = "Hello World"

  # x = w // 2 - len(text) // 2
  # y = h // 2

  # stdscr.attron(curses.color_pair(1))
  # stdscr.addstr(y, x, text)
  # stdscr.attroff(curses.color_pair(1))
  
  # stdscr.refresh()
  # time.sleep(3)


def main():
  os.environ.setdefault("ESCDELAY", "0")
  curses.wrapper(setup_gol)
  
  #test_gol()

if __name__ == "__main__":
  main()