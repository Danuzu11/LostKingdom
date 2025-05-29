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

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_KP_ENTER, "enter")

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_d, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_a, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "jump")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_x, "x")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_p, "pause")
pygame.mixer.init()
pygame.init()

# Dimensiones de la ventana
VIRTUAL_WIDTH = 1020
VIRTUAL_HEIGHT = 500

WINDOW_WIDTH = 1020
WINDOW_HEIGHT = 500

# Dimensiones de la ventana
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{WINDOW_WIDTH//4},{WINDOW_HEIGHT//4}"
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Lost Kingdom")



# Rutas y recursos
BASE_DIR = pathlib.Path(__file__).parent

# width significa el ancho de la imagen
# height significa el alto de la imagen

# Estos son los valores de la textura del player para recortar el ancho y alto del sprite
# el ancho y alto de la textura del player
SCALE_FACTOR = 2

# Configuración del jugador
PLAYER_SPEED = 150
PLAYER_SPEED_JUMP = -10

king_width = 128
king_height = 70  

enemy1_width = 80
enemy1_height = 80
 
COLLISION_WIDTH = king_width
COLLISION_HEIGHT = king_height
GRAVITY = 0.5

ANIMATIONS_DELAYS = {
    "run": 100, 
    "attack": 350, 
    "jump": 300, 
    "idle": 90
}


LEVELS = {
    # "intro1": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "introLevel.tmx", pixelalpha=True),
    "intro": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "levelTest.tmx", pixelalpha=True),
    "roomboss": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "roomboss.tmx", pixelalpha=True),
}

SOUNDS = {
    "jump": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "jump.wav"),
    "timer": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "timer.wav"),
    "count": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "count.wav"),
    "win": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.wav"),
    # "principal_theme": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "DreadMarch.wav"),
    "slash1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash1.wav"),
    "slash2": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash2.wav"),
    "principal_theme1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "EclipsedDesolation.wav"),
    "menu_theme1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "CursedCitadel(Intro).wav"),
    "principal_theme": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "smoothMedieval.mp3"),
}

# Generar textura del spritesheet
TEXTURES = {
    "kingRun": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingRun.png"),
    "kingAttack": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingAttacks.png"),
    "kingJump": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingJump.png"),
    "idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "idle.png"),
    
    
    "enemyAnimations": pygame.image.load(BASE_DIR / "assets" / "textures" / "NightBorne.png"),
    
    "fireplace": pygame.image.load(BASE_DIR / "assets" / "textures" / "fireplace.png"),
    "torch": pygame.image.load(BASE_DIR / "assets" / "textures" / "torch.png"),
    "castleTorch": pygame.image.load(BASE_DIR / "assets" / "textures" / "torch_big" / "castleTorch.png"),
    
    
    #"menu": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "menu.png"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "menu": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "slayer.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "death2": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "death2.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
}


# Generar textura del spritesheet
COMPLEX_TEXTURES = {
    "Player":{
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingRun.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingAttacks.png"),
        "Jump": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingJump.png"),
    },
    
    "NightBorne":{
        "NightBorne": pygame.image.load(BASE_DIR / "assets" / "textures" / "NightBorne.png"),
    },
    
    "Minotaur":{ 
        "Minotaur": pygame.image.load(BASE_DIR / "assets" / "textures" / "minotaur" / "minotaur.png"),
    },
    
    "Golem":{
        "Idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "Golem" /"Golem_IdleB.png"),
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "Golem" /"Golem_Run.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "Golem" / "Golem_AttackC.png"),
    },
  
}

# AQUI MANEJAMOS EL ANALISIS PARA ENEMIGOS Y JUGADORES PERO UN POQUITO MAS COMPLEJO
# YA QUE QUEREMOS QUE PUEDA ANALIZAR TODO UN SPRITESHEET DE TODOS LOS MOVIMIENTOS
# O UN SPTRITESHEET DE UN SOLO MOVIMIENTO , COMO POR EJEMPLO EL DE PLAYER

COMPLEX_FRAMES = {
    "Player":{
        "Run":  frames.generate_frames(TEXTURES["kingRun"], king_width , king_height - 6),        
        "Attack": frames.generate_frames(TEXTURES["kingAttack"], king_width , king_height - 6),
        "Jump": frames.generate_frames(TEXTURES["kingJump"], king_width, king_height - 6),
    },
    
    "NightBorne":{
        "NightBorne": frames.generate_frames(COMPLEX_TEXTURES["NightBorne"]["NightBorne"], enemy1_width, enemy1_height),
    },
    
    "Minotaur":{
        "Minotaur": frames.generate_frames(COMPLEX_TEXTURES["Minotaur"]["Minotaur"], 288 , 160),
    },
        
    "Golem":{
        "Idle":  frames.generate_frames(COMPLEX_TEXTURES["Golem"]["Idle"], 64 , 64),  
        "Run":  frames.generate_frames(COMPLEX_TEXTURES["Golem"]["Run"], 64 , 64),        
        "Attack": frames.generate_frames(COMPLEX_TEXTURES["Golem"]["Attack"], 64 , 64),
    },
    
}

# Generar frames del sprite
FRAMES = {
    "kingRun":  frames.generate_frames(TEXTURES["kingRun"], king_width , king_height - 6),        
    "kingAttack": frames.generate_frames(TEXTURES["kingAttack"], king_width , king_height - 6),
    "kingJump": frames.generate_frames(TEXTURES["kingJump"], king_width, king_height - 6),
    
    "enemyAnimations": frames.generate_frames(TEXTURES["enemyAnimations"], enemy1_width, enemy1_height),
    
    "idle": frames.generate_frames(TEXTURES["idle"], king_width , king_height - 6),
    "fireplace": frames.generate_frames(TEXTURES["fireplace"], 64, 64),
    "torch": frames.generate_frames(TEXTURES["torch"], 64, 64),  
    "castleTorch": frames.generate_frames(TEXTURES["castleTorch"], 12, 42),
    
}



ANIMATIONS_ENEMY_DELAYS = {
    "NightBorne": {
        "idle": 80,
        "run": 80,
        "attack": 50,
    },
    "Golem": {
        "idle": 80,
        "run": 80,
        "attack": 50,
    },
    "Minotaur": {
        "idle": 100,
        "run": 100,
        "attack": 150,
    },
}


ENEMY_SPEED = 100

ANIMATED_DECORATIONS = {
    "fireplace" : {
        "texture" : TEXTURES["fireplace"] ,
        "frames" : FRAMES["fireplace"] ,
        "correctionX" : 0,
        "correctionY" : 60,
    },
    "torch" : {
        "texture" : TEXTURES["torch"] ,
        "frames" : FRAMES["torch"]   ,
        "correctionX" : 0,
        "correctionY" : 0,
    },
    "castleTorch" : {
        "texture" : TEXTURES["castleTorch"] ,
        "frames" : FRAMES["castleTorch"] ,
        "correctionX" : 5,
        "correctionY" : 40,  
    }
    
}



# Inicializar fuentes
pygame.font.init()
FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 8),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
} 