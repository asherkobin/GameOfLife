import curses
from curses_colors import ColorPair
from curses_helpers import RleException, TextInputDialog

class EditMode():
  def __init__(self, curses_screen, display_area, pattern_helper):
    self.curses_screen = curses_screen
    self.display_area = display_area
    self.pattern_helper = pattern_helper
    self.cell_coordinate_list = []
    self.cursor_char = " "
    self.cell_char = "*"
    self.num_rows = self.display_area.get_num_rows()
    self.num_cols = self.display_area.get_num_cols()
    self.draw_mode = False
    self.save_dialog = TextInputDialog(curses_screen.stdscr, display_area)

  def print_edit_ui(self):
    # display screen border
    self.curses_screen.rectangle(
      self.display_area.get_start_row(),
      self.display_area.get_start_col(),
      self.display_area.get_num_rows(),
      self.display_area.get_num_cols() - 1) # leave room for status bar

    # status bar
    status_bar_text = f" Use ARROW keys to Move | Commands: SPACE to Toggle Cell | D to {'disable' if self.draw_mode else 'enable'} Draw Mode | ENTER to Save | ESC to Discard | P to Paste RLE Data | L to Load RLE File"
    self.curses_screen.print(status_bar_text, ColorPair.BLACK_ON_WHITE, self.display_area.get_num_rows(), 0)
    status_bar_padding = " " * ((self.display_area.get_num_cols() + 2) - len(status_bar_text) - 1)
    self.curses_screen.insert(status_bar_padding, ColorPair.BLACK_ON_WHITE, self.display_area.get_num_rows(), len(status_bar_text))

  def start(self, load_rle = False):
    self.cell_coordinate_list = []
    self.draw_mode = False
    
    new_pattern_name = "User Generated"
    cursor_row = self.num_rows // 2 
    cursor_col = self.num_cols // 2
    prev_cursor_row = None
    prev_cursor_col = None
    discard_work = False
    cursor_was_on_cell = False
    
    self.print_edit_ui()

    if load_rle:
      matrix = self.load_rle_data_into_editor("")
      for row_idx in range(len(matrix)):
        for col_idx in range(len(matrix[0])):
          if matrix[row_idx][col_idx] == 1:
            self.cell_coordinate_list.append((row_idx + 1, col_idx + 1))
            self.curses_screen.print(self.cell_char, ColorPair.WHITE_ON_BLACK, row_idx + 1, col_idx + 1)

    self.curses_screen.print(self.cursor_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)
    self.curses_screen.stdscr.refresh()
    
    while True:
      key = self.curses_screen.stdscr.getch()

      # reset for each key-press
      
      cursor_moved = False
      repaint_screen = False
      add_cell = False  
      remove_cell = False
      cursor_on_cell = False
      cursor_was_on_cell = False

      # save previous cursor location

      prev_cursor_col = cursor_col
      prev_cursor_row = cursor_row

      # cursor movement

      if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        if key == curses.KEY_UP:
          if cursor_row > 1:
            cursor_row -= 1
        elif key == curses.KEY_DOWN:
          if cursor_row < self.num_rows - 1:
            cursor_row += 1
        elif key == curses.KEY_LEFT:
          if cursor_col > 1:
            cursor_col -= 1
        elif key == curses.KEY_RIGHT:
          if cursor_col < self.num_cols - 1:
            cursor_col += 1
        
        cursor_moved = True

        cursor_on_cell = (cursor_row, cursor_col) in self.cell_coordinate_list
        cursor_was_on_cell = (prev_cursor_row, prev_cursor_col) in self.cell_coordinate_list

        if self.draw_mode and not cursor_on_cell:
          add_cell = True

      # toggle cell on/off
      
      elif key == curses.ascii.SP:
        cursor_on_cell = (cursor_row, cursor_col) in self.cell_coordinate_list
        
        if cursor_on_cell:
          remove_cell = True
        else:
          add_cell = True
      
      # save and quit

      elif key == curses.ascii.NL:
        break

      # discard and quit
      
      elif key == curses.ascii.ESC:
        discard_work = True
        break

      # toggle draw-mode

      elif key == ord('d'):
        self.draw_mode = not self.draw_mode
        if self.draw_mode:
          add_cell = True
        repaint_screen = True

      # paste pattern stored in clipboard
      
      elif key == ord('p'):
        paste_result = self.handle_paste()
        if paste_result != "OK":
          self.curses_screen.modal_popup(paste_result, self.display_area, 2)
          repaint_screen = True

      # save pattern to file

      elif key == ord('s'):
        self.handle_save()
        repaint_screen = True

      # load pattern from file

      elif key == ord('l'):
        self.handle_load()
        repaint_screen = True

      # process the status of the various flags

      if cursor_moved:
        if cursor_was_on_cell:
          # print the cell where the cursor previously was located
          self.curses_screen.print(self.cell_char, ColorPair.WHITE_ON_BLACK, prev_cursor_row, prev_cursor_col)
        else:
          # erase the cursor from previous location
          self.curses_screen.print(self.cursor_char, ColorPair.WHITE_ON_BLACK, prev_cursor_row, prev_cursor_col)
        
        if cursor_on_cell:
          # print cell at cursor location (inverted color)
          self.curses_screen.print(self.cell_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)
        else:
          # print cursor
          self.curses_screen.print(self.cursor_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)

      if add_cell:
        if cursor_on_cell:
          raise Exception("Unexpected")
        # print cell at cursor location (inverted color) and add it to the list
        self.curses_screen.print(self.cell_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)
        self.cell_coordinate_list.append((cursor_row ,cursor_col))

      elif remove_cell:
        if not cursor_on_cell:
          raise Exception("Unexpected")
        # print cursor and remove cell from the list
        self.curses_screen.print(self.cursor_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)
        self.cell_coordinate_list.remove((cursor_row ,cursor_col))
        cursor_on_cell = False        

      elif repaint_screen:
        self.curses_screen.stdscr.erase()
        self.print_edit_ui()
        for cell_coordinate in self.cell_coordinate_list:
          self.curses_screen.print(self.cell_char, ColorPair.WHITE_ON_BLACK, cell_coordinate[0], cell_coordinate[1])
        if (cursor_row, cursor_col) in self.cell_coordinate_list:
          self.curses_screen.print(self.cell_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)
        else:
          self.curses_screen.print(self.cursor_char, ColorPair.BLACK_ON_WHITE, cursor_row, cursor_col)

    if discard_work:
      new_pattern_name = None
    else:
      new_pattern_name = self.save_dialog.prompt("Enter Name for Pattern")
      
      if new_pattern_name is not None:
        new_pattern_matrix = self.pattern_helper.make_matrix_from_coords(self.cell_coordinate_list)
        if new_pattern_matrix:
          self.pattern_helper.add(new_pattern_name, new_pattern_matrix, True)
        else:
          new_pattern_name = None
    
    return new_pattern_name

  def handle_save(self):
    self.save_pattern(self.cell_coordinate_list)
    self.curses_screen.modal_popup("Saved to pattern.txt", self.display_area, 2)

  def handle_load(self):
    self.curses_screen.modal_popup("Load Not Implemented", self.display_area, 2)

  def handle_paste(self):
    from clipboard import get_clipboard_text
    rle_data = get_clipboard_text()
    
    matrix = None

    try:
      matrix = self.pattern_helper.rle_to_matrix(rle_data, self.display_area.max_row_idx - 1, self.display_area.max_col_idx - 1)
    except RleException as e:
      try:
        matrix = self.pattern_helper.conwaylife_to_matrix(rle_data, self.display_area.max_row_idx - 1, self.display_area.max_col_idx - 1)
        e.message = "CL_OK"
      except:
        e.message = "CL_FAIL"
      if e.message == "Invalid Format":
        return "Clipboard does not contain RLE data."
      elif e.message == "CL_FAIL":
        return "Clipboard does not contain Conway Life data."
    
    for row_idx in range(len(matrix)):
      for col_idx in range(len(matrix[0])):
        if matrix[row_idx][col_idx] == 1:
          self.cell_coordinate_list.append((row_idx + 1, col_idx + 1))
          self.curses_screen.print(self.cell_char, ColorPair.WHITE_ON_BLACK, row_idx + 1, col_idx + 1)

    return "OK"  

  def save_pattern(self, cell_coordinate_list):
    if len(cell_coordinate_list) > 0:
      pattern_matrix = self.pattern_helper.make_matrix_from_coords(cell_coordinate_list)
      
      num_rows = len(pattern_matrix)
      num_cols = len(pattern_matrix[0])
      
      with open("pattern.txt", "w") as pattern_file:
        pattern_file.writelines([f"({num_rows}, {num_cols})"])
        pattern_lines = [str(row) for row in pattern_matrix]
        pattern_file.writelines(pattern_lines)
    else:
      self.curses_screen.modal_popup("Nothing to save!", self.display_area, 2)

  def load_rle_data_into_editor(self, rle_data):
    s = "x = 5, y = 18, rule = B3/S23\n3bo$4bo$o3bo$b4o4$o$b2o$2bo$2bo$bo3$3bo$4bo$o3bo$b4o!"
    s = "x = 76, y = 59, rule = B3/S23\n12bo$13b2o$12b2o2$5bo$3bobo4bo$4b2o5b2o$10b2o2$3bo$bobo$2b2o2$73bobo$73b2o$74bo11$30bo$31b2o$30b2o24$63b3o$63bo$64bo2$34b2o$35b2o$34bo!"
    s = "x = 26, y = 12, rule = LifeHistory:C40,20\n15.A$2A12.A9.2A$A.A11.3A6.A.A$A24.A4$9.A.A$8.A$8.A$8.A2.A$8.3A!"
    s = "x = 49, y = 26, rule = B3/S23\n20b3o3b3o$19bo2bo3bo2bo$4o18bo3bo18b4o$o3bo17bo3bo17bo3bo$o8bo12bo3bo12bo8bo$bo2bo2b2o2bo25bo2b2o2bo2bo$6bo5bo7b3o3b3o7bo5bo$6bo5bo8bo5bo8bo5bo$6bo5bo8b7o8bo5bo$bo2bo2b2o2bo2b2o4bo7bo4b2o2bo2b2o2bo2bo$o8bo3b2o4b11o4b2o3bo8bo$o3bo9b2o17b2o9bo3bo$4o11b19o11b4o$16bobo11bobo$19b11o$19bo9bo$20b9o$24bo$20b3o3b3o$22bo3bo2$21b3ob3o$21b3ob3o$20bob2ob2obo$20b3o3b3o$21bo5bo!"

    pattern = self.pattern_helper.rle_to_matrix(rle_data, self.display_area.max_row_idx, self.display_area.max_col_idx)

    return pattern
