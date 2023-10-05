import random
import math
import textwrap
import ui
import choice
import location
from marker import Marker
import item
import character

line_length = 1000
break_line_str = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# this file is for generating text adventure games.
# maps are built and populated with characters and items
# there are funtions which can call from game object to see details of that game
def link_locations(locations):
    for location in locations:
        for loc in locations:
            # so loop thru locations and link other locations here. and if already been linked then dont link it again
            # location should be added to other location if its not in there
            if loc != location and not loc in location.linked_locations:
                location.add_linked_locations([loc])

def load_data(setting):
    location_dataset = []
    if setting == 0:
        with open('locationsM.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                location_dataset.append(values)
        character_dataset = []
        with open('charactersM.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                character_dataset.append(values)
        consumables_dataset = []
        with open('consumablesM.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                consumables_dataset.append(values)
        weapons_dataset = []
        with open('weaponsM.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                weapons_dataset.append(values)
        armour_dataset = []
        with open('armorM.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                armour_dataset.append(values)
        info_dataset = []
        with open('infosM.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                info_dataset.append(values)

    if setting == 1:
        with open('locationsWW.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                location_dataset.append(values)
        character_dataset = []
        with open('charactersWW.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                character_dataset.append(values)
        consumables_dataset = []
        with open('consumablesWW.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                consumables_dataset.append(values)
        weapons_dataset = []
        with open('weaponsWW.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                weapons_dataset.append(values)
        armour_dataset = []
        with open('armorWW.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                armour_dataset.append(values)
        info_dataset = []
        with open('infosWW.txt', 'r') as file:
            for line in file:
                values = line.strip().split('@')
                info_dataset.append(values)
    return location_dataset, character_dataset, consumables_dataset, weapons_dataset, armour_dataset, info_dataset



class Game:
    # this method should make use of methods to generate npcs, items, locations, etc
    def __init__(self, seed=None, goal=None, game_size = None, setting = None):
        self.goal_character_talk = None
        self.goal_consume = None
        self.goal_character_give = None
        self.goal_character = None
        self.goal_give = None
        self.goal_get = None
        self.goal_loc = None
        self.goal_loc_get_to = None
        self.win_str = None
        self.intro_str = None
        self.locations = []
        self.characters = []
        self.items = []
        self.weapons = []
        self.armour = []
        self.consumables = []
        self.seed = seed
        while self.seed == None:
            temp = ui.get_input("What seed do you want for the game? Must be a whole number.")
            if temp.isdigit():
                self.seed = temp
        random.seed(self.seed)
        self.item_counter = random.randint(0, 2)
        # ask the player for a game size
        self.game_size = game_size
        while self.game_size == None:
            temp = ui.get_input("What size for the game do you want? s: small m: medium l: large")
            temp = temp.lower()
            if temp == 's' or temp == 'small':
                self.game_size = 10
            elif temp == 'm' or temp == 'medium':
                self.game_size = 25
            elif temp == 'l' or temp == 'large':
                self.game_size = 40
        if self.game_size < 10:
            self.game_size = 10
        if self.game_size > 70:
            self.game_size = 70
        self.goal_consume_type = None
        self.goal_take_type = None
        self.goal_character_kill = None
        self.setting = setting
        while self.setting == None:
            temp = ui.get_input("What setting for the game do you want? ww: wild west m: medieval")
            temp = temp.lower()
            if temp == 'ww' or temp == 'wild west':
                self.setting = 1
                print("set setting to 1 ")
            elif temp == 'm' or temp == 'medieval':
                self.setting = 0
        self.goal = goal
        while self.goal == None:
            #kill, take, give, consume, talk, get to
            temp = ui.get_input("What quest for the game do you want? 1: assassination 2: item acquisition 3: item delivery 4: consume 5: message delivery 6: go to")
            temp = temp.lower()
            if temp == '1' or temp == 'assassination':
                self.goal = 0
            elif temp == '2' or temp == 'item acquisition':
                self.goal = 1
            elif temp == '3' or temp == 'item delivery':
                self.goal = 2
            elif temp == '4' or temp == 'consume':
                self.goal = 3
            elif temp == '5' or temp == 'message delivery':
                self.goal = 4
            elif temp == '6' or temp == 'go to':
                self.goal = 5
        self.location_dataset, self.character_dataset, self.consumables_dataset, self.weapons_dataset, self.armour_dataset, self.info_dataset = load_data(self.setting)
        self.generate_locations()
        self.generate_items()
        self.generate_characters()
        self.added_locations = []
        self.angry_count = 0
        self.angry_delay = 0
        self.define_goal()
        self.win_bool = False
        self.is_lost = False



    def spawn_player(self, player):
        #player.location = self.addedLocations[random.randint(0,len(self.addedLocations)-1)]
        viable_spawns = [x for x in self.added_locations if x.requirement == None]
        # dont spawn where the place needed to get into marker loc
        if self.game_size <= 30:
            viable_spawns.remove(self.marker_marker_loc)
        elif self.game_size <= 50:
            viable_spawns.remove(self.marker_3_loc)
        elif self.game_size > 50:
            viable_spawns.remove(self.marker_4_loc)

        none_angry = []
        for x in viable_spawns:
            has_angry = False
            for char in x.characters:
                if char.anger == True:
                    has_angry = True
            if has_angry == False:
                none_angry.append(x)

        # check if location has linked location which doesnt contain an angry
        is_spawned = False
        while is_spawned == False:
            if len(none_angry) > 0:
                popped_loc = none_angry.pop(random.randint(0,len(none_angry)-1))
            else:
                ui.print_to_game_text("Found nowhere viable to spawn the player")
            for linked in popped_loc.linked_locations:
                has_angry = False
                for char in linked.characters:
                    if char.anger == True:
                        has_angry = True
                if has_angry == False:
                    player.location = popped_loc
                    is_spawned = True



    def print_start_text(self):
        ui.print_to_game_text(textwrap.fill(self.intro_str, line_length))

    # Generating an amount of locations based on the game size
    def generate_locations(self):
        for n in range(self.game_size):
            if self.location_dataset:
                rand_num = random.randint(0, len(self.location_dataset) - 1)
                self.locations.append(location.Location(self.location_dataset[rand_num][0], self.location_dataset[rand_num][1]))
                self.location_dataset.pop(rand_num)



    # Generating an amount of characters based on the game size
    def generate_characters(self):
        for n in range(self.game_size):
            if self.character_dataset:
                rand_num = random.randint(0, len(self.character_dataset) - 1)
                hp = random.randint(1, 8)
                dmg = random.randint(1, 8)
                speed = random.randint(1, 8)
                defence = random.randint(1, 8)
                info = self.info_dataset.pop(random.randint(0, len(self.info_dataset) - 1))
                self.characters.append(character.Character.NPC(self.character_dataset[rand_num][0], self.character_dataset[rand_num][1], hp, dmg, speed, defence, info=info[1]))
                self.character_dataset.pop(rand_num)

    # Generating an amount of items based on the game size
    def generate_items(self):
        for n in range(self.game_size):
            if self.weapons_dataset:
                rand_num = random.randint(0, len(self.weapons_dataset) - 1)
                dmg = random.randint(1, 10)
                speed = -random.randint(1, 10)
                self.weapons.append(item.Item.Weapon(self.weapons_dataset[rand_num][0], self.weapons_dataset[rand_num][1], dmg, speed))
                self.weapons_dataset.pop(rand_num)

        for n in range(self.game_size):
            if self.armour_dataset:
                rand_num = random.randint(0, len(self.armour_dataset) - 1)
                shield = random.randint(1, 10)
                speed = -random.randint(1, 10)
                # so passive is calculated by dividing shield by 1to shield amount and rounding it up. this means passive cant be more than shield
                passive_shield = math.ceil(shield/random.randint(1,shield))
                self.armour.append(item.Item.Armour(self.armour_dataset[rand_num][0], self.armour_dataset[rand_num][1], shield, speed, passive_shield))
                self.armour_dataset.pop(rand_num)
        # so consumables sshould uhhhh. i guess

        for n in range(self.game_size):
            if self.consumables_dataset:
                rand_num = random.randint(0, len(self.consumables_dataset) - 1)
                consumable_type = random.randint(1,4)
                stat = random.randint(1,10)
                if consumable_type == 1:
                    # health
                    self.consumables.append(item.Item.Potion.HealPotion(self.consumables_dataset[rand_num][0],
                                                                        self.consumables_dataset[rand_num][1], stat / 10))
                elif consumable_type == 2:
                    # strength
                    self.consumables.append(item.Item.Potion.StrengthPotion(self.consumables_dataset[rand_num][0],
                                                                            self.consumables_dataset[rand_num][1], stat))
                elif consumable_type == 3:
                    # speed
                    self.consumables.append(item.Item.Potion.SpeedPotion(self.consumables_dataset[rand_num][0],
                                                                         self.consumables_dataset[rand_num][1], stat))
                elif consumable_type == 3:
                    # speed
                    self.consumables.append(item.Item.Potion.ArmourPotion(self.consumables_dataset[rand_num][0],
                                                                          self.consumables_dataset[rand_num][1], stat))

                self.consumables_dataset.pop(rand_num)

    # this function will work by having a few goals. call after generating content
    #  kill, take, give, consume, talk, get to
    def define_goal(self):
        # if goal is none then randomly assign goal from 0-5
        if self.goal == None:
            self.goal = random.randint(0,5)
        # then assign goal win marker.
        if self.goal == 0:
            # goal is kill then. assigns character you aim to kill
            self.goal_character_kill = self.characters.pop(random.randint(0, len(self.characters) - 1))
            # then put this character in location and make this location require markers to reach.
            self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
            self.goal_loc.add_characters([self.goal_character_kill])
        elif self.goal == 1:
            # goal is take. player should take an item. this could mean trade to unlock it, kill or just take
            # so add consumables now as dont need to differentiate
            # if trade or kill give it to someone and hide them away. if just take make location hard to get to
            self.goal_take_type = random.randint(1, 3)
            if self.goal_take_type == 1 or self.goal_take_type == 2:
                self.goal_get = self.pop_item()
                self.goal_character = self.characters.pop(random.randint(0, len(self.characters) - 1))
                if self.goal_take_type == 1:
                    # trade
                    self.goal_character.trade_offer = self.goal_get
                    self.goal_character.inventory.addToInventory(self.goal_get)
                    self.goal_character.trade_desire =  self.pop_item()
                    self.goalTrade = self.goal_character.trade_desire
                elif self.goal_take_type == 2:
                    # kill
                    self.goal_character.inventory.addToInventory(self.goal_get)

                # add to location the character
                self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
                self.goal_loc.add_characters([self.goal_character])
            elif self.goal_take_type == 3:
                # just take
                self.goal_get =  self.pop_item()
                self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
                self.goal_loc.add_items([self.goal_get])
        elif self.goal == 2:
            # give
            self.goal_give = self.pop_item()
            self.goal_character_give = self.characters.pop(random.randint(0, len(self.characters) - 1))
            self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
            self.goal_loc.add_characters([self.goal_character_give])
        elif self.goal == 3:
            # consume. this is whats used in generate items the consumable part. so if leftover consumable just do one of them
            self.goal_consume_type =  random.randint(1, 3)
            # if trade or kill give it to someone and hide them away. if just take make location hard to get to
            if self.goal_consume_type == 1 or self.goal_consume_type == 2:
                self.goal_consume = self.consumables.pop(random.randint(0, len(self.consumables) - 1))
                self.goal_character = self.characters.pop(random.randint(0, len(self.characters) - 1))
                if self.goal_consume_type == 1:
                    # trade
                    self.goal_character.trade_offer = self.goal_consume
                    self.goal_character.inventory.addToInventory(self.goal_consume)
                    self.goal_character.trade_desire = self.consumables.pop(random.randint(0, len(self.consumables) - 1))
                    self.goalTrade = self.goal_character.trade_desire
                elif self.goal_consume_type == 2:
                    # kill
                    self.goal_character.inventory.addToInventory(self.goal_consume)

                # add to location the character
                self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
                self.goal_loc.add_characters([self.goal_character])
            elif self.goal_consume_type == 3:
                # just take
                self.goal_consume = self.consumables.pop(random.randint(0, len(self.consumables) - 1))
                self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
                self.goal_loc.add_items([self.goal_consume])

            # so add consumables after as needed to differentiate
        elif self.goal == 4:
            # talk
            # so add consumables now as dont need to differentiate
            self.goal_character_talk = self.characters.pop(random.randint(0, len(self.characters) - 1))
            self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
            self.goal_loc.add_characters([self.goal_character_talk])
        elif self.goal == 5:
            # get to
            # so add consumables now as dont need to differentiate
            self.goal_loc = self.locations.pop(random.randint(0, len(self.locations) - 1))
            self.goal_loc_get_to = self.goal_loc

        # add goal location to addedlocations
        self.added_locations.append(self.goal_loc)

        # so first give goalLoc a requirement
        # then link seperately two or three locations to that.
        # create info strings. one says where the thing is to get in there. one saying what is in there.

        def lock_location(location_to_lock, whats_in_lock_loc):
            # this function will take in a location
            # this may need to be changed. so its not returning marker but marker is saved to be used
            # 1. give location a marker
            marker = Marker("Marker")
            location_to_lock.requirement = marker
            # 2. link locations next to it
            loc1 = self.locations.pop(random.randint(0, len(self.locations)-1))
            loc2 = self.locations.pop(random.randint(0, len(self.locations)-1))
            link_locations([location_to_lock, loc1, loc2])
            # 3. add new location and hide marker in there
            marker_loc = self.locations.pop(random.randint(0, len(self.locations)-1))
            # add new ones to added locations
            self.added_locations.extend([loc1, loc2, marker_loc])
            # marker should be of a few different types. fight, object, talk etc
            marker_type = random.randint(0,2)
            if marker_type == 0:
                # that means fight marker
                # give character two items
                fight_char = self.characters.pop(random.randint(0,len(self.characters)-1))
                fight_char.inventory.addToInventory(self.pop_item())
                fight_char.inventory.addToInventory(self.pop_item())
                fight_char.fight_marker = marker
                marker_loc.add_characters([fight_char])
                # form strings here and add em to characters in loc1 and loc2
                str1 = "They don't just let anyone into " + location_to_lock.name + ". " + whats_in_lock_loc
                str2 = "To get into " + location_to_lock.name + " you have to prove yourself by killing " + fight_char.name + ". They can be found in " + marker_loc.name
                loc1_char = self.characters.pop(random.randint(0, len(self.characters)-1))
                loc2_char = self.characters.pop(random.randint(0, len(self.characters)-1))
                loc1_char.info = str1
                loc2_char.info = str2
                loc1.add_characters([loc1_char])
                loc2.add_characters([loc2_char])


            elif marker_type == 1:
                # object is a marker
                item_marker = self.pop_item()
                item_marker.marker = marker
                marker_loc.add_items([item_marker])
                # form strings here and add em to characters in loc1 and loc2
                str1 = "They don't just let anyone into " + location_to_lock.name + ". " + whats_in_lock_loc
                str2 = "To get into " + location_to_lock.name + " you have to prove yourself by acquiring '" + item_marker.name + "'. This can be found in " + marker_loc.name
                loc1_char = self.characters.pop(random.randint(0, len(self.characters)-1))
                loc2_char = self.characters.pop(random.randint(0, len(self.characters)-1))
                loc1_char.info = str1
                loc2_char.info = str2
                loc1.add_characters([loc1_char])
                loc2.add_characters([loc2_char])

            elif marker_type == 2:
                # talk
                talk_char = self.characters.pop(random.randint(0, len(self.characters)-1))
                marker_loc.add_characters([talk_char])
                talk_char.talk_marker = marker
                # form strings here and add em to characters in loc1 and loc2
                str1 = "They don't just let anyone into " + location_to_lock.name + ". " + whats_in_lock_loc
                str2 = "It's very difficult to get into " + location_to_lock.name + ", I heard that " + talk_char.name + " knows how to get in, ask them. They can be found in " + marker_loc.name
                loc1_char = self.characters.pop(random.randint(0, len(self.characters)-1))
                loc2_char = self.characters.pop(random.randint(0, len(self.characters)-1))
                loc1_char.info = str1
                loc2_char.info = str2
                loc1.add_characters([loc1_char])
                loc2.add_characters([loc2_char])
                talk_options = ["There's a secret tunnel into " + location_to_lock.name, "Climb the walls to get into " + location_to_lock.name, "Go to " + location_to_lock.name + " now, the doorman will let you in"]
                talk_char.info = talk_options[random.randint(0, len(talk_options)-1)]

            return marker_loc

        whats_in_lock_loc_string = ""
        #  kill, take, give, consume, talk, get to
        if self.goal == 0:
            whats_in_lock_loc_string = self.goal_character_kill.name + " is in there."
        elif self.goal == 1:
            whats_in_lock_loc_string = self.goal_get.name + " is in there."
        elif self.goal == 2:
            whats_in_lock_loc_string = self.goal_character_give.name + " is in there."
        elif self.goal == 3:
            whats_in_lock_loc_string = self.goal_consume.name + " is in there."
        elif self.goal == 4:
            whats_in_lock_loc_string = self.goal_character_talk.name + " is in there."
        elif self.goal == 5:
            whats_in_lock_loc_string = "It's the " + self.goal_loc_get_to.name + ", of course not just anyone can get in."

        # goal locations lock down
        marker_loc = lock_location(self.goal_loc, whats_in_lock_loc_string)
        self.marker_loc = marker_loc
        # location of marker needed to get into goal should now be locked down.
        str_clue = "Supposedly, what lies in " + marker_loc.name + " is needed to get into " + self.goal_loc.name
        marker_marker_loc = lock_location(marker_loc, str_clue)
        self.marker_marker_loc = marker_marker_loc


        # now should connect all the locations and add items and characters with items and ye
        # so loop thru linked locations of the goal location, the marker_loc and marker_marker_loc and assign them stuff
        # and then link their linked

        # adding items to some characters
        popped_characters = []
        for n in range(math.ceil(len(self.characters)/3)):
            if len(self.weapons) > 1 and len(self.armour)>1 and len(self.consumables)>1 :
                rand_amount = random.randint(0,3)
                character1 = self.characters.pop(random.randint(0, len(self.characters)-1))
                popped_characters.append(character1)
                for x in range(rand_amount):
                    character1.inventory.addToInventory(self.pop_item())

        # add the characters back into characters
        self.characters.extend(popped_characters)

        # now link locations and add characters/items. so get a location give it 0-1 item and 0-2 characters. but 50-50 if characters n then 50-50 if 1 or 2
        # make graph traversing function. so start at location, get linked locations, if has some then go to them, add characters and items
        # if doesnt have locations, link new ones then go to them. have a chance to not add a new location, so like a dead end.
        # then when run out of locations (self.location is determined by gamesize)


        def build_map(Locations):
            # bridging locations is dependant on game size
            if self.game_size <= 15:
                max_bridge_length = 1
                character_and_item_max = 1
                angry_amount = 1
                self.angry_delay = 1
                base_angry_delay = 1
            elif self.game_size > 15 and self.game_size <= 20:
                max_bridge_length = 3
                character_and_item_max = 2
                angry_amount = 2
                self.angry_delay = 2
                base_angry_delay = 2
            elif self.game_size > 20 and self.game_size <= 30:
                max_bridge_length = 4
                character_and_item_max = 3
                angry_amount = 3
                self.angry_delay = 3
                base_angry_delay = 3
            elif self.game_size > 30 and self.game_size <= 50:
                max_bridge_length = 4
                character_and_item_max = 3
                angry_amount = 4
                self.angry_delay = 4
                base_angry_delay = 4
            else:
                max_bridge_length = 4
                character_and_item_max = 4
                if self.game_size < 60:
                    angry_amount = 5
                elif self.game_size < 70:
                    angry_amount = 6
                elif self.game_size <= 80:
                    angry_amount = 7
                self.angry_delay = 5
                base_angry_delay = 5



            def bridge_locations(loc1, loc2, bridge_size):
                last_loc_added = loc1
                for n in range(bridge_size):
                    new_loc = self.locations.pop(random.randint(0,len(self.locations)-1))
                    # add new loc to addedLocations
                    self.added_locations.extend([new_loc])
                    link_locations([last_loc_added, new_loc])
                    last_loc_added = new_loc
                link_locations([last_loc_added, loc2])

            # link locations so there is ways to get to each
            # so for different sizes of games make bigger maps with more locked things
            if self.game_size <= 30:
                bridge_locations(self.goal_loc.linked_locations[0], marker_loc.linked_locations[0], max_bridge_length)
                bridge_locations(self.goal_loc.linked_locations[1], marker_marker_loc, max_bridge_length)
                bridge_locations(marker_loc.linked_locations[1], marker_marker_loc, max_bridge_length)
            elif self.game_size <= 50:
                str_clue = "Supposedly, what lies in " + marker_marker_loc.name + " is needed to get into " + marker_loc.name
                marker_3_loc = lock_location(marker_marker_loc, str_clue)
                self.marker_3_loc = marker_3_loc
                # builds bridges in this shape
                # gl ------ ml
                # |         |
                # |         |
                # mml ----- m3
                bridge_locations(self.goal_loc.linked_locations[0], marker_loc.linked_locations[0], max_bridge_length)
                bridge_locations(self.goal_loc.linked_locations[1], marker_marker_loc.linked_locations[0], max_bridge_length)
                bridge_locations(marker_loc.linked_locations[1], marker_3_loc, max_bridge_length)
                bridge_locations(marker_marker_loc.linked_locations[1], marker_3_loc, max_bridge_length)
            elif self.game_size > 50:
                str_clue = "Supposedly, what lies in " + marker_marker_loc.name + " is needed to get into " + marker_loc.name
                marker_3_loc = lock_location(marker_marker_loc, str_clue)
                self.marker_3_loc = marker_3_loc
                str_clue = "Supposedly, what lies in " + marker_3_loc.name + " is needed to get into " + marker_marker_loc.name
                marker_4_loc = lock_location(marker_3_loc, str_clue)
                self.marker_4_loc = marker_4_loc
                # builds bridges in this shape
                # gl ------ ml
                # |            \
                # |             m4
                # |           /
                # mml ----- m3
                bridge_locations(self.goal_loc.linked_locations[0], marker_loc.linked_locations[0], max_bridge_length)
                bridge_locations(self.goal_loc.linked_locations[1], marker_marker_loc.linked_locations[0], max_bridge_length)
                bridge_locations(marker_loc.linked_locations[1], marker_4_loc, max_bridge_length)
                bridge_locations(marker_marker_loc.linked_locations[1], marker_3_loc.linked_locations[0], max_bridge_length)
                bridge_locations(marker_3_loc.linked_locations[1], marker_4_loc, max_bridge_length)



            # now just add more locations, and add items and characters to those new locations.
            # loop thru current locations by accessing linked locations and saving them.
            # then if not having a requirement or more than 3 locations then can add new location to link to.
            # every 3 locations added link it to a location already addded. this ensures inter-connectedness

            def add_and_link_new_loc(location):
                new_loc = self.locations.pop(random.randint(0, len(self.locations)-1))
                # add new loc to addedLocations
                self.added_locations.extend([new_loc])
                link_locations([location, new_loc])
                return new_loc

            # this method loops thru viable locations (which are added locations with < 3 linked locs and no requirements
            # and adds new characters which get spawned with items and characters
            # and adds connections every 3rd new location added

            #so while loop for viable locs
            #pop first instance.
            #if has more than amount of connections, dont add it to holder list.
            #if not then add it to holder list,
            #then when linking next this uses both lists, and check then for locations linked to if those are more than amount.
            #do it till viable locs is empty
            viable_locs = [x for x in self.added_locations if x.requirement == None and len(x.linked_locations) < 3]
            holder_locs = []
            while viable_locs:
                new_loc_counter = 0
                temp_loc = viable_locs.pop(0)
                if len(temp_loc.linked_locations) < 3:
                    if len(self.locations) > 2:
                        amount = random.randint(0, 2)
                        for n in range(amount):
                            new_loc = add_and_link_new_loc(temp_loc)
                            viable_locs.append(new_loc)
                            new_loc_counter += 1
                    else:
                        for i in range(random.randint(1,2)):
                            combined = viable_locs + holder_locs
                            if len(combined) > 0:
                                linked_loc = combined[random.randint(0, len(combined) - 1)]
                                link_locations([temp_loc, linked_loc])
                                if len(linked_loc.linked_locations) >= 3:
                                    if linked_loc in viable_locs:
                                        viable_locs.remove(linked_loc)
                                    if linked_loc in holder_locs:
                                        holder_locs.remove(linked_loc)
                    if new_loc_counter >1:
                        new_loc_counter = 0
                        # add link to location already added
                        # shouldnt be added to location with marker or
                        for i in range(random.randint(1,2)):
                            combined = viable_locs + holder_locs
                            if len(combined) > 0:
                                linked_loc = combined[random.randint(0, len(combined) - 1)]
                                link_locations([temp_loc, linked_loc])
                                if len(linked_loc.linked_locations) >= 3:
                                    if linked_loc in viable_locs:
                                        viable_locs.remove(linked_loc)
                                    if linked_loc in holder_locs:
                                        holder_locs.remove(linked_loc)
                    if len(temp_loc.linked_locations) < 3:
                        holder_locs.append(temp_loc)


            # this method will add few characters n items
            def add_random_characters(location):
                # 2/3 chance. if below 0.663 add 1-3 characters
                if len(self.characters) >= character_and_item_max:
                    amount = random.randint(1, character_and_item_max)
                    for i in range(amount):
                        poppedChar = self.characters.pop(random.randint(0,len(self.characters)-1))
                        if self.angry_count < angry_amount:
                            if self.angry_delay == 0:
                                poppedChar.anger = True
                                self.angry_count += 1
                                self.angry_delay = base_angry_delay
                            else:
                                self.angry_delay -= 1
                        location.add_characters([poppedChar])

            def add_random_items(location):
                if len(self.weapons) > 1 and len(self.armour)>1 and len(self.consumables)>1 and (len(self.weapons) + len(self.armour) + len(self.consumables))> character_and_item_max:
                    amount = random.randint(1, character_and_item_max)
                    for i in range(amount):
                        location.add_items([self.pop_item()])

            viable_locs_for_adding = [x for x in self.added_locations if x.requirement == None]
            random.shuffle(viable_locs_for_adding)
            counter = 0
            counter_direction = True
            for location in viable_locs_for_adding:
                # want a way to determine order added to the locations. so shuffle locations. then go - char, item, char n item, none, char n item, item, char
                if counter == 0:
                    add_random_characters(location)
                elif counter == 1:
                    add_random_items(location)
                elif counter == 2:
                    add_random_characters(location)
                    add_random_items(location)
                if counter == 0:
                    counter_direction = True
                elif counter == 3:
                    counter_direction = False
                if counter_direction == True:
                    counter += 1
                elif counter_direction == False:
                    counter -= 1



        # now build map
        build_map([self.goal_loc, marker_loc, marker_marker_loc])

        # then should add player to starting location
        # should spawn player in a location which isnt blocked by a requirement
        # should give the player an introduction text which is determined by the gameGoal
        # also needs to set goal give. and checks for if the player has won
        # kill, take, give, consume, talk, get to
        # this below adds more for specific goals

        def add_item_to_viable_loc(item):
            viable_locs_for_adding = [x for x in self.added_locations if x.requirement == None]
            rand_num = random.randint(0, len(viable_locs_for_adding) - 1)
            viable_locs_for_adding[rand_num].add_items([item])

        if self.setting == 0:
            if self.goal == 0:
                self.intro_str = "The kingdom of Mistrun has fallen into disarray. Your destiny is to find and kill " + self.goal_character_kill.name + ", and restore balance to Mistrun."
                self.win_str = "You fulfilled your destiny and killed " + self.goal_character_kill.name + ", and have restored balance to Mistrun."
            elif self.goal == 1:
                self.intro_str = "You have lost your beloved " + self.goal_get.name + ". You are to track down and acquire it."
                self.win_str = "You found your beloved " + self.goal_get.name + ". All is well."
                # here is where item to give in trade should be
                if self.goal_take_type == 1:
                    add_item_to_viable_loc(self.goalTrade)
            elif self.goal == 2:
                self.intro_str = self.goal_character_give.name + " needs the " + self.goal_give.name + " to survive. The order of this land lies in your very hands."
                self.win_str = "Because of you " + self.goal_character_give.name + " lives. Order of the land remains."
                # assigning the item to give to a location
                add_item_to_viable_loc(self.goal_give)

            elif self.goal == 3:
                self.intro_str = "This place has an ancient ritual, where those who consume " + self.goal_consume.name + " become the divine ruler. You feel it, that this is your destiny."
                self.win_str = "You complete the ancient ritual to consume " + self.goal_consume.name + " and you have become the divine ruler."
                # here is where item to give in trade should be
                if self.goal_consume_type == 1:
                    add_item_to_viable_loc(self.goalTrade)
            elif self.goal == 4:
                self.intro_str = "You have been tasked with delivering a vital message to " + self.goal_character_talk.name
                self.win_str = "You successfully delivered the vital message to" + self.goal_character_talk.name + ". All is well."
            elif self.goal == 5:
                self.intro_str = "Your life is in danger, there is only one place which will prove safe and that is " + self.goal_loc_get_to.name + ". You are to go to there."
                self.win_str = "You managed to get to " + self.goal_loc_get_to.name + ". You go on to live a long and bountiful life."
            else:
                self.intro_str = "Something is wrong and the intro can't be determined"
                self.win_str = "Something is wrong and the win string can't be determined"

        if self.setting == 1:
            if self.goal == 0:
                self.intro_str = "Tumbleweed City has fallen into disarray. You are hired to find and kill " + self.goal_character_kill.name + ", and restore balance to Tumbleweed City."
                self.win_str = "You fulfilled your contract and killed " + self.goal_character_kill.name + ", and have restored balance to Tumbleweed City."
            elif self.goal == 1:
                self.intro_str = "You have lost your beloved " + self.goal_get.name + ". You are to track down and acquire it."
                self.win_str = "You found your beloved " + self.goal_get.name + ". All is well."
                # here is where item to give in trade should be
                if self.goal_take_type == 1:
                    add_item_to_viable_loc(self.goalTrade)
            elif self.goal == 2:
                self.intro_str = self.goal_character_give.name + " needs the " + self.goal_give.name + " to survive. Their life lies in your very hands."
                self.win_str = "Because of you " + self.goal_character_give.name + " lives."
                # assigning the item to give to a location
                add_item_to_viable_loc(self.goal_give)

            elif self.goal == 3:
                self.intro_str = "This place has a unique superstition, where those who consume " + self.goal_consume.name + " become invincible. You are sick and desperate, this is your last hope of survival."
                self.win_str = "You complete the superstition to consume " + self.goal_consume.name + " and you instantly feel better. You go on to live a long life."
                # here is where item to give in trade should be
                if self.goal_consume_type == 1:
                    add_item_to_viable_loc(self.goalTrade)
            elif self.goal == 4:
                self.intro_str = "You have been tasked with delivering a vital message to " + self.goal_character_talk.name
                self.win_str = "You successfully delivered the vital message to" + self.goal_character_talk.name + ". All is well."
            elif self.goal == 5:
                self.intro_str = "Your life is in danger, there is only one place which will prove safe and that is " + self.goal_loc_get_to.name + ". You are to go to there."
                self.win_str = "You managed to get to " + self.goal_loc_get_to.name + ". You go on to live a long and bountiful life."
            else:
                self.intro_str = "Something is wrong and the intro can't be determined"
                self.win_str = "Something is wrong and the win string can't be determined"

        def shuffle_location(locationToShuffle: location.Location):
            random.shuffle(locationToShuffle.linked_locations)
            random.shuffle(locationToShuffle.characters)
            random.shuffle(locationToShuffle.items)

        for loc in self.added_locations:
            shuffle_location(loc)

    def win(self):
        ui.print_to_game_text("CONGRATULATIONS!!!")
        ui.print_to_game_text(textwrap.fill(self.win_str, line_length))
        self.win_bool = True


    def play_game(self, player):
        self.print_start_text()
        self.is_lost = False
        self.spawn_player(player)
        choice1 = choice.Choice(player, self)
        while self.win_bool == False and self.is_lost == False:
            choice1.make_choice()

    def print_details(self):
        for location in self.added_locations:
            text = ""
            for link in location.linked_locations:
                text += link.name + ", "
            ui.print_to_game_text("In " + location.name + ": " + text)

    def print_characters(self):
        for location in self.added_locations:
            text = ""
            for character in location.characters:
                text += character.name + ", "
            ui.print_to_game_text("In " + location.name + ": " + text)

    def print_items(self):
        for location in self.added_locations:
            text = ""
            for item in location.items:
                text += item.name + ", "
            ui.print_to_game_text("In " + location.name + ": " + text)

    def print_items_in_characters(self):
        for location in self.added_locations:
            for character in location.characters:
                text = ""
                for item in character.inventory.items:
                    text += item.name + ", "
                ui.print_to_game_text("for " + character.name + ": " + text)

    def pop_item(self):
        # based on own counter will pop value from weapon, consumable or armor
        # pop weapon
        if self.item_counter == 0:
            popped_item = self.weapons.pop(random.randint(0,len(self.weapons)-1))
        if self.item_counter == 1:
            popped_item = self.armour.pop(random.randint(0, len(self.armour) - 1))
        if self.item_counter == 2:
            popped_item = self.consumables.pop(random.randint(0,len(self.consumables)-1))
        self.item_counter += 1
        if self.item_counter == 3:
            self.item_counter = 0
        return popped_item

    def print_how_to_win(self):
        ui.print_to_game_text("This is how to win:")
        ui.print_to_game_text("Win condition is in " + self.goal_loc.name)
        if self.goal == 0:
            # kill
            ui.print_to_game_text("The goal is to kill " + self.goal_character_kill.name)
        elif self.goal == 1:
            # get
            ui.print_to_game_text("The goal is to get " + self.goal_get.name)
            if self.goal_take_type == 1:
                # trade
                ui.print_to_game_text("Trade to get item (Or just kill the character) from " + self.goal_character.name)
                ui.print_to_game_text("What you get from trade " + self.goal_character.trade_offer.name)
                ui.print_to_game_text("What you have t give " + self.goal_character.trade_desire.name)
            elif self.goal_take_type == 2:
                # kill
                ui.print_to_game_text("Kill " + self.goal_character.name + " to get item")
            else:
                ui.print_to_game_text("Just have to take item from the location")
        elif self.goal == 2:
            # give
            ui.print_to_game_text("The goal is to give " + self.goal_give.name + " this item: " + self.goal_character_give.name)
        elif self.goal == 3:
            # consume.
            ui.print_to_game_text("The goal is to consume " + self.goal_consume.name)
            if self.goal_consume_type == 1:
                # trade
                ui.print_to_game_text("Trade to consume")
                ui.print_to_game_text("Trade to get item (Or just kill the character) from " + self.goal_character.name)
                ui.print_to_game_text("What you get from trade " + self.goal_character.trade_offer.name)
                ui.print_to_game_text("What you have to give " + self.goal_character.trade_desire.name)
            elif self.goal_consume_type == 2:
                # kill
                ui.print_to_game_text("Kill " + self.goal_character.name + " to get item")
            elif self.goal_consume_type == 3:
                # just take
                ui.print_to_game_text("just take the item from location")
        elif self.goal == 4:
            # talk
            ui.print_to_game_text("Goal is to talk to" + self.goal_character_talk.name)
        elif self.goal == 5:
            # get to
            ui.print_to_game_text("Just get to goal location")
        ui.print_to_game_text("You require whats in:", self.marker_loc.name, "To get into", self.goal_loc.name, ". You require whats in", self.marker_marker_loc.name, "To get into", self.marker_loc.name)
        if self.game_size > 30 and self.game_size <= 50:
            ui.print_to_game_text("You require whats in:", self.marker_3_loc.name, "To get into", self.marker_marker_loc.name)
        if self.game_size > 50:
            ui.print_to_game_text("You require whats in:", self.marker_3_loc.name, "To get into", self.marker_marker_loc.name,
                  ". You require whats in", self.marker_4_loc.name, "To get into", self.marker_3_loc.name)
        ui.print_to_game_text("\n")