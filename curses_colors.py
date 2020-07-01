import curses

class ColorPair():
  WHITE_ON_BLACK      =   1
  GREEN_ON_BLACK      =   2
  BLUE_ON_BLACK       =   3
  YELLOW_ON_BLACK     =   4
  RED_ON_BLACK        =   5
  MAGENTA_ON_BLACK    =   6
  CYAN_ON_BLACK       =   7
  
  BLACK_ON_WHITE      =  10
  WHITE_ON_BLUE       =  11
  
  GRADIENT_1_ON_BLACK = 100
  GRADIENT_2_ON_BLACK = 101
  GRADIENT_3_ON_BLACK = 102
  GRADIENT_4_ON_BLACK = 103
  GRADIENT_5_ON_BLACK = 104

class CustomColors():
  GRADIENT_1 = 100
  GRADIENT_2 = 101
  GRADIENT_3 = 102
  GRADIENT_4 = 103
  GRADIENT_5 = 104

class CursesColorHelper:
  def __init__(self):
    pass

  def init_color_pairs(self):
    gradient_1 = "rgb(0, 255, 0)"
    curses.init_color(CustomColors.GRADIENT_1, *self.rgb_to_curses(gradient_1))
    
    gradient_2 = "rgb(0, 225, 173)"
    curses.init_color(CustomColors.GRADIENT_2, *self.rgb_to_curses(gradient_2))
    
    gradient_3 = "rgb(0, 186, 255)"
    curses.init_color(CustomColors.GRADIENT_3, *self.rgb_to_curses(gradient_3))
    
    gradient_4 = "rgb(0, 135, 255)"
    curses.init_color(CustomColors.GRADIENT_4, *self.rgb_to_curses(gradient_4))
    
    gradient_5 = "rgb(0, 0, 255)"
    curses.init_color(CustomColors.GRADIENT_5, *self.rgb_to_curses(gradient_5))

    curses.init_pair(ColorPair.GRADIENT_1_ON_BLACK, CustomColors.GRADIENT_1, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.GRADIENT_2_ON_BLACK, CustomColors.GRADIENT_2, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.GRADIENT_3_ON_BLACK, CustomColors.GRADIENT_3, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.GRADIENT_4_ON_BLACK, CustomColors.GRADIENT_4, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.GRADIENT_5_ON_BLACK, CustomColors.GRADIENT_5, curses.COLOR_BLACK)

    curses.init_pair(ColorPair.WHITE_ON_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.BLACK_ON_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(ColorPair.GREEN_ON_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(ColorPair.BLUE_ON_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.YELLOW_ON_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.RED_ON_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.MAGENTA_ON_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.CYAN_ON_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)

  def color_byte_to_curses_int(self, color_byte):
    scale = 1000 / 255
    curses_int = color_byte * scale
    curses_int = round(curses_int)
    return curses_int

  def rgb_to_curses(self, rgb_string):
    # "rgb(0, 225, 173)" => [0, 255, 173] => [0, 1000, 486]
    curses_colors = []
    rgb_string = rgb_string[4:-1]
    rgb_colors = rgb_string.split(",")

    for color_byte in rgb_colors:
      curses_colors.append(self.color_byte_to_curses_int(int(color_byte)))

    return curses_colors