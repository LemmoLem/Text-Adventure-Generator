import item
import textwrap
import location
import math
import character
import ui

line_length = 1000
break_line_str = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# this file contains how players and characters interact
# interactions are functions rather than classes, so they just have to be called rather than made
class Choice:
    # choice needs to be overhauled. inventory and input checking is fine.
    # should print description of current location. and fighting and other event chains will be in their own part


    def __init__(self, player, game):
        self.player = player
        self.game = game


    # moves player
    def move_player(self, next_location):
        if next_location.requirement == None:
            self.player.location = next_location
        else:
            if self.player.check_for_marker(next_location.requirement) == True:
                self.player.location = next_location
                ui.print_to_game_text("You enter", next_location.name, "by utilising your prior gained knowledge.")
            else:
                ui.print_to_game_text("You fail to enter " + next_location.name)
        if self.player.location == self.game.goal_loc_get_to:
            self.game.win()


    # for fleeing from a fight
    def run(self, next_location):
        has_moved = False
        if next_location.requirement == None:
            self.player.location = next_location
            has_moved = True
        else:
            if self.player.check_for_marker(next_location.requirement) == True:
                self.player.location = next_location
                ui.print_to_game_text("You enter", next_location.name, "by utilising your prior gained knowledge.")
                has_moved = True
            else:
                has_moved = False
        if self.player.location == self.game.goal_loc_get_to:
            self.game.win()
        return has_moved

    # to take in and handle user input and perform actions
    def parse_input(self, options, options_string, info_text):
        #printToGameText(textwrap.fill(optionsString + " i: inventory", lineLength))
        ui.print_to_game_text(break_line_str)
        ui.print_to_game_text(info_text)
        choice_made = None
        while choice_made == None and self.game.win_bool == False:
            player_choice = ui.get_input(textwrap.fill(options_string + " i: inventory", line_length))
            player_choice = player_choice.lower()
            for x in options:
                # so if x is a string should check against
                if isinstance(x,str):
                    if x.lower() == player_choice:
                        ui.print_to_game_text("You chose " + x)
                        choice_made = x
                else:
                    if x.name.lower() == player_choice:
                        ui.print_to_game_text("You chose " + x.name)
                        choice_made = x
                    # then tries to work out whether its successful or not
                    # option class will have values for whether success or not
            try:
                num_choice = int(player_choice)
                if num_choice <= len(options) and num_choice > 0:
                    choice_made = options[num_choice - 1]
            except ValueError:
                skip_this = 1
                skip_this += 1
                # print("val error")

            # if player chose to use item in their inventory
            # they have to exit inventory
            # once they choose an item they have to choose something to do with it
            if player_choice == "i" or player_choice == "inventory":
                #printToGameText("These are your inventory options?")
                ui.print_to_game_text(break_line_str)
                choice_made = False
                exit_choice = False
                while exit_choice == False and self.game.win_bool == False:
                    inv_str = ""
                    if str(self.player.inventory) == "":
                        #printToGameText("Your inventory is empty.")
                        #printToGameText("e: exit")
                        inv_str = "Your inventory is empty. e: exit"
                    else:
                        #printToGameText(str(self.player.inventory) + " e: exit")
                        inv_str = str(self.player.inventory) + " e: exit"

                    inv_choice = ui.get_input(inv_str)
                    inv_choice = inv_choice.lower()
                    inv_choice_item = None
                    for y in self.player.inventory.getItems():
                        if y.name.lower() == inv_choice.lower():
                            inv_choice_item = y
                    try:
                        inv_choice = int(inv_choice)
                        if inv_choice <= len(self.player.inventory.getItems()) and inv_choice > 0:
                            inv_choice_item = self.player.inventory.getItems()[inv_choice - 1]
                    except ValueError:
                        skip_this = 1
                        # print("val error")

                    # if the item isnt none then players need to use it or exit
                    # have a bool determining is useable
                    #
                    if (inv_choice_item != None):
                        ui.print_to_game_text(textwrap.fill(inv_choice_item.description, line_length))
                        item_exit = False
                        if inv_choice_item.is_useable == False:
                            while item_exit == False:
                                #printToGameText("This item can't be used. Press 'e' to exit this item")
                                item_choice = ui.get_input("This item can't be used. Press 'e' to exit this item")
                                if item_choice.lower() == 'e':
                                    item_exit = True
                        else:
                            while item_exit == False:
                                #printToGameText("This item can be used. Press 'e' to exit this item or 'u' to use the item")
                                item_choice = ui.get_input("This item can be used. Press 'e' to exit this item or 'u' to use the item")
                                if item_choice.lower() == 'e' or 'u':
                                    item_exit = True
                                    # if using item in inventory should remove it from the inventory and apply its effects
                                    if item_choice.lower() == 'u':
                                        self.player.use_potion(inv_choice_item)
                                        self.player.inventory.removeFromInventory(inv_choice_item)
                                        if inv_choice_item == self.game.goal_consume:
                                            self.game.win()
                    if (type(inv_choice) == str):
                        if (inv_choice.lower() == 'e' or inv_choice.lower() == 'exit'):
                            exit_choice = True
            #if choice_made == None:
                #printToGameText(textwrap.fill(infoText, lineLength))
                #printToGameText(textwrap.fill("Please enter a number or type out the action. These are the options: " + optionsString + " i: inventory", lineLength))

        print("ESCAPED PARSE INPUT")
        print(choice_made)
        return choice_made

    def get_options(self):
        # move options, characters in location and items
        move_options = self.player.location.linked_locations
        character_options = self.player.location.characters
        item_options = self.player.location.items



        options = []
        options_string = ""
        i = 1
        for option in move_options:
            options.append(option)
            options_string += str(i) + ": " + option.name + " "
            i += 1
        if character_options != None:
            for option in character_options:
                options.append(option)
                options_string += str(i) + ": " + option.name+ " "
                i += 1
        if item_options != None:
            for option in item_options:
                options.append(option)
                options_string += str(i) + ": " + option.name+ " "
                i += 1
        return options, options_string

    def fight(self, a_character):
        if a_character.fight_marker != None:
            self.player.add_to_markers(a_character.fight_marker)
        # get the weapons and armor from player and character
        player_weapons, player_armour = self.player.inventory.getWeaponsAndArmour()
        char_weapons, char_armour = a_character.inventory.getWeaponsAndArmour()

        # so, first ask player of options based on what they have in their inventory
        # add barefists and brace to weapons and player options
        bare_fists = item.Item.Weapon("Bare fists", "Your bare fists", 1,-1,None)
        brace = item.Item.Armour(name="Brace", description="Bracing for the attack", armour_stat=2, speed_stat=-1, passive_armour=1)
        player_weapons.extend([bare_fists])
        player_armour.extend([brace])
        options = player_weapons + player_armour
        options_string = ""
        num = 1
        for x in options:
            options_string += str(num) + ": " + x.name + " [" + x.get_stats_string() + "] "
            num += 1
        options += ["run"]
        options_string += str(num) + ": " + "Run"
        fight_string = "You are in a fight with " + a_character.name + "\n" + a_character.name + "'s health is " + str(a_character.health_points) + "\n" + "Your health is " + str(self.player.health_points)
        #printToGameText(fight_string)
        #printToGameText(character.name + "'s health is " + str(character.healthPoints))
       # printToGameText("Your health is " + str(self.player.healthPoints))
        choice = self.parse_input(options, options_string, fight_string)
        char_choice = a_character.fight_choice(char_weapons, char_armour, self.player)
        is_run = False

        # functions for attacking
        def apply_attack_to_none_block(target, target_armour, damage, attacker):
            if not target_armour:
                # if no armor then just apply damage minus the base defence they have
                if damage > target.defence:
                    amount = damage - target.defence
                    target.health_points -= amount
                    if target == self.player:
                        ui.print_to_game_text("You were hit for " + str(amount) + " points of damage")
                        ui.print_to_game_text("You now have " + str(target.health_points) + " health points")
                    else:
                        ui.print_to_game_text(target.name + " was hit for " + str(amount) + " points of damage")
                else:
                    if target == self.player:
                        ui.print_to_game_text(attacker.name + " hit failed to break through your armour")
                    else:
                        ui.print_to_game_text("Your hit failed to break through " + target.name + "'s armour")
            else:
                defence = target.defence
                for x in target_armour:
                    defence += x.passive_armour
                if damage > defence:
                    amount = damage - defence
                    target.health_points -= amount
                    if target == self.player:
                        ui.print_to_game_text("You were hit for " + str(amount) + " points of damage")
                        ui.print_to_game_text("You now have " + str(target.health_points) + " health points")
                    else:
                        ui.print_to_game_text(target.name + " was hit for " + str(amount) + " points of damage")
                else:
                    if target == self.player:
                        ui.print_to_game_text(attacker.name + " hit failed to break through your armour")
                    else:
                        ui.print_to_game_text("Your hit failed to break through " + target.name + "'s armour")
        def apply_attack_to_block(target, target_armour_choice, damage, attacker):
            # if target armor choice is false
            if target_armour_choice == False:
                if damage > target.defence:
                    amount = damage - target.defence
                    target.health_points -= amount
                    if target == self.player:
                        ui.print_to_game_text("You were hit for " + str(amount) + " points of damage")
                        ui.print_to_game_text("You now have " + str(target.health_points) + " health points")
                    else:
                        ui.print_to_game_text(target.name + " was hit for " + str(amount) + " points of damage")
                    return True
                else:
                    if target == self.player:
                        ui.print_to_game_text(attacker.name + " hit failed to break through your armour")
                    else:
                        ui.print_to_game_text("Your hit failed to break through " + target.name + "'s armour")
                    return False
            else:
                # if damage is more than players block choice
                if damage > target_armour_choice.armour_stat + target.defence:
                    amount = damage - (target_armour_choice.armour_stat + target.defence)
                    target.health_points -= amount
                    if target == self.player:
                        ui.print_to_game_text("You were hit for " + str(amount) + " points of damage")
                        ui.print_to_game_text("You now have " + str(target.health_points) + " health points")
                    else:
                        ui.print_to_game_text(target.name + " was hit for " + str(amount) + " points of damage")
                    return True
                else:
                    if target == self.player:
                        ui.print_to_game_text(attacker.name + " hit failed to break through your armour")
                    else:
                        ui.print_to_game_text("Your hit failed to break through " + target.name + "'s armour")
                    return False


        hit_count = 0
        # if player chooses a weapon
        if type(choice) == item.Item.Weapon:
            # add attack of weapon to player damage
            damage = choice.attack_stat + self.player.damage
            # checks if opponent blocked or attack
            if type(char_choice) == item.Item.Armour or char_choice == False:
                # if players attack is bigger than there block then do damage
                if char_choice == False:
                    ui.print_to_game_text("You try to attack with " + choice.name + " and " + a_character.name + " tries to block with no shield.")
                else:
                    ui.print_to_game_text("You try to attack with " + choice.name + " and " + a_character.name + " tries to block with " + char_choice.name + ".")
                # tries to apply attack
                if apply_attack_to_block(a_character, char_choice, damage, self.player):
                    # could be used so if character keeps getting hit then changes approach
                    hit_count += 1
                # else the player didnt do any damage so then should apply biggest damage
                else:
                    ui.print_to_game_text(a_character.name, "fully blocked your attack and so retaliates.")
                    attack_weapon = a_character.inventory.getBiggestDamageWeapon()
                    if attack_weapon == False:
                        # so if no weapon try attack
                        ui.print_to_game_text(a_character.name + " tries to attack you barehanded.")
                        apply_attack_to_none_block(self.player, player_armour, a_character.damage, a_character)
                    else:
                        ui.print_to_game_text(a_character.name + " tries to attack you with a " + attack_weapon.name + ".")
                        apply_attack_to_none_block(self.player, player_armour, a_character.damage + attack_weapon.attack_stat, a_character)



            if type(char_choice) == item.Item.Weapon or char_choice == True:
                # both are attacking so then should then see who attacks faster
                if char_choice == True:
                    # if player is faster
                    if self.player.speed + choice.speed_stat > a_character.speed:
                        ui.print_to_game_text("You move quicker and get the first attack.")
                        apply_attack_to_none_block(a_character, char_armour, choice.attack_stat + self.player.damage, self.player)
                        if a_character.health_points >0:
                            ui.print_to_game_text(a_character.name + " tries to hit you back with their bare fists.")
                            apply_attack_to_none_block(self.player, player_armour, a_character.damage, a_character)

                    else:
                        ui.print_to_game_text(a_character.name + " moves quicker and get the first attack. They attack with their bare fists.")
                        apply_attack_to_none_block(self.player, player_armour, a_character.damage, a_character)
                        if self.player.health_points >0:
                            ui.print_to_game_text("You try to hit back.")
                            apply_attack_to_none_block(a_character, char_armour, choice.attack_stat + self.player.damage, self.player)
                # so if the character does have a weapon
                else:
                    if self.player.speed + choice.speed_stat > a_character.speed + char_choice.speed_stat:
                        ui.print_to_game_text("You move quicker and get the first attack.")
                        apply_attack_to_none_block(a_character, char_armour, choice.attack_stat + self.player.damage, self.player)
                        if a_character.health_points >0:
                            ui.print_to_game_text(a_character.name + " tries to hit you back with " + char_choice.name + ".")
                            apply_attack_to_none_block(self.player, player_armour, a_character.damage + char_choice.attack_stat, a_character)
                    else:
                        ui.print_to_game_text(a_character.name + " moves quicker and get the first attack. They attack with " + char_choice.name + ".")
                        apply_attack_to_none_block(self.player, player_armour, a_character.damage + char_choice.attack_stat, a_character)
                        if self.player.health_points >0:
                            ui.print_to_game_text("You try to hit back.")
                            apply_attack_to_none_block(a_character, char_armour, choice.attack_stat + self.player.damage, self.player)

        elif type(choice) == item.Item.Armour:
            # if the opponent didnt block then see if player blocked their damage fully
            if type(char_choice) == item.Item.Armour or char_choice == False:
                ui.print_to_game_text("You and " + a_character.name + " both stand staring each other down. Both of you tried to block.")
            else:
                shield = choice.armour_stat + self.player.defence
                # if character doesnt have a weapon then do this
                if char_choice == True:
                    ui.print_to_game_text(a_character.name + " tries to hit you with their bare fists.")
                    if apply_attack_to_block(self.player, choice, a_character.damage, a_character):
                        # could be used so if character keeps getting hit then changes approach
                        hit_count += 1

                    # else the player didnt do any damage so then should apply biggest damage
                    else:
                        ui.print_to_game_text("You now get a chance to hit with a counter attack. Choose your weapon.")
                        weapons_string = ""
                        num = 1
                        for x in player_weapons:
                            weapons_string += str(num) + ": " + x.name + "[" + x.get_stats_string() + "] "
                            num += 1

                        player_counter_choice = self.parse_input(player_weapons, weapons_string, "You now get a chance to hit with a counter attack. Choose your weapon.")
                        apply_attack_to_none_block(a_character, char_armour, self.player.damage + player_counter_choice.attack_stat, self.player)
                else:
                    ui.print_to_game_text(a_character.name + " attacks with " + char_choice.name + ".")
                    if apply_attack_to_block(self.player, choice, a_character.damage + char_choice.attack_stat, a_character):
                        # could be used so if character keeps getting hit then changes approach
                        hit_count += 1

                    # else the player didnt do any damage so then should apply biggest damage
                    else:
                        ui.print_to_game_text("You now get a chance to hit with a counter attack. Choose your weapon.")
                        weapons_string = ""
                        num = 1
                        for x in player_weapons:
                            weapons_string += str(num) + ": " + x.name + "[" + x.get_stats_string() + "] "
                            num += 1

                        player_counter_choice = self.parse_input(player_weapons, weapons_string, "You now get a chance to hit with a counter attack. Choose your weapon.")
                        apply_attack_to_none_block(a_character, char_armour, self.player.damage + player_counter_choice.attack_stat, self.player)

        elif choice == "run":
            has_moved = False
            ran_to_location = None
            for location in self.player.location.linked_locations:
                if not has_moved:
                    has_moved = self.run(location)
                    ran_to_location = location
            if has_moved:
                self.player.health_points = math.ceil(self.player.health_points / 2)
                a_character.anger = True
                is_run = True
                ui.print_to_game_text("You just managed to escape by running into " + ran_to_location.name + ". " + a_character.name + " will remember this.")
                ui.print_to_game_text("Your health is now " + str(self.player.health_points))
                return True
            else:
                ui.print_to_game_text("There was nowhere to run to.")



        # if npc still has health then its a failure for the player
        if is_run == False:
            if a_character.health_points <= 0:
                is_success = True
            else:
                is_success = False
            if self.player.health_points > 0:
                print("still alive")
            else:
                ui.print_to_game_text("You died")
                self.game.is_lost = True
                is_success = None

            if is_success == True:
                # character is dead so is removed from the location
                ui.print_to_game_text("You won the fight")
                self.player.location.remove_character(a_character)
                if a_character.inventory.getItems() != []:
                    self.player.location.add_items(a_character.inventory.getItems())
                    text = ""
                    items = a_character.inventory.getItems()
                    for x in items:
                        text += ", "+ x.name
                    ui.print_to_game_text("As " + a_character.name + " falls to the ground, they drop" + text)
                self.player.in_fight = False
                if self.game.goal_character_kill == a_character:
                    self.game.win()
            if is_success == False:
                self.fight(a_character)
            return False

    def talk(self, a_character):
        ui.print_to_game_text(break_line_str)
        if a_character.talk_marker != None:
            self.player.add_to_markers(a_character.talk_marker)
        if a_character.talk_requirement != None:
            if self.player.check_for_marker(a_character.talk_requirement):
                ui.print_to_game_text(textwrap.fill("Hello " + self.player.name + ". " + a_character.info, line_length))
            else:
                ui.print_to_game_text("I am not allowed to speak of this")
        else:
            ui.print_to_game_text(textwrap.fill("Hello " + self.player.name + ". " + a_character.info, line_length))
        if self.game.goal_character_talk == a_character:
            self.game.win()

    def trade(self, a_character):
        ui.print_to_game_text(break_line_str)
        if a_character.wants_trade():
            info_text = "I really want " + a_character.trade_desire.name + ". I am offering " + a_character.trade_offer.name + " for it"
            ui.print_to_game_text(info_text)
            choice = self.parse_input(["yes", "no"], "1: Yes 2: No", info_text)
            if choice == "yes":
                if a_character.trade_desire in self.player.inventory.items:
                    ui.print_to_game_text("Finally I get my hands on", a_character.trade_desire.name)
                    self.player.inventory.removeFromInventory(a_character.trade_desire)
                    self.player.inventory.addToInventory(a_character.trade_offer)
                    a_character.inventory.removeFromInventory(a_character.trade_offer)
                    a_character.inventory.addToInventory(a_character.trade_desire)
                    if a_character.trade_offer == self.game.goal_get:
                        self.game.win()
                    a_character.trade_desire = None
                    a_character.trade_offer = None
                else:
                    ui.print_to_game_text("You don't have", a_character.trade_desire.name + ", you fool.")
            else:
                ui.print_to_game_text("Your loss.")
        else:
            ui.print_to_game_text("I don't want to trade anything with you.")


    def take(self, item):
        if item.marker != None:
            self.player.add_to_markers(item.marker)
        self.player.location.items.remove(item)
        self.player.inventory.addToInventory(item)
        ui.print_to_game_text("You pick up " + item.name + " and put it in your inventory.")

        if item == self.game.goal_get:
            self.game.win()


    def give(self, a_character):
        choice_made = None
        ui.print_to_game_text(break_line_str)
        while choice_made == None:
            choice = ui.get_input(
                "Pick an item to give from your inventory: " + str(self.player.inventory) + "e: exit inventory")
            choice = choice.lower()
            for x in self.player.inventory.items:
                if x.name.lower() == choice:
                    ui.print_to_game_text("You chose " + x.name)
                    choice_made = x
            if choice == "e":
                choice_made = "Exit inventory"
                ui.print_to_game_text("You choose not to give anything")
            try:
                num_choice = int(choice)
                if num_choice <= len(self.player.inventory.items) and num_choice > 0:
                    ui.print_to_game_text("You chose to give " + self.player.inventory.items[num_choice - 1].name)
                    choice_made = self.player.inventory.items[num_choice - 1]
            except ValueError:
                skip_this = 1
                skip_this +=1
                # print("val error")


        if choice_made != "Exit inventory":
            if choice_made.marker != None:
                self.player.add_to_markers(choice_made.marker)
            a_character.inventory.addToInventory(choice_made)
            self.player.inventory.removeFromInventory(choice_made)
            if a_character == self.game.goal_character_give and choice_made == self.game.goal_give:
                self.game.win()


    def character_choices(self, a_character):
        options = ["Talk", "Trade", "Give", "Fight", "Exit interaction"]
        options_string = "1: Talk 2: Trade 3: Give 4: Fight 5: Exit interaction"
        is_exit = False
        while is_exit == False and self.game.win_bool == False:
            choice_made = self.parse_input(options, options_string, a_character.description)

            if choice_made == None:
                # this shouldnt ever be called cus parse input loops itself until gets an output
                ui.print_to_game_text(textwrap.fill(a_character.description, line_length))
                #print("Please enter a number or type out the action. These are the options: " +options_string)
            else:
                # options = ["Talk", "Trade", "Give", "Fight", "Exit interaction", "inventory"]
                if choice_made == options[0]:
                    self.talk(a_character)
                elif choice_made == options[1]:
                    self.trade(a_character)
                elif choice_made == options[2]:
                    self.give(a_character)
                elif choice_made == options[3]:
                    self.fight(a_character)
                    is_exit = True
                elif choice_made == options[4]:
                    is_exit = True


    def item_choices(self, item):
        choice_made = None
        ui.print_to_game_text(break_line_str)
        ui.print_to_game_text(textwrap.fill(item.description, line_length))
        options = ["Take","Exit interaction"]
        options_string = "1: Take e: Exit interaction"
        #printToGameText(options_string)

        while choice_made == None and self.game.win_bool == False:
            player_choice = ui.get_input(options_string)
            if player_choice == "take" or player_choice == "Take":
                self.take(item)
                choice_made = "Take"
            if player_choice == "e":
                choice_made = "Exit interaction"
            try:
                num_choice = int(player_choice)
                if num_choice == 1:
                    self.take(item)
                    choice_made = 1
            except ValueError:
                skip_this = 1
                skip_this += 1
                # print("val error")
            #if choice_made == None:
                #printToGameText(textwrap.fill(item.description, lineLength))
                #printToGameText("Please enter a number or type out the action. These are the options: " + options_string)

    def check_if_fight(self):
        has_fled = False
        # have to make a new list of the characters in location, as if u win the fight the character is removed from the list
        # which affects looping thru with for loop.
        temp_chars = list(self.player.location.characters)
        for a_character in temp_chars:
            # so if player goes into location where there is someone angry at them then starts a fight.
            print("anger", a_character.anger, "has_fled", has_fled)
            if a_character.anger == True and has_fled == False:
                ui.print_to_game_text(a_character.name + " is angry at you and starts a fight.")
                has_fled = self.fight(a_character)
        if has_fled == True:
            self.check_if_fight()
    def make_choice(self):
        # first checks if theres angry ppl in this location.
        self.check_if_fight()
        location_str = "You are in " + self.player.location.name +"\n"+self.player.location.description
        #printToGameText("You are in", self.player.location.name)
        #printToGameText(textwrap.fill(self.player.location.description, lineLength))


        if self.game.is_lost != True:
            # tries to accept input by comparing strings first. make it case non dependant
            # then tries to accept based on number
            # takes the return of the action which is the next action
            options, options_string = self.get_options()
            # so when printing player options should also print an option for inventory

            choice_made = self.parse_input(options, options_string, location_str)
            if type(choice_made) == location.Location:
                self.move_player(choice_made)
            elif type(choice_made) == character.Character.NPC:
                self.character_choices(choice_made)
                # should be in here looping character interaction till they leave the character
            elif type(choice_made) == item.Item or type(choice_made) == item.Item.Armour or type(choice_made) == item.Item.Weapon or type(choice_made) == item.Item.Key or type(choice_made) == item.Item.Potion or type(choice_made) == item.Item.Potion.SpeedPotion  or type(choice_made) == item.Item.Potion.ArmourPotion or type(choice_made) == item.Item.Potion.HealPotion or type(choice_made) == item.Item.Potion.StrengthPotion:
                self.item_choices(choice_made)
