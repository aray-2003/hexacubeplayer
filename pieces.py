import random

"""
orange : pink (hook) 3
purple : blue (diamond) 6
yellow : yellow-green (single) 1
blue : orange (hook-180) 3/4
red : green (line) 2
green : yellow (semicircle) 5

"""

# List of possible pieces
pieces = {
  1: [ # yellowish-green
    []
  ],
  2: [ # green
    #line paths
    ['dr', 'dr', 'dr'], 
    ['dl','dl','dl'],
    ['l','l','l']
  ],
  3: [ # pink
    ['r','ur','dr'],
    ['ur','dr','r'],
    ['dr','ur','r'],
    ['r','dr','ur'],
    ['dr','dr','l'],
    ['dl','dl','r'],
    ['r','dl','dl'],
    ['r','dl','dr']
  ],
  4: [ # orange
    ['dr','ur','ur'],
    ['dr','dr','ur'],
    ['dr','l','dl'],
    ['ur','dr','dr']
  ],
  5: [ # yellow
    ['l','dl','dr'],
    ['ur','r','dr'],
    ['r','dr','dl'],
    ['dr','dl','l'],
    ['dl','l','ul'],
    ['l','ul','ur']
  ],
  6: [ # blue
    ['r','dr','l'],
    ['r','dl','l'],
    ['dl','r','dl']
  ]
}

class Piece:
  def __init__(self, path, color):
    self.path = path
    self.color = color


# Generate easier to use pool
pool = []
poolCollapsed = []

for color in pieces:
  for path in pieces[color]:
    pool.append(Piece(path, color))
    if (color != 1):
      poolCollapsed.append(Piece(path, color))


# Gets all of the pieces
def all_pieces():
  global poolCollapsed
  return poolCollapsed

# Generates a new piece (randomly)
def new_piece():
  global pool
  return random.choice(pool)

