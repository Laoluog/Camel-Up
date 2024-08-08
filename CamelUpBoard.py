import random
import math
from itertools import permutations, product
import copy
from colorama import Fore, Back, Style, init

from CamelUpPlayer import CamelUpPlayer

class CamelUpBoard:
    def cartesian_product(self, lis1, lis2):
        return list(product(lis1, lis2))
    def __init__(self, camel_styles: list[str]):
        self.TRACK_POSITIONS = 16
        self.DICE_VALUES = [1,2,3]
        self.BETTING_TICKET_VALUES = [5, 3, 2, 2]
        
        self.camel_styles = camel_styles
        self.camel_colors= camel_styles.keys()
        self.track = self.starting_camel_positions()
        self.pyramid = set(self.camel_colors)
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = [] #preserves order

    def starting_camel_positions(self)->list[list[str]]:
        '''Places camels on the board at the beginning of the game
        '''
        track = [[] for i in range(self.TRACK_POSITIONS)]
        dictcam = {}
        for x in list(self.camel_colors):
            dictcam[x] = random.randint(0, 2)
        for key in dictcam.keys():
            track[dictcam.get(key)].append(key)
        return track
    
    def print(self, players: list[CamelUpPlayer]):
        '''Prints the current state of the Camel Up board, including:
        '''
        board_string = "\n"
         #Ticket Tents
        ticket_string = "Ticket Tents: "
        for ticket_color in self.ticket_tents:
            if len(self.ticket_tents[ticket_color]) > 0:
                next_ticket_value = str(self.ticket_tents[ticket_color][0])
            else:
                next_ticket_value = 'X'
            ticket_string+=self.camel_styles[ticket_color]+next_ticket_value+Style.RESET_ALL+" "
        board_string += ticket_string +"\t\t"

        #Dice Tents
        dice_string = "Dice Tents: "
        for die in self.dice_tents:
            dice_string+=self.camel_styles[die[0]]+str(die[1])+Style.RESET_ALL+" "

        for i in range (5-len(self.dice_tents)):
            dice_string+=Back.WHITE+" "+Style.RESET_ALL+" "
        
        #Camels and Race Track
        board_string += dice_string +"\n"
        for row in range(4, -1, -1):
            row_str = [" "]*16
            for i in range(len(self.track)):
                for camel_place, camel in enumerate(self.track[i]):
                    if camel_place == row:
                        row_str[i]=self.camel_styles[camel]+ camel +  Style.RESET_ALL 
            board_string += "🌴 "+str("   ".join(row_str))+" |🏁\n"
        board_string += "   "+"".join([str(i)+"   " for i in range(1, 10)])
        board_string += "".join([str(i)+"  " for i in range(10, 17)])+"\n"

        #Player Info
        player_string=""
        for player in players:
            player_string+=f"{player.name} has {player.money} coins."
            if len(player.bets)>0:
                bets_string = " ".join([self.camel_styles[bet[0]]+str(bet[1])+Style.RESET_ALL for bet in player.bets])
                player_string += f" Bets: {bets_string}"  
            player_string+="\t\t" 
        
        board_string+=player_string
        print(board_string+"\n")

    def reset_tents(self):
        '''Rests dice tents and ticket tents at the end of a leg
        '''
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = []

    def place_bet(self, color:str)->tuple[str, int]:
        '''Manages the board perspective when a player places a bet:
        '''
        tickets_left = self.ticket_tents[color]
        ticket = ()
        if len(tickets_left)>0:
            ticket =(color, tickets_left[0])
            self.ticket_tents[color] = tickets_left[1:]
        return ticket

    def move_camel(self, die:tuple[str, int], verbose=False):
        '''Updates the track according to the die color and value
        '''
        if verbose: ("Current track state:", self.track)
        ### BEGIN SOLUTION
        camellist = self.track.copy()
        newnumber = 0
        camelsmove = []
        storex = 0
        storez = 0
        for x in range(len(camellist)):
            for z in range(len(camellist[x])):
                if die[0] == camellist[x][z]:
                    newnumber = die[1] + x
                    camelsmove = camellist[x][z:len(camellist[x])]
                    storex = x
                    storez = z
        for i in camelsmove:
            camellist[newnumber].append(i)
        camellist[storex] = camellist[storex][0:storez]
        self.track = camellist
        ### END SOLUTION
        if verbose: print("Updated track state:", self.track)
        return self.track
    
    def shake_pyramid(self)->tuple[str, int]:
        '''Manages all the steps (from the board persepctive) involved with shaking the pyramid, 
           which includes:
                - selecting a random color and dice value from the dice colors in the pyramid
                - removing the rolled dice from the pyramid
                - placing the rolled dice in the dice tents
        '''
        rolled_die=("", 0)
        ### BEGIN SOLUTION
        pyramid = self.pyramid.copy()
        if not pyramid:
            return ("", 0)
        randshake = random.randint(1, 3)
        randcolor = random.choice(list(pyramid))
        pyramid.remove(randcolor)
        self.pyramid = pyramid
        ### END SOLUTION
        self.dice_tents.append((randcolor, randshake))
        return (randcolor, randshake)

    def is_leg_finished(self)->bool:
        '''Determines whether the leg of a race is finished
        '''
        ### BEGIN SOLUTION
        if not self.pyramid:
            return True
        return False
        ### END SOLUTION

    def get_rankings(self):
        '''Determines first and second place camels on the track
        '''
        rankings = ("", "")
        ### BEGIN SOLUTION
        finallist = []
        checkerlist = self.track[::-1]
        while len(finallist) < 2:
            for x in checkerlist:
                if x:
                    gob = x[::-1]
                    for z in gob:
                        finallist.append(z)
        ### END SOLUTION
        return (str(finallist[0]), str(finallist[1]))

    def get_all_dice_roll_sequences(self)-> set:
        '''
            Constructs a set of all possible roll sequences for the dice currently in the pyramid
            Note: Use itertools product function
        ''' 
        roll_space = set()
        ### BEGIN SOLUTION
        letterseqs = self.pyramid.copy()
        numbseqs = [1, 2, 3]
        numbseqs = product(numbseqs, repeat=len(letterseqs))
        letterseqs = permutations(letterseqs)

        roll_space = set(product(letterseqs, numbseqs))
        newrs = []
        for i in roll_space:
            if len(i[0]) == 0:
                newrs = {(())}
            if len(i[0]) == 1:
                newrs.append((i[0][0], i[1][0]))
            if len(i[0]) == 2:
                newrs.append(((i[0][0], i[1][0]), (i[0][1], i[1][1])))
            if len(i[0]) == 3:
                newrs.append(((i[0][0], i[1][0]), (i[0][1], i[1][1]), (i[0][2], i[1][2])))
            if len(i[0]) == 4:
                newrs.append(((i[0][0], i[1][0]), (i[0][1], i[1][1]), (i[0][2], i[1][2]), (i[0][3], i[1][3])))
            if len(i[0]) == 5:
                newrs.append(((i[0][0], i[1][0]), (i[0][1], i[1][1]), (i[0][2], i[1][2]), (i[0][3], i[1][3]), (i[0][4], i[1][4])))
        ### END SOLUTION
        return set(newrs)
    
    def run_enumerative_leg_analysis(self)->dict[str, tuple[float, float]]:
        '''Conducts an enumerative analysis of the probability that each camel will win either 1st or 
           2nd place in this leg of the race. The enumerative analysis counts 1st/2nd place finishes 
           via calculating the entire state space tree
        '''
        win_percents={color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION
        finaldictwin = {}
        finaldicttwo = {}
        actdict = {}
        dicelist = self.get_all_dice_roll_sequences()

        winlist = []
        for i in dicelist:
            practicet = copy.deepcopy(self.track)
            for x in i:
                self.move_camel(x)
            winlist.append(self.get_rankings())
            self.track = practicet

        z = len(winlist)
        for x in winlist:
            if x[0] not in finaldictwin:
                finaldictwin[x[0]] = 1
            else:
                finaldictwin[x[0]] += 1
            if x[1] not in finaldicttwo:
                finaldicttwo[x[1]] = 1
            else:
                finaldicttwo[x[1]] += 1
        for a in self.camel_colors:
            if a in finaldictwin.keys() and a in finaldicttwo.keys():
                actdict[a] = ((((finaldictwin.get(a))/z)), ((finaldicttwo.get(a))/z))
            elif a in finaldictwin.keys():
                actdict[a] = (((finaldictwin.get(a))/z), 0.0)
            elif a in finaldicttwo.keys():
                actdict[a] = (0.0, ((finaldicttwo.get(a))/z))
            else: 
                actdict[a] = (0.0, 0.0)
        ### END SOLUTION
        return actdict

    def run_experimental_leg_analysis(self, trials:int)->dict[str, tuple[float, float]]:
        '''Conducts an experimental analysis (ie. a random simulation) of the probability that each camel
            will win either 1st or 2nd place in this leg of the race. The experimenta analysis counts 
            1st/2nd place finishes bycounting outcomes from randomly shaking the pyramid over a given 
            number of trials.
        '''
        win_percents={color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION
        pract = copy.deepcopy(self.track)
        keep = copy.deepcopy(self.dice_tents)
        pyr = self.pyramid
        winlist = []
        finaldictwin = {}
        finaldicttwo = {}
        actdict = {}
        for i in range(trials):
            pract = copy.deepcopy(self.track)
            keep = copy.deepcopy(self.dice_tents)
            while len(self.pyramid) > 0:
                shake = self.shake_pyramid()
                self.move_camel(shake)
            winlist.append(self.get_rankings())
            self.pyramid = pyr
            self.track = pract
            self.dice_tents = keep
        for x in winlist:
            if x[0] not in finaldictwin:
                finaldictwin[x[0]] = 1
            else:
                finaldictwin[x[0]] += 1
            if x[1] not in finaldicttwo:
                finaldicttwo[x[1]] = 1
            else:
                finaldicttwo[x[1]] += 1
        for a in self.camel_colors:
            if a in finaldictwin.keys() and a in finaldicttwo.keys():
                actdict[a] = ((((finaldictwin.get(a))/trials)), ((finaldicttwo.get(a))/trials))
            elif a in finaldictwin.keys():
                actdict[a] = (((finaldictwin.get(a))/trials), 0.0)
            elif a in finaldicttwo.keys():
                actdict[a] = (0.0, ((finaldicttwo.get(a))/trials))
            else: 
                actdict[a] = (0.0, 0.0)

        self.pyramid = pyr
        self.track = pract
        self.dice_tents = keep
        ### END SOLUTION
        return actdict
   
if __name__ == "__main__":
    camel_styles= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    board = CamelUpBoard(camel_styles)
    p1 = CamelUpPlayer("p1")
    p2 = CamelUpPlayer("p2")
    board.print([p1, p2])
    die = ('b', 1)
    board.move_camel(die)
    #Roll 3 random dice
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    board.print([p1, p2])
    #Probabilites
    all_possible_dice_sequences= board.get_all_dice_roll_sequences()
    print(f"{len(all_possible_dice_sequences)} possible dice sequences for {len(board.pyramid)} dice in the pyramid:") 
    print("Enumerative Probabilities:", board.run_enumerative_leg_analysis())
    print("Experimental Probabilities:", board.run_experimental_leg_analysis(300))
