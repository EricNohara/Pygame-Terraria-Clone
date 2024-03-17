from helper.myconstants import *
from helper.items import *
from helper.events import EventHandler

class Inventory:
    def __init__(self, app, textures) -> None:
        self.app = app
        self.screen = app.screen
        self.textures = textures
        # create slots
        self.slots = []
        for _ in range(INVENTORY_SIZE):
            self.slots.append(Item())
        self.slots[0] = ShortSwordItem('shortsword', 1)
        self.active_slot = 0
        self.font = pg.font.Font(None, 30)


    def debug(self):
        for slot in self.slots:
            print(slot)

    def use(self, player, position):
        """Do check if active item is an item (not empty slot) and if so, uses the item."""
        if self.slots[self.active_slot].name != 'default':
            self.slots[self.active_slot].use(player, position)

    def add_item(self, item):
        first_available_slot = len(self.slots)  # first empty slot
        target_slot = len(self.slots)           # first slot of existing item name in inventory
        for i, slot in enumerate(self.slots):
            if slot.name == 'default' and i < first_available_slot:
                first_available_slot = i
            if slot.name == item.name:
                target_slot = i
        if target_slot < len(self.slots):
            self.slots[target_slot].quantity += items[item.name].quantity
        elif first_available_slot < len(self.slots):
            self.slots[first_available_slot] = items[item.name].item_type(item.name, items[item.name].quantity)

    def update(self):
        if EventHandler.keydown(pg.K_RIGHT):
            if self.active_slot < len(self.slots) - 1:
                self.active_slot += 1
        if EventHandler.keydown(pg.K_LEFT):
            if self.active_slot > 0:
                self.active_slot -= 1
        if EventHandler.clicked_any():
            self.debug()

    def draw(self):
        pg.draw.rect(self.screen, 'grey', pg.Rect(0, 0, SLOTSIZE * len(self.slots), SLOTSIZE))
        x_offset = TILESIZE / 2
        y_offset = TILESIZE / 2
        for i in range(len(self.slots)):
            if i == self.active_slot:
                pg.draw.rect(self.screen, 'white', pg.Rect(i * SLOTSIZE, 0, SLOTSIZE, SLOTSIZE))
            pg.draw.rect(self.screen, 'black', pg.Rect(i * SLOTSIZE, 0, SLOTSIZE, SLOTSIZE), 2)
            if self.slots[i].name != 'default':
                self.screen.blit(self.textures[self.slots[i].name], (x_offset + (TILESIZE*2)*i, y_offset))
                self.amount_text = self.font.render(str(self.slots[i].quantity), True, 'black')
                self.screen.blit(self.amount_text, (5 + (TILESIZE*2)*i, 5))

        pg.draw.rect(self.screen, 'black', pg.Rect(0, 0, SLOTSIZE * len(self.slots), SLOTSIZE), 4)