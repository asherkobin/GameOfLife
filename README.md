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
- Bounds on EDIT - Fixed
- Menu Ordering after EDIT - Fixed
- EDIT curosr not big enough - Fixed
- Edge coditons on evolve - Fixed
- Crash on console window resize
- Fix Paste:
x = 459, y = 712, rule = B3/S23
417bo$415b2o$416b2o39$456bobo$456b2o$391bo65bo$391bobo$391b2o38$432bo$
431bo$431b3o$366bobo$366b2o$367bo38$408bo$406b2o$342bo64b2o$341bo$341b
3o39$382bo$382bobo$318bo63b2o$316b2o$317b2o39$357bobo$357b2o$292bo65bo
$292bobo$292b2o38$333bo$332bo$332b3o$267bobo$267b2o$268bo38$309bo$307b
2o$243bo64b2o$242bo$242b3o39$283bo$283bobo$219bo63b2o$217b2o$218b2o39$
258bobo$258b2o$193bo65bo$193bobo$193b2o38$234bo$233bo$233b3o$168bobo$
168b2o$169bo38$210bo$208b2o$144bo64b2o$143bo$143b3o39$184bo$184bobo$
120bo63b2o$118b2o$119b2o39$159bobo$159b2o$94bo65bo$94bobo$94b2o38$135b
o$134bo$134b3o$69bobo$69b2o$70bo38$111bo$109b2o$45bo64b2o$44bo$44b3o
39$85bo$85bobo$21bo63b2o$19b2o$20b2o5$14b2o$14b2o$16bo$14b3o$13bobo$
14b2o$13bo$13bo$11bo8$3o$3o$o2bo$b3o$b2o!

TODO:
- Make CLASSES ! - Done
- Count generations - Done
- Color particles based on age - Done
- Create background grid
- Edit TOGGLE - Done
- Text on Home Page - Done
- Matrix off-screen or wrap - Done
- Make menu dividers or Sub-menus
- Get average distrubution of cell age to better represent color gradients