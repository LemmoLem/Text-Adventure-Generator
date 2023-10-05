import inventory
import math
import item
from ui import print_to_game_text

# This file is for the NPC and player character.
# there are functions for the player to use a potion and for finding npc's choice in a fight
class Character:
    class Player:
        def __init__(self, name, description, base_health, damage, defence, location, speed):
            self.name = name
            self.description = description
            self.base_health = base_health
            self.health_points = base_health
            self.damage = damage
            self.defence = defence
            self.inventory = inventory.Inventory([])
            self.location = location
            self.speed = speed
            self.in_fight = False
            self.markers = []

        def add_to_markers(self, marker):
            self.markers.append(marker)

        def check_for_marker(self, marker):
            for i in self.markers:
                if i == marker:
                    return True
            return False

        def use_potion(self, potion):
            if (type(potion) == item.Item.Potion.HealPotion):
                # healing so add whatever percentage of health to player
                self.health_points += potion.heal_percentage * self.base_health
                self.health_points = math.ceil(self.health_points)
                # if goes over then should set it to players max hp
                if self.health_points > self.base_health:
                    self.health_points = self.base_health
                    # how much supposed to heal minus amount went over it
                    heal_amount = math.ceil(potion.heal_percentage * self.base_health) - (math.ceil(potion.heal_percentage * self.base_health) - self.base_health)
                else:
                    heal_amount = math.ceil(potion.heal_percentage * self.base_health)
                print_to_game_text("You used " + potion.name + " and healed  " + str(heal_amount))
            elif (type(potion) == item.Item.Potion.ArmourPotion):
                self.defence += potion.armour_up
                print_to_game_text("You used " + potion.name + " and added " + str(potion.armour_up) + " shields")
            elif (type(potion) == item.Item.Potion.SpeedPotion):
                self.speed += potion.speed_up
                print_to_game_text("You used " + potion.name + " and added " + str(potion.speed_up) + " speed points")
            elif (type(potion) == item.Item.Potion.StrengthPotion):
                self.damage += potion.strength_up
                print_to_game_text("You used " + potion.name + " and added " + str(potion.strength_up) + " to your damage")

    class NPC:

        def __init__(self, name, description, health_points, damage, speed, defence, fight_marker=None, talk_marker=None, talk_requirement=None, info=None, trade_desire=None, trade_offer=None, anger=False):
            self.name = name
            self.description = description
            self.health_points = health_points
            self.damage = damage
            self.speed = speed
            self.defence = defence
            self.inventory = inventory.Inventory([])
            self.fight_marker = fight_marker
            self.talk_marker = talk_marker
            self.talk_requirement = talk_requirement
            if info == None:
                self.info = "I have nothing to say to you."
            else:
                self.info = info
            self.trade_desire = trade_desire
            self.trade_offer = trade_offer
            self.anger = anger


        def wants_trade(self):
            if self.trade_desire != None and self.trade_offer != None:
                return True
            else:
                return False

        def fight_choice(self, char_weapons, char_armour, player):
            # so should take in player stats and its own stats
            # if the player is better in all stats it should just shield. if the character isnt angry then thinks rationally. otherwise if they angry they will attack.
            if player.damage > self.damage and player.health_points > self.health_points and player.speed > self.speed and self.anger == False:
                if not char_armour:
                    return False
                else:
                    biggest_armour = char_armour[0]
                    for x in char_armour:
                        if x.armour_stat > biggest_armour.armour_stat:
                            biggest_armour = x
                    return biggest_armour
            else:
                # then see if thinks will be faster, if it doesnt then it chooses fastest weapon, if does think faster then just attack
                if self.speed > player.speed:
                    if not char_weapons:
                        return True

                    else:
                        biggest_speed = char_weapons[0]
                        for x in char_weapons:
                            if x.speed_stat > biggest_speed.speed_stat:
                                biggest_speed = x
                        return biggest_speed
                else:
                    if not char_weapons:
                        return True
                    else:
                        biggest_attack = char_weapons[0]
                        for x in char_weapons:
                            if x.attack_stat > biggest_attack.attack_stat:
                                biggest_attack = x
                        return biggest_attack
