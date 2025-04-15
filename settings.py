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

# Dimensiones de la ventana
VIRTUAL_WIDTH = 1020
VIRTUAL_HEIGHT = 740
WINDOW_WIDTH = VIRTUAL_WIDTH 
WINDOW_HEIGHT = VIRTUAL_HEIGHT 

SCALE_FACTOR = 2

# Configuración del jugador
PLAYER_SPEED = 150

# Rutas y recursos
BASE_DIR = pathlib.Path(__file__).parent

# width significa el ancho de la imagen
# height significa el alto de la imagen

king_width = 128
king_height = 70   

COLLISION_WIDTH = king_width
COLLISION_HEIGHT = 70

# king_width_attack = 130
# king_height_attack = 70

# scaled_surface = pygame.transform.scale(surface, (frame_king.width * 2, frame_king.height * 2))
# Cargar texturas

SOUNDS = {
    "jump": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "jump.wav"),
    "timer": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "timer.wav"),
    "count": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "count.wav"),
    "win": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.wav"),
    "principal_theme": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "DreadMarch.wav"),
    "slash1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash1.wav"),
    "slash2": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash2.wav"),
}

TEXTURES = {
    "martian": pygame.image.load(BASE_DIR / "assets" / "textures" / "martian.png"),
    "kingRun": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingRun.png"),
    "kingAttack": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingAttacks.png"),
    "kingJump": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingJump.png"),
}

# Generar frames del sprite
FRAMES = {
    "martian": frames.generate_frames(TEXTURES["martian"], 16, 20), 
    "kingRun": frames.generate_frames(TEXTURES["kingRun"], king_width - 2, king_height),        
    "kingAttack": frames.generate_frames(TEXTURES["kingAttack"], king_width , king_height),
    "kingJump": frames.generate_frames(TEXTURES["kingJump"], king_width, king_height),
}

# Inicializar fuentes
pygame.font.init()
FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 8),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
} 