import pygame as pg
from helper.myconstants import *

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
                
    def double_clicked(last_a_click, last_d_click):
        for event in EventHandler.events:
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                last_clicked = pg.time.get_ticks()
                if last_a_click != 0 and last_clicked - last_a_click < DASH_DOUBLE_CLICK:
                    return 'left', last_a_click, last_d_click
                last_a_click = last_clicked
            elif event.type == pg.KEYDOWN and event.key == pg.K_d:
                last_clicked = pg.time.get_ticks()
                if last_d_click != 0 and last_clicked - last_d_click < DASH_DOUBLE_CLICK:
                    return 'right', last_a_click, last_d_click
                last_d_click = last_clicked
        return 'None', last_a_click, last_d_click
    
    def scrolled():
        for event in EventHandler.events:
            if event.type == pg.MOUSEWHEEL:
                if event.y == 1:
                    return 'up'
                elif event.y == -1:
                    return 'down'
        return 'None'
    
    def clicked_any() -> bool:
        for event in EventHandler.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                return True
        return False
