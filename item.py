# item class is made up of potions, weapons and armour. these have associated stats

class Item:
    # items will belong to a characters inventory
    # they can improve player stats
    # potions will need to be called on their own, so for make choice there will be function to look in inventory
    # and then player can inspect everything in the inventory and use a potion
    class Weapon:
        def __init__(self, name, description, attack_stat, speed_stat, marker=None):
            self.name = name
            self.description = description + " Attack: " + str(attack_stat) + " Speed: " + str(speed_stat)
            self.attack_stat = attack_stat
            self.speed_stat = speed_stat
            self.is_useable = False
            self.marker = marker

        def get_stats_string(self):
            text = "Attack: " + str(self.attack_stat) + " Speed: " + str(self.speed_stat)
            return text
    class Key:
        def __init__(self, name, description, marker):
            self.name = name
            self.description = description
            self.is_useable = False
            self.marker = marker
    class Potion:
        class HealPotion:
            # heal potion should be of values like 0.34, 0.7
            def __init__(self, name, description, heal_percentage, marker=None):
                self.name = name
                self.description = description + " HealPercentage: " + str(heal_percentage * 100) + "%"
                self.heal_percentage = heal_percentage
                self.is_useable = True
                self.marker = marker
        class StrengthPotion:
            def __init__(self, name, description, strength_up, marker=None):
                self.name = name
                self.description = description + " Strength: "+ str(strength_up)
                self.strength_up = strength_up
                self.is_useable = True
                self.marker = marker
        class SpeedPotion:
            def __init__(self, name, description, speed_up, marker=None):
                self.name = name
                self.description = description + " Speed: "+ str(speed_up)
                self.speed_up = speed_up
                self.is_useable = True
                self.marker = marker
        class ArmourPotion:
            def __init__(self, name, description, armour_up, marker=None):
                self.name = name
                self.description = description + " Armour: "+ str(armour_up)
                self.armour_up = armour_up
                self.is_useable = True
                self.marker = marker

    class Armour:
        def __init__(self, name, description, armour_stat, speed_stat, passive_armour, marker=None):
            self.name = name
            self.description = description + " Armour: " + str(armour_stat) + " Passive Armour: " + str(passive_armour)
            self.armour_stat = armour_stat
            self.speed_stat = speed_stat
            self.is_useable = False
            self.marker = marker
            self.passive_armour = passive_armour

        def get_stats_string(self):
            text = "Armour: " + str(self.armour_stat) + " Speed: " + str(self.speed_stat) + " Passive Armour: " + str(self.passive_armour)
            return text
