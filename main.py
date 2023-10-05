import copy

import pyfiglet
import character
from ui import get_input
from ui import print_to_game_text
from ui import frame_main_loop
import game

# main method for the game
# this contains make character function and before function
# these are used to then allow player to generate and play games

break_line_str = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

def MakeCharacter():
    name = None
    hp = None
    dmg = None
    defense = None
    sped = None
    while name == None:
        temp = get_input("What name do you want for your character?")
        if type(temp) == str:
            name = temp
    while hp == None or dmg == None or defense == None or sped == None:
        temp = get_input("What stats do you want for your character? Health, damage, defense, speed. Write values in format of 4,7,2,3. Values must be from 1 to 10")
        temp_split = temp.split(',')
        if len(temp_split) == 4:
            is_valid = True
            for n in temp_split:
                if n.isdigit() == True:
                    if int(n) > 10 or int(n)< 1:
                        is_valid = False
                else:
                    is_valid = False
            if is_valid == True:
                hp = int(temp_split[0])
                dmg = int(temp_split[1])
                defense = int(temp_split[2])
                sped = int(temp_split[3])

    player = character.Character.Player(name=name, description=None, base_health=hp, damage=dmg, defence=defense, location=None, speed=sped)
    return player

def BeforeFunc():
    print_to_game_text(pyfiglet.figlet_format('TEXT ADVENTURE GAME GENERATOR', font="digital"))
    print_to_game_text(pyfiglet.figlet_format('CREATED BY LIAM POOLE', font="digital"))
    print_to_game_text(
        'Welcome to the game. This box is where the game details are shown. The box below displays current input options, and the bottom box is where you type. Press enter or the button to sumbit input.')
    print_to_game_text(break_line_str)
    player_char = MakeCharacter()
    while True:
        game3 = game.Game()
        #game3.PrintDetails()
        #game3.PrintHowToWin()
        while game3.is_lost == False and game3.win_bool == False:
            player_copy = copy.deepcopy(player_char)
            game3.play_game(player=player_copy)

BeforeFunc()
frame_main_loop()