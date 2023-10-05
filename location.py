# location class is for building a map.
# players move between locations, and locations contain characters and items

class Location:
    # characters and items need to be i.e. [] or [sword]
    def __init__(self, name, description, requirement=None, linked_locations = None, marker=None, characters=None, items=None):
        self.name = name
        self.description = description
        self.linked_locations = linked_locations
        self.requirement = requirement
        self.marker = marker
        self.characters = characters
        self.items = items
        if linked_locations == None:
            self.linked_locations = []
        if characters == None:
            self.characters = []
        if items == None:
            self.items = []

    def add_items(self, items):
        self.items.extend(items)

    def add_characters(self, characters):
        self.characters.extend(characters)
    def remove_character(self, character):
        self.characters.remove(character)
    def remove_item(self, item):
        self.characters.remove(item)
    def add_linked_locations(self, locations):
        self.linked_locations.extend(locations)