import os
import openai
import time

# generates and saves information text used in medieval games. the nouns are gathered from generate medieval script.
# a secret key is required to replace "OPENAI_API_KEY" to run this script. secret keys are tied to OpenAI accounts
openai.api_key = os.getenv("OPENAI_API_KEY")

# got rid of s in s" ending ones as would add an extra s to words when wanting to make them plural
nouns = []
consumable_name_str = ["Potion", "Cake", "Loaf of Bread", "Elixir", "Brew", "Tonic", "Concoction", "Tincture", "Essence", "Beer"]
armor_str = ["Shield", "Suit of Armour", "Chainmail Vest", "Helmet", "Gambeson", "Glove", "Coat of Plate", "Scale Armour"]
occupation_str = ["Miller", "Blacksmith", "Stonemason", "Armorer", "Minstrel", "Carpenter", "Weaver", "Watchman",
                 "Thatcher", "Baker", "Highway man", "Knight", "Prince", "Prisoner", "Farmer",
                 "Fisherman", "Monk", "Nun", "Apothecary","Butcher", "Merchant","Witch", "Court jester"]
race_str = ["Wizard", "Ork", "Ogre", "Goblin", "Troll", "Dragon", "Dwarf", "Elf", "Giant", "Mermaid", "Gnome",
                "Nymph", "Dryad", "Satyr", "Centaur", "Demon", "Imp", "Werewolf", "Banshee", "Golem", "Sphinx", "Fairy",
           "Human"]
locations_str = ["Castle", "Townhouse", "Inn", "Bazaar", "Crypt", "Dock house", "Flour mill", "Gallow", "Gatehouse",
                "Haberdashery", "Longhouse", "Tailor", "Monastery", "Field", "Outhouse", "Pavilion",
                "Philosopher's forum", "Plaza", "Plague pit", "Prison", "Public bath", "School", "Shrine", "Stable",
                "Stonemason", "Tannery", "Theatre", "Workshop", "Town hall", "Tower", "Abbey", "Stockade","Refinery"
                ,"Coal mine", "Dungeon", "Canal", "Cave", "Wood", "Mountain", "Quarry", "Underworld", "Witch's hut"
                ,"Moor", "Ork workshop", "Ogre's bridge", "Tunnel", "Beach", "Elf fortress", "Dwarf inn", "Dragon's lair"]
weaponsStr = ["Sword", "Axe", "Hatchet","Knife","Mace","Rapier","Spear","Dagger","Longsword"]
nouns.extend(consumable_name_str)
nouns.extend(armor_str)
nouns.extend(occupation_str)
nouns.extend(race_str)
nouns.extend(locations_str)
opinions = ["Positive", "Negative","Hateful","Loving","Neutral","Funny","Bitter","Condemning", "Passionate","Doubtful",
            "Snobbish","Appreciative","Sensitive", "Shocked", "Cynical", "Mesmerized","Arrogant","Jealous"]


f = open("infosToPrune.txt", "a")

x = 0
for n in range(3):
    for y in nouns:
        time.sleep(0.8)
        text = 'write, for use in a medieval set text adventure game, a two sentence personal '+ opinions[x].lower() + ' opinion of ' +y.lower() +'s.'
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=text,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        stripped = response["choices"][0]["text"].strip('\n')
        print(opinions[x] + " " + y + "@" + stripped)
        f.write(opinions[x] + " " + y + "@" + stripped + "\n")
        x += 1
        if x == len(opinions):
            x = 0

f.close()
