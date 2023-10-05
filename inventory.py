import item

# class for characters inventories.
# inventories are a list of items and there are methods to get the best stat from a weapon/armour object in the inventory
class Inventory:
    def __init__(self, items=None):
        if items is None:
            items = []
        self.items = items

    def addToInventory(self, item):
        if (self.items == []):
            self.items = [item]
        else:
            self.items.extend([item])

    def removeFromInventory(self, item):
        self.items.remove(item)

    def __str__(self):
        outputStr = ""
        # make so options are numbered and so that player can choose number
        for x in self.items:
            num = self.items.index(x) +1
            outputStr += str(num) + ": " + x.name + " "
        return str(outputStr)

    def getItems(self):
        return self.items
    def getWeapon(self):
        for x in self.items:
            if type(x) == item.Item.Weapon:
                return x
        return None

    def getWeaponsAndArmour(self):
        weapons = []
        armour = []
        for x in self.items:
            if type(x) == item.Item.Weapon:
                weapons.append(x)
            if type(x) == item.Item.Armour:
                armour.append(x)
        return weapons, armour
    def getBiggestDamageWeapon(self):
        weapons, armour = self.getWeaponsAndArmour()
        if not weapons:
            return False
        else:
            biggestDamage = weapons[0]
            for x in weapons:
                if x.attack_stat > biggestDamage.attack_stat:
                    biggestDamage = x
            return biggestDamage

    def getArmour(self):
        for x in self.items:
            if type(x) == item.Item.Armour:
                return x
        return None