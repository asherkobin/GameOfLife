import curses
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

def start_gol(stdscr):
  height, width = stdscr.getmaxyx()
  cell_matrix = CellMatrix(height, width)
  k = 0
  cursor_x = 0
  cursor_y = 0

  # Clear and refresh the screen for a blank canvas
  stdscr.clear()
  stdscr.refresh()

  # Start colors in curses
  curses.start_color()
  curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

  # Loop where k is the last character pressed
  while (k != ord('q')):

      # Initialization
      stdscr.clear()
      height, width = stdscr.getmaxyx()

      if k == curses.KEY_DOWN:
          cursor_y = cursor_y + 1
      elif k == curses.KEY_UP:
          cursor_y = cursor_y - 1
      elif k == curses.KEY_RIGHT:
          cursor_x = cursor_x + 1
      elif k == curses.KEY_LEFT:
          cursor_x = cursor_x - 1

      cursor_x = max(0, cursor_x)
      cursor_x = min(width-1, cursor_x)

      cursor_y = max(0, cursor_y)
      cursor_y = min(height-1, cursor_y)

      # Declaration of strings
      title = "The Game of Life"[:width-1]
      subtitle = "Written by Asher Kobin"[:width-1]
      keystr = "Last key pressed: {}".format(k)[:width-1]
      statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
      if k == 0:
          keystr = "No key press detected..."[:width-1]

      # Centering calculations
      start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
      start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
      start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
      start_y = int((height // 2) - 2)

      # Rendering some text
      whstr = "Width: {}, Height: {}".format(width, height)
      stdscr.addstr(0, 0, whstr, curses.color_pair(1))

      # Render status bar
      stdscr.attron(curses.color_pair(3))
      stdscr.addstr(height-1, 0, statusbarstr)
      stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
      stdscr.attroff(curses.color_pair(3))

      # Turning on attributes for title
      stdscr.attron(curses.color_pair(2))
      stdscr.attron(curses.A_BOLD)

      # Rendering title
      stdscr.addstr(start_y, start_x_title, title)

      # Turning off attributes for title
      stdscr.attroff(curses.color_pair(2))
      stdscr.attroff(curses.A_BOLD)

      # Print rest of text
      stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
      stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
      stdscr.addstr(start_y + 5, start_x_keystr, keystr)
      stdscr.move(cursor_y, cursor_x)

      # Refresh the screen
      stdscr.refresh()

      # Wait for next input
      k = stdscr.getch()

def main():
    curses.wrapper(start_gol)

if __name__ == "__main__":
    main()