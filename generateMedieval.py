import os
import openai
import time

# generates and saves descriptions for each class used in medieval games.
# a secret key is required to replace "OPENAI_API_KEY" to run this script. secret keys are tied to OpenAI accounts

openai.api_key = os.getenv("OPENAI_API_KEY")
promptText = 'Write, for use in a medieval set text adventure game, a generic two sentence description for a '


desc_str = ["Enchanted", "Magical", "Mysterious", "Bewitched", "Mystical", "Occult", "Special", "Possessed", "Other-worldly", "Demonic"]
consumable_name_str = ["Potion", "Cake", "Loaf of Bread", "Elixir", "Brew", "Tonic", "Concoction", "Tincture", "Essence", "Beer"]

print(len(desc_str))
print(len(consumable_name_str))


f = open("consumablesToPrune.txt", "a")

for x in desc_str:
    time.sleep(3)
    for y in consumable_name_str:
      text = promptText + x.lower() + " " + y.lower() + "."
      response = openai.Completion.create(
        model="text-babbage-001",
        prompt=text,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
      stripped = response["choices"][0]["text"].strip('\n')
      print(x + " " + y + "@" + stripped)
      f.write(x + " " + y + "@" + stripped + "\n")

for y in consumable_name_str:
    time.sleep(1)
    text = promptText + y.lower()+ "."
    response = openai.Completion.create(
        model="text-babbage-001",
        prompt=text,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
    stripped = response["choices"][0]["text"].strip('\n')
    print(y + "@" + stripped)
    f.write(y + "@" + stripped + "\n")
f.close()





desc_str = ["Wise", "Mean", "Charming"]
occupation_str = ["Miller", "Blacksmith", "Stonemason", "Armorer", "Minstrel", "Carpenter", "Weaver", "Watchman",
                 "Thatcher", "Baker", "Highway man", "Knight", "Prince", "Prisoner", "Farmer",
                 "Fisherman", "Monk", "Nun", "Apothecary","Butcher", "Merchant","Witch", "Court jester"]
race_str = ["Wizard", "Ork", "Ogre", "Goblin", "Troll", "Dragon", "Dwarf", "Elf", "Giant", "Mermaid", "Gnome",
                "Nymph", "Dryad", "Satyr", "Centaur", "Demon", "Imp", "Werewolf", "Banshee", "Golem", "Sphinx", "Fairy",
           "Human"]


f = open("charactersToPrune.txt", "a")


for x in desc_str:
    for y in occupation_str:
        time.sleep(0.8)
        text = promptText + x.lower() + " " +y.lower() +"."
        response = openai.Completion.create(
            model="text-babbage-001",
            prompt=text,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        stripped = response["choices"][0]["text"].strip('\n')
        print(x + " " + y + "@" + stripped)
        f.write(x + " " + y + "@" + stripped + "\n")
    time.sleep(3)
    for z in race_str:
        text = promptText + x.lower() + " "+ z.lower()+"."
        response = openai.Completion.create(
            model="text-babbage-001",
            prompt=text,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        stripped = response["choices"][0]["text"].strip('\n')
        print(x + " " + z + "@" + stripped)
        f.write(x + " " + z + "@" + stripped + "\n")

for x in occupation_str:
    time.sleep(1)
    text = promptText + x.lower() + "."
    response = openai.Completion.create(
        model="text-babbage-001",
        prompt=text,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    stripped = response["choices"][0]["text"].strip('\n')
    print(x + "@" + stripped)
    f.write(x + "@" + stripped + "\n")

for x in race_str:
    time.sleep(1)
    text = promptText + x.lower() + "."
    response = openai.Completion.create(
        model="text-babbage-001",
        prompt=text,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    stripped = response["choices"][0]["text"].strip('\n')
    print(x + "@" + stripped)
    f.write(x + "@" + stripped + "\n")


f.close()



desc_str = ["Quiet", "Lively", "Spooky", "Forgotten", "Menacing", "Misty", "Damp", "Majestic", "Magical", "Large",
           "Small", "Decadent", "Posh", "Squalid", "Royal", "Guarded", "Mysterious", "Grim", "Civilized", "Gothic"
           , "Evil", "Murky", "Enchanting", "Ornate", "Grand", "Impressive", "Dreamlike", "Ethereal", "Rustic"
           , "Shadowy", "Cavernous", "Cryptic", "Ephemeral"]
locations_str = ["Castle", "Townhouse", "Inn", "Bazaar", "Crypt", "Dock house", "Flour mill", "Gallows", "Gatehouse",
                "Haberdashery", "Longhouse", "Tailor", "Monastery", "Field", "Outhouse", "Pavilion",
                "Philosopher's forum", "Plaza", "Plague pit", "Prison", "Public baths", "School", "Shrine", "Stable",
                "Stonemason", "Tannery", "Theatre", "Workshop", "Town hall", "Tower", "Abbey", "Stockade","Refinery"
                ,"Coal mine", "Dungeon", "Canal", "Cave", "Woods", "Mountain", "Quarry", "Underworld", "Witch's hut"
                ,"Moor", "Ork workshop", "Ogre's bridge", "Tunnel", "Beach", "Elf fortress", "Dwarf inn", "Dragon's lair"]


print(len(desc_str))

f = open("locationsToPrune.txt", "a")

x = 0
for n in range(3):
    for y in locations_str:
        time.sleep(1)
        text = promptText + desc_str[x].lower() + " " + y.lower() + "."
        response = openai.Completion.create(
            model="text-babbage-001",
            prompt=text,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        stripped = response["choices"][0]["text"].strip('\n')
        print(desc_str[x] + " " + y + "@" + stripped)
        f.write(desc_str[x] + " " + y + "@" + stripped + "\n")
        x+=1
        if x == len(desc_str):
            x = 0

f.close()



desc_str = ["Bronze", "Silver", "Gold", "Wooden", "Small", "Dual-wield", "Large", "Two-handed", "Rusty", "Broken"]
weapons_str = ["Sword", "Axe", "Hatchet", "Knife", "Mace", "Rapier", "Spear", "Dagger", "Longsword"]

f = open("weaponsToPrune.txt", "a")


for x in desc_str:
    time.sleep(3)
    for y in weapons_str:
        text = promptText + x.lower() + " " + y.lower() + "."
        response = openai.Completion.create(
            model="text-babbage-001",
            prompt=text,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        stripped = response["choices"][0]["text"].strip('\n')
        print(x+" "+ y + "@" + stripped)
        f.write(x+" "+ y + "@" + stripped+"\n")

f.close()



desc_str = ["Golden", "Iron", "Wooden", "Bronze", "Diamond", "Weathered", "Shiny", "Bejewelled", "Rusty", "Broken"]
armor_str = ["Shield", "Suit of Armour", "Chainmail Vest", "Helmet", "Gambeson", "Gloves", "Coat of Plates", "Scale Armour"]


print(len(desc_str))
print(len(armor_str))


f = open("armorToPrune.txt", "a")

for x in desc_str:
    time.sleep(3)
    for y in armor_str:
        text = promptText + x.lower()+" "+y.lower()+"."
        response = openai.Completion.create(
            model="text-babbage-001",
            prompt=text,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        stripped = response["choices"][0]["text"].strip('\n')
        print(x + " " + y + "@" + stripped)
        f.write(x + " " + y + "@" + stripped + "\n")

for y in armor_str:
    time.sleep(3)
    text = promptText + y.lower()+"."
    response = openai.Completion.create(
        model="text-babbage-001",
        prompt=text,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    stripped = response["choices"][0]["text"].strip('\n')
    print(y + "@" + stripped)
    f.write(y + "@" + stripped + "\n")
f.close()
