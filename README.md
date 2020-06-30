# GameOfLife

GOL Rules:
      |   |
    --+---+--
      | C |
    --+---+--
      |   |

Scan array from top to bottom, starting at top-left (probably)

if C is alive:
  if neighbors == 2 or 3:
    C stays alive
  else
    C becomes dead
else if C is dead
  if neighbors == 3:
    C become alive

BUGS:
- Bounds on EDIT
- Menu Ordering after EDIT - Fixed
- EDIT curosr not big enough
- Generations does not reset
- Edge coditons on evolve

TODO:
- Make CLASSES !
- Count generations - Done
- Color particles based on age - Done
- Create background grid
- Edit TOGGLE
- Text on Home Page
- Matrix off-screen or wrap
- Make menu dividers or Sub-menus
- Get average distrubution of cell age to better represent color gradients