from python_imagesearch.imagesearch import imagesearcharea

from pieces import Piece, pieces, all_pieces
from board import Board
from time import sleep


import os
import re
import os
import keyboard
import mouse
import sys, os



application_path = os.path.dirname(sys.executable)

units = {
    'dl':[-33,59],
    'ul':[-33,-59],
    'dr':[33,59],
    'r':[66,0],
    'l':[-66,0],
    'd':[0,115]
}

begin = [827,177]

roll = [807,1015]

piece1_region = {
    0: [666, 730], #top-left
    1: [850, 930] #bot-right
}
piece2_region = {
    0: [866, 730], #top-left
    1: [1050, 930] #bot-right
}
piece3_region = {
    0: [1066, 730], #top-left
    1: [1250, 930] #bot-right
}

score_weighting = 3 #3
space_weighting = 3 #3
move_weighting = 1 #1
possible_move_weighting = 180 #180

plr = None
target = 0
mouse_delay = 0.3
move_delay = 1
can_reroll = True

class Player:
    def __init__(self):
        self.pieces = [get_piece(1), get_piece(2), get_piece(3)]
        self.moves = []
        self.done = False
        self.finished_board = None
        self.current_board = Board([])
    
    def append_move(self, board, move):
        b = board.duplicate()
        b.make_move(move)
        return b
    

    def weight(self, b, move, pieces, depth, max_depth, alpha, beta):
        board = self.append_move(b, move)
        next_moves = board.get_moves(pieces)
        possible_moves = board.get_moves(all_pieces())
        w = board.score_last * score_weighting + (board.spaces / 61.0) * space_weighting + len(next_moves) * move_weighting + len(possible_moves) * possible_move_weighting
        if depth + 1 < max_depth:
            for move in next_moves:
                p = pieces[:]
                p.remove(move.piece)

                w += -self.weight(board, move, p, depth + 1, max_depth, -beta, -alpha)
                alpha = max(alpha, w)
                if alpha >= beta:
                    break
        return w   
    
    def get_worst_move(self, depth):
        board = self.current_board.duplicate()
        valid_moves = board.get_moves(self.pieces)
        best_move = valid_moves[0]

        return best_move, 100000
    def get_best_move(self, depth):
        board = self.current_board.duplicate()
        valid_moves = board.get_moves(self.pieces)

        best_weight = 0
        best_move = None

        for d in range(1, depth+1):
            for move in valid_moves:
                w = self.weight(board, move, self.pieces, 0, d, float('-inf'), float('inf'))
                if w > best_weight:
                    best_weight = w
                    best_move = move

        return best_move, best_weight
    
    def status(self):
        self.current_board.print_self()

    def score(self):
        return self.current_board.score
    
    def reroll(self):
        global mouse_delay, move_delay, can_reroll
        p = [self.pieces[0].path,self.pieces[1].path,self.pieces[2].path]
        mouse.move(roll[0],roll[1], mouse_delay)
        mouse.click()
        sleep(move_delay)
        self.pieces = [get_piece(1), get_piece(2), get_piece(3)]
        q = [self.pieces[0].path,self.pieces[1].path,self.pieces[2].path]
        can_reroll = not (p == q)

  



    def play(self):
        global piece1_region,piece2_region,piece3_region, target, move_delay, can_reroll

        if self.score() <= target:
            move, weight = self.get_best_move(1)
        else:
            move, weight = self.get_worst_move(1)

        if weight > 10000 or not can_reroll:
            if (move == None):
                self.done = True
                exit()
            else:
                self.moves.append(move)
                self.current_board.make_move(move)
                print(move.loc)
                
                match(self.pieces.index(move.piece) + 1):
                    case(1):
                        place(piece1_region, move.loc)
                    case(2):
                        place(piece2_region, move.loc)
                    case(3):
                        place(piece3_region, move.loc)
                
                self.status()
                print()
                sleep(move_delay)
                piece = get_piece(self.pieces.index(move.piece) + 1)
                self.pieces[self.pieces.index(move.piece)] = piece 
                can_reroll = True
        else:
            if self.score() <= target:
                self.reroll()
            self.play()
        

    def finish(self):
        while not self.done:
            self.play()
        self.finished_board = Board(self.moves)

def get_piece(p: int) -> Piece:
    if piece1_region != None and piece2_region != None and piece3_region != None:
        match(p):
            case 1:
                color, path, _ =  getPiece(piece1_region)
                return Piece(pieces[color][path], color)
            case 2:
                color, path, _ =  getPiece(piece2_region)
                return Piece(pieces[color][path], color)
            case 3:
                color, path, _ =  getPiece(piece3_region)
                return Piece(pieces[color][path], color)


def getPiece(region: map):
    for img in os.listdir('./imgs/'):
        piece_found = imagesearcharea(
            './imgs/'+str(img),
            region[0][0],region[0][1],region[1][0],region[1][1],
            .8)
        if piece_found[0] != -1:
            return extract(str(img))
        
        
def midpoint(region: map):
    x1, y1 = region[0]
    x2, y2 = region[1]

    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2

    return midpoint_x, midpoint_y


def findLocation(loc: list, origin: list) -> list:
    grid_origin_x = origin[0]
    grid_origin_y = origin[1]

    grid_spacing_x = 66  
    grid_spacing_y = 59

    height = loc[0]
    position = loc[1] 

    x = grid_origin_x + (position * grid_spacing_x)
    
    if height <= 4:
        x -= height * (grid_spacing_x // 2)
    else:
        x -= (8-height) * grid_spacing_x // 2
       
    y = grid_origin_y + (height * grid_spacing_y)

    return x,y
        
def extract(filename: str):
    # Remove the file extension
    filename = filename.rsplit('.', 1)[0]

    # Extract the numbers using regular expressions
    numbers = re.findall(r'\d+', filename)

    # Extract the two sets of letters using string splitting
    letters = filename.split('-')[1:-1]

    # Extract the color and path from the numbers and letters
    color = int(numbers[0])
    path = int(numbers[1])

    return color, path, letters



def place(piece: map, loc: list) -> None:
    global begin, units, mouse_delay
    if begin:
        color, path, directon = getPiece(piece)
        point = midpoint(piece)
        loc = list(findLocation(loc, begin))

        for s in directon:
            loc[0] += units[str(s)][0]
            loc[1] += units[str(s)][1]
        
        loc[1] += units['d'][1]
        
        mouse.drag(point[0],point[1],loc[0],loc[1],True,mouse_delay)
    

def start() -> None:
    global plr

    if not plr:
        plr = Player()
    plr.finish()
    



if __name__ == '__main__':
    
    target = int(input("What score do you want? ")) + 100
    choice = int(input("How fast do you want to go? (1: Natural, 2: Max-speed, 3: Custom) "))
    if choice == 2:
        mouse_delay = 0.02
        move_delay = 0.7
    elif choice == 3:
        mouse_delay = float(input("Delay for mouse movement: "))
        mouse_delay = float(input("Delay between moves: "))

    print("Ready! Go into game and press \"e\" to begin.")
    keyboard.wait('e')
    start()














