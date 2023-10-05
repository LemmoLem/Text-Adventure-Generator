import os
import openai
import time

# generates and saves information text used in wild west games. the nouns are gathered from generate wild west script.
# a secret key is required to replace "OPENAI_API_KEY" to run this script. secret keys are tied to OpenAI accounts
openai.api_key = os.getenv("OPENAI_API_KEY")

# got rid of s in s" ending ones as would add an extra s to words when wanting to make them plural
nouns = []
consumable_name_str = ["Beer", "Can of Bean", "Loaf of Bread", "Bacon", "Egg", "Moonshine", "Coffee", "Potato", "Beef", "Dried Meat"]
occupation_str = ["Sheriff", "Marshall", "Cowboy", "Blacksmith", "Teacher", "Banker", "Bartender", "Miner",
                 "Bandit", "Baker", "Railroad Worker", "Outlaw", "Bounty Hunter", "Rancher", "Saloon Keeper",
                 "Pastor", "Shopkeeper", "Governor", "Mayor","Butcher", "Judge","Oil Baron", "Freight Hauler",
                 "Prospector", "Farmer", "Hunter", "Mountain Man","Gunsmith","Carriage Driver","Gambler",
                 "Stables Keeper", "Carpenter","Gunslinger","Doctor", "Nurse"]
locations_str = ["Inn", "Flour mill", "Gallow", "Railroad", "Saloon", "Casino", "Reservoir", "Desert", "Sand Dune",
                 "Field", "Outhouse", "Bank", "Swamp", "Windmill", "Camp","Sawmill", "Train Station", "Gulch", "Canyon",
                 "School", "Stable", "Ranch", "Homestead", "Bakery", "Valley","Reservation","Sheriff's Office", "Manor",
                 "Tannery", "Theatre", "Workshop","Refinery", "General Store", "Graveyard", "Courthouse", "Well",
                "Coal mine", "Cave", "Wood", "Mountain", "Quarry", "Tunnel", "Frontier Fort", "Boomtown", "Mining Camp",
                "Jail", "Ghost Town", "Main Street"]
weapons_str = ["Revolver", "Rifle", "Pistol", "Gatling Gun", "Shotgun", "Bowie Knife", "Tomahawk", "Bow and Arrow", "Whip", "Axe", "Pickaxe"]
armor_str = ["Cowboy Hat", "Duster", "Chap", "Bandana", "Spur", "Boot", "Poncho", "Jean", "Overall", "Flannel Shirt", "Glove"]

opinions = ["Positive", "Negative","Hateful","Loving","Neutral","Funny","Bitter","Condemning", "Passionate","Doubtful",
            "Snobbish","Appreciative","Sensitive", "Shocked", "Cynical", "Mesmerized","Arrogant","Jealous"]

nouns.extend(consumable_name_str)
nouns.extend(occupation_str)
nouns.extend(locations_str)
nouns.extend(weapons_str)
nouns.extend(armor_str)

f = open("infosToPruneWW.txt", "a")

x = 0
for n in range(3):
    for y in nouns:
        time.sleep(1)
        text = 'write, for use in a wild west set text adventure game, a two sentence personal '+ opinions[x].lower() + ' opinion of ' +y.lower() +'s.'
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
