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

