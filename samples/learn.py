import os
import curses
import time
from curses.textpad import rectangle

def start_game(stdscr):
  sh, sw = stdscr.getmaxyx()
  box = [[0, 0], [sh - 2, sw - 1]]
  cursor_pos = [5,5]

  rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
  stdscr.addstr(cursor_pos[0], cursor_pos[1], "*")

  stdscr.refresh()
  
  while True:
    
    key = stdscr.getch()
    
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

    stdscr.addstr(cursor_pos[0], cursor_pos[1], "*")
    
    stdscr.refresh()

menu = ["Play", "Exit"]

def print_menu(stdscr, selected_row_idx):
  stdscr.clear()
  h, w = stdscr.getmaxyx()

  for idx, item in enumerate(menu):
    x = w // 2 - len(item) // 2
    y = h // 2 - len(menu) // 2 + idx
    if idx == selected_row_idx:
      stdscr.attron(curses.color_pair(1))
      stdscr.addstr(y, x, item)
      stdscr.attroff(curses.color_pair(1))
    else:
      stdscr.addstr(y, x, item)

  stdscr.refresh()

def main(stdscr):
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
  
  current_row_idx = 0
  
  print_menu(stdscr, current_row_idx)

  while True:
    key = stdscr.getch()

    stdscr.clear()

    if key == curses.KEY_UP and current_row_idx > 0:
      current_row_idx -= 1
    elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
      current_row_idx += 1
    elif key == curses.KEY_ENTER or key in [10, 13]:
      if current_row_idx == len(menu) - 1:
        break
      elif menu[current_row_idx] == "Play":
        start_game(stdscr)

    print_menu(stdscr, current_row_idx)

    stdscr.refresh()

os.environ.setdefault("ESCDELAY", "0")
curses.wrapper(main)


 # h, w = stdscr.getmaxyx()

  # text = "Hello World"

  # x = w // 2 - len(text) // 2
  # y = h // 2

  # stdscr.attron(curses.color_pair(1))
  # stdscr.addstr(y, x, text)
  # stdscr.attroff(curses.color_pair(1))
  
  # stdscr.refresh()
  # time.sleep(3)
