import pygame as pg

class EventHandler:
    def __init__(self) -> None:
        EventHandler.events = pg.event.get()

    def poll_events():
        EventHandler.events = pg.event.get()

    def keydown(key):
        for event in EventHandler.events:
            if event.type == pg.KEYDOWN:
                if event.key == key:
                    return True
        return False
    
    def clicked(leftright = 1) -> bool:
        for event in EventHandler.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == leftright:
                    return True
    
    def clicked_any() -> bool:
        for event in EventHandler.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                return True
        return False
