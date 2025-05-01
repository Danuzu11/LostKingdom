"""
ISPPJ1 2024
Study Case: New Martian (Platformer)

This file contains the game settings that include the association of the
inputs with their ids, constants of values to set up the game, textures,
frames, and fonts.
"""
import pathlib

import pygame

from gale import frames
from gale import input_handler
import pytmx
import os
# from src import loaders

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_p, "pause")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_KP_ENTER, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_d, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_a, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "jump")
input_handler.InputHandler.set_mouse_click_action(input_handler.MOUSE_BUTTON_1, "jump")

pygame.mixer.init()
pygame.init()

# Dimensiones de la ventana
VIRTUAL_WIDTH = 1020
VIRTUAL_HEIGHT = 500

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

# Dimensiones de la ventana
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{WINDOW_WIDTH//4},{WINDOW_HEIGHT//4}"
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Lost Kingdom")

SCALE_FACTOR = 2

# Configuración del jugador
PLAYER_SPEED = 150
PLAYER_SPEED_JUMP = -10

# Rutas y recursos
BASE_DIR = pathlib.Path(__file__).parent

# width significa el ancho de la imagen
# height significa el alto de la imagen

# Estos son los valores de la textura del player para recortar el ancho y alto del sprite
# el ancho y alto de la textura del player
king_width = 128
king_height = 70  

 
COLLISION_WIDTH = king_width
COLLISION_HEIGHT = king_height
GRAVITY = 0.5

ANIMATIONS_DELAYS = {"run": 100, "attack": 150, "jump": 100, "idle": 200}


LEVELS = {
    "intro": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "introLevel.tmx", pixelalpha=True),
}

SOUNDS = {
    "jump": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "jump.wav"),
    "timer": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "timer.wav"),
    "count": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "count.wav"),
    "win": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.wav"),
    # "principal_theme": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "DreadMarch.wav"),
    "slash1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash1.wav"),
    "slash2": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash2.wav"),
    "principal_theme": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "EclipsedDesolation.wav"),
}

# Generar textura del spritesheet
TEXTURES = {
    "kingRun": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingRun.png"),
    "kingAttack": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingAttacks.png"),
    "kingJump": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingJump.png"),
    "idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "idle.png"),
    "fireplace": pygame.image.load(BASE_DIR / "assets" / "textures" / "fireplace.png"),
    "torch": pygame.image.load(BASE_DIR / "assets" / "textures" / "torch.png"),
    "background_layer_1": pygame.image.load(BASE_DIR / "assets" / "textures" / "background_layer_1.png"),
}

# Generar frames del sprite
FRAMES = {
    "kingRun":  frames.generate_frames(TEXTURES["kingRun"], king_width - 2, king_height - 6),        
    "kingAttack": frames.generate_frames(TEXTURES["kingAttack"], king_width , king_height - 6),
    "kingJump": frames.generate_frames(TEXTURES["kingJump"], king_width, king_height - 6),
    "idle": frames.generate_frames(TEXTURES["idle"], king_width , king_height - 6),
    "fireplace": frames.generate_frames(TEXTURES["fireplace"], 64, 64),
    "torch": frames.generate_frames(TEXTURES["torch"], 64, 64),
}

ANIMATED_DECORATIONS = {
    "fireplace" : {
        "texture" : TEXTURES["fireplace"] ,
        "frames" : FRAMES["fireplace"] 
    },
    "torch" : {
        "texture" : TEXTURES["torch"] ,
        "frames" : FRAMES["torch"]   
    }
    
}

# Inicializar fuentes
pygame.font.init()
FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 8),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
} 