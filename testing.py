import copy

import game
import character
import choice
import item
import inventory
# test file
# tests performed for generating games and fight interaction

# build games
game_size = 0
number = 0
do_generate = True
if do_generate:
    for seed in range(20):
        for goal in range(0,5):
            for game_size in range(20, 80):
                for setting in range(0,1):
                    gen_game = game.Game(seed, goal, game_size, setting)
                    number += 1
                    print(number)

# player and character have equal stats. player has bare fists tho which is extra attack
game = game.Game(0,0,0,0)
player = character.Character.Player("lem",None,8,8,8,None,8)
enemy = character.Character.NPC("same stats", None, 8, 8, 8, 8)
game.spawn_player(player)
player.location.add_characters([enemy])
choice1 = choice.Choice(player,game)
choice1.fight(enemy)

# player has worse stats
player = character.Character.Player("lem",None,2,2,2,None,2)
enemy = character.Character.NPC("worse stats", None, 8, 8, 8, 8)
game.spawn_player(player)
player.location.add_characters([enemy])
choice1 = choice.Choice(player,game)
choice1.fight(enemy)

# player has better stats so npc blocks and counters but cant break thru player defense
player = character.Character.Player("lem",None,5,5,5,None,5)
enemy = character.Character.NPC("blocks but not strong enough to counter", None, 2, 2, 2, 2)
enemy.inventory.addToInventory(item.Item.Armour("shield","is a shield",9,-4,6))
game.spawn_player(player)
player.location.add_characters([enemy])
choice1 = choice.Choice(player,game)
choice1.fight(enemy)

# player has better stats so npc blocks and counters with weapon
player = character.Character.Player("lem",None,5,5,5,None,5)
enemy = character.Character.NPC("blocks and counters", None, 2, 2, 2, 2)
enemy.inventory.addToInventory(item.Item.Armour("shield","is a shield",9,-4,6))
enemy.inventory.addToInventory(item.Item.Weapon("sword","is a sword",9,-4))
game.spawn_player(player)
player.location.add_characters([enemy])
choice1 = choice.Choice(player,game)
choice1.fight(enemy)

# player has no location to run to as angry ppl in others
player = character.Character.Player("lem",None,5,5,5,None,5)
enemy = character.Character.NPC("dont run", "desc", 2, 2, 2, 2, anger=True)
game.spawn_player(player)
player.location.add_characters([enemy])
for loc in player.location.linked_locations:
    loc.add_characters([copy.deepcopy(enemy)])
choice1 = choice.Choice(player,game)
while player.health_points > 0:
    choice1.make_choice()

