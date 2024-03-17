from helper.myconstants import *
from helper.sprite import *

class Item:
    """Do create generic item class with name and quantity fields."""
    def __init__(self, name: str = "default", quantity: int = 0) -> None:
        self.name = name
        self.quantity = quantity

    def use(self, *args, **kwargs):
        """This is a default use class inherited by all sub item classes."""
        pass

    def attack(self, *args, **kwargs):
        pass

    def __str__(self):
        """This is a dunder method used for debugging inventory purposes."""
        return f'Name: {self.name}, Quantity: {self.quantity}'

class BlockItem(Item):
    """Do create placeable item class (block)."""
    def __init__(self, name: str, quantity: int = 0) -> None:
        super().__init__(name, quantity)
    
    def use(self, player, position: tuple):
        """Do handle block placing."""
        if self.quantity > 0:
            items[self.name].use_type([player.group_list[group] for group in items[self.name].groups], player.textures[self.name], position, self.name)
            self.quantity -= 1
            if self.quantity <= 0:
                self.name = 'default'
        else:
            self.name = 'default'

class ShortSwordItem(Item):
    def __init__(self, name: str = "default", quantity: int = 0) -> None:
        super().__init__(name, quantity)
    
    def use(self, player, position):
        print('Using short sword')

    def attack(self, player, target):
        target.kill()

class ItemData():
    """Do create class to store item data."""
    def __init__(self, name: str, quantity: int = 1, groups: list[str] = ['sprites', 'block_group'], use_type: Entity = Entity, item_type: Item = Item) -> None:
        self.name = name
        self.quantity = quantity
        self.groups = groups
        self.use_type = use_type
        self.item_type = item_type

items: dict[str, ItemData] = {
    'grass': ItemData('grass', item_type=BlockItem),
    'stone': ItemData('stone', item_type=BlockItem),
    'dirt': ItemData('dirt', item_type=BlockItem),
    'grassdirt': ItemData('grassdirt', item_type=BlockItem),
    'cobblestone': ItemData('cobblestone', item_type=BlockItem),
    'crackedstone': ItemData('crackedstone', item_type=BlockItem),
    'copperore': ItemData('copperore', item_type=BlockItem),
    'silverore': ItemData('silverore', item_type=BlockItem),
    'coalore': ItemData('coalore', item_type=BlockItem),
    'platinumore': ItemData('platinumore', item_type=BlockItem),
    'rubyore': ItemData('rubyore', item_type=BlockItem),
    'saphireore': ItemData('saphireore', item_type=BlockItem),
    'emeraldore': ItemData('emeraldore', item_type=BlockItem),

    'shortsword': ItemData('shortsword', item_type=ShortSwordItem),
}