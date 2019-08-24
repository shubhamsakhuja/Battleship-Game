# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:45:52 2019

@author: ASUS
"""
#**************WELCOME TO BATTLESHIP GAME****************
# This game will generate a single ship.
# Battlefield size is input by the user and will be created accordingly.
# Coordinates of the battlefield starts from (0,0) so there are chances your ship will start from (0,0).
# Ship is always of size 5.
# Ship cannot go out of battlefield so guess values accordingly.
# Please follow instructions what code is asking to input, for example: a number or a string like yes/no.
# This code has limited type checks and restrictions on user input assumping user is smart enought to understand what has been asked.
# After 5 misses, a message will prompt after every miss that you want to give up ?
# Updates possible are - Add 2 ships, give up prompt windows after every 5 misses.
# Updates possible are - Create a bot that will destroy your ship automatically after limited number of misses.
# Enjoy gaming folks!

from random import randint
import sys

#set up the player battlefield 
hit_battlefield = []
global field_size

#promputing user to provide input to start the game
player_input = input("Do you want to start a new game of Battleship? Type n/no/y/yes - ").lower()
if player_input not in ['yes', 'y', 'no', 'n']:
    print("Enter a valid value")
else:
    if player_input == 'yes' or player_input == 'y':
            while True:
                try:
                    field_size = int(input(
                        "Enter a number\n\nThis will determine how big will be the battlefield (Always greater than 5 ie.5 rows, 5 columns etc.): "))
                    if (field_size) < 5:
                        raise ValueError()
                except ValueError:
                    print("You did not enter the number equal or greater than 5!")
                    continue
                else:
                    break
                
    elif player_input == 'no' or player_input == 'n':
            print("Thank you for playing!")
            input("Press the 'Enter' key to exit the game.")
            sys.exit(0)

#creating battlefield
for x in range(0,field_size):
    hit_battlefield.append(["0"] * field_size)

#prints a new screen with the title and the current player's hit board.
def new_screen():
    print("Welcome to the Battleship Game !")
    print_battlefield(hit_battlefield)
    
def print_battlefield(battlefield):
    for row in battlefield:
        print(" ".join(row))
        
    print("\n")

#Creates a random point (x,y position) and returns it as a tuple.
def random_position(battlefield, xBound, yBound):
    xCoordinate = randint(1, (len(battlefield) ))
    yCoordinate = randint(1, (len(battlefield[0]) ))
    return (xCoordinate, yCoordinate)
    #uncomment to know the random coordinates generated for debugging purpose only
    #print(xCoordinate, yCoordinate)

#Our ship is a object that is passed a name and a size.
class Ship:
    #Constructor function that sets up our local variables and makes positions our ship.
    def __init__(self, size):
        self.size = size
        self.direction = randint(0,1)
        self.positions = []
        self.damage = 0
        self.count_hit = 0
        self.count_miss = 0
        
        #The following code finds a starting position and tries to position the ship based on that starting position, if one of the locations we try to place our ship is occupied, we find a new starting point.
        empty_space = False
        row = randint(1,len(hit_battlefield)+1)
        diffr = (len(hit_battlefield) - 5)
        if row > diffr:
            row = diffr
        else:
            row = row
            
        col = randint(1,len(hit_battlefield)+1)
        diffc = (len(hit_battlefield) - 5)
        if col > diffc:
            col = diffc
        else:
            col = row
        
        
        #print(size)
        #This loop continues looking for an open space until one is found.
        while not empty_space:
            empty_space = True
        #The ship is vertical and our locations are empty, so we place the ship.
            if self.direction == 0:
                for i in range(size):
                    self.positions.append([row + i, col])
                
        #The ship is horizontal and our locations are empty, so we place the ship.
            elif self.direction == 1:
                for i in range(size):
                    self.positions.append([row, col + i])
                
#Set up our ships list and add our ship objects
ships = []
ships.append(Ship(5))

#Debugging script so we can see the positions of the ship
#for ship in ships:
#   print("positions:")
#   for position in ship.positions:
#      print(str(position[0]) + "," + str(position[1]))

#The main game loop continues until the ships have all been destroyed (when a ship is destroyed it is removed from the ships list).
def main():
    #print(field_size)
    while (len(ships) is not 0):
        new_screen()
        print("WARNING! Coordinates in a battlefield starts from (0,0) so guess positions accordingly")
        guess_row = int(input("Enter Row value within the battlefield range:")) 
        guess_col = int(input("Enter Column value within the battlefield range:"))
        
        #Check if the guess was off the board.
        if (guess_row < 0 or guess_row > (len(hit_battlefield) - 1) or guess_row == "") or (guess_col < 0 or guess_col > (len(hit_battlefield[0]) - 1) or guess_col == ""):
            print("You guess is outside of the battlefield, try again!")
            
        #Check if the player has fired at that location already.
        elif(hit_battlefield[guess_row][guess_col] != "0"):
            print("You're trying to shoot at the same spot twice are you? Fool! Try again")
            
        #Check the position to see if a ship is there and a hit is registered.
        else:
            hit = False
            for ship in ships:
                for position in ship.positions:
                    #Check if a ship position is equal to the guessed position.
                    if guess_row == position[0] and guess_col == position[1]:
                        hit = True
                        ship.damage += 1
                        #Check if the ship is destroyed.
                        if ship.damage == ship.size:
                            print("Phew! You damaged the ship completely")
                            #Loop through the ship positions and set them to D for destroyed.
                            for section in ship.positions:
                                hit_battlefield[section[0]][section[1]] = "D"
                            #Remove the ship from the array.
                            ships.remove(ship)
                        #Otherwise the ship has been hit, mark it with an H.
                        else:
                            print("You hit the ship, bravo!")
                            hit_battlefield[guess_row][guess_col] = "H"
                            ship.count_hit +=1
                        break
                #Break out of the outer loop if a hit was registered.
                if hit == True:
                    break
            #If no hit was registered after the outer for loop ends, the guess was a miss.
            if hit == False:
                print("You missed the target!")
                hit_battlefield[guess_row][guess_col] = "X"
                ship.count_miss +=1
                
                #Prompting user to give up when count of misses are greater than 5
                if ship.count_miss > 5:
                    continue_game = input("It's been a while.. Do you want to give up? Type n/no/y/yes - ").lower()
                    if continue_game in ['yes', 'y']:
                        print("Thank you for playing!")
                        input("Press the 'Enter' key to exit the game.")
                        sys.exit(0)
                    elif continue_game in['no','n']:
                        print("Next turn")
                
    print("You've sunk the ship! You won :)")
                        
    print("Your hit score is:",ship.count_hit)
    print("Your miss score is:",ship.count_miss)
    print_battlefield(hit_battlefield)
    

    
#Runs the main game loop
if __name__ == "__main__":
    main()