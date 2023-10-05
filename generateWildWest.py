import os
import openai
import time

# generates and saves descriptions for each class used in wild west games.
# a secret key is required to replace "OPENAI_API_KEY" to run this script. secret keys are tied to OpenAI accounts

openai.api_key = os.getenv("OPENAI_API_KEY")
promptText = 'Write, for use in a wild west set text adventure game, a generic two sentence description for a '

# 16 from first 2 lines
# 50 locations, two descriptions for each location. quarry is 40th location

desc_str = ["Fresh", "Salty", "Bitter", "Refreshing", "Tasty", "Mouldy", "Nutritious", "Sweet", "Dirt Covered", "Spicy"]
consumable_name_str = ["Beer", "Can of Beans", "Loaf of Bread", "Bacon", "Eggs", "Moonshine", "Coffee", "Potato", "Beef", "Dried Meat"]

print(len(desc_str))
print(len(consumable_name_str))


f = open("consumablesToPruneWW.txt", "a")

for x in desc_str:
    for y in consumable_name_str:
      time.sleep(1)
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



# https://wildwestrp.com/threads/a-guide-to-potential-jobs-for-wild-west-roleplayers-non-mechanic-job-suggestions.2377/


desc_str = ["Wise", "Mean", "Charming", "Grizzled", "Lone", "Tetchy", "Old", "Sly"]
occupation_str = ["Sheriff", "Marshall", "Cowboy", "Blacksmith", "Teacher", "Banker", "Bartender", "Miner",
                 "Bandit", "Baker", "Railroad Worker", "Outlaw", "Bounty Hunter", "Rancher", "Saloon Keeper",
                 "Pastor", "Shopkeeper", "Governor", "Mayor","Butcher", "Judge","Oil Baron", "Freight Hauler",
                 "Prospector", "Farmer", "Hunter", "Mountain Man","Gunsmith","Carriage Driver","Gambler",
                 "Stables Keeper", "Carpenter","Gunslinger","Doctor", "Nurse"]



f = open("charactersToPruneWW.txt", "a")


for x in desc_str:
    for y in occupation_str:
        time.sleep(1)
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



f.close()



desc_str = ["Quiet", "Lively", "Spooky", "Forgotten", "Menacing", "Misty", "Damp", "Large", "Rowdy", "Desolate",
           "Bustling", "Small", "Decadent", "Posh", "Squalid", "Guarded", "Mysterious", "Grim", "Civilized", "Gothic"
           , "Evil", "Murky", "Ornate", "Grand", "Impressive",  "Rustic", "Shadowy", "Cavernous", "Cryptic", "Dusty",
           "Ramshackle","Rugged", "Lawless", "Remote", "Time-worn", "Serene"]
locations_str = ["Inn", "Flour mill", "Gallows", "Railroad", "Saloon", "Casino", "Reservoir", "Desert", "Sand Dune",
                 "Field", "Outhouse", "Bank", "Swamp", "Windmill", "Camp","Sawmill", "Train Station", "Gulch", "Canyon",
                 "School", "Stable", "Ranch", "Homestead", "Bakery", "Valley","Reservation","Sheriff's Office", "Manor",
                 "Tannery", "Theatre", "Workshop","Refinery", "General Store", "Graveyard", "Courthouse", "Well",
                "Coal mine", "Cave", "Woods", "Mountain", "Quarry", "Tunnel", "Frontier Fort", "Boomtown", "Mining Camp",
                "Jail", "Ghost Town", "Main Street"]


print(len(desc_str))

f = open("locationsToPruneWW.txt", "a")

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



desc_str = ["Silver", "Gold", "Small", "Large", "Rusty", "Broken", "Powerful", "Sturdy", "Ornate", "Defective", "Ornate", "Prized"]
weapons_str = ["Revolver", "Rifle", "Pistol", "Gatling Gun", "Shotgun", "Bowie Knife", "Tomahawk", "Bow and Arrow", "Whip", "Axe", "Pickaxe"]

f = open("weaponsToPruneWW.txt", "a")


for x in desc_str:
    for y in weapons_str:
        time.sleep(1)
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



desc_str = ["Weathered", "Shiny", "Bejewelled", "Clean", "Dirty", "Dusty", "Sturdy", "Colourful", "Ripped", "Loose", "Too Tight"]
armor_str = ["Cowboy Hat", "Duster", "Chaps", "Bandana", "Spurs", "Boots", "Poncho", "Jeans", "Overalls", "Flannel Shirt", "Gloves"]


print(len(desc_str))
print(len(armor_str))


f = open("armorToPruneWW.txt", "a")

for x in desc_str:
    for y in armor_str:
        time.sleep(1)
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
    time.sleep(1)
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