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
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_f, "f")

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
SCALE_FACTOR = 1.3

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
    "attack": 400, 
    "jump": 300, 
    "idle": 120,
    "death": 400,
}


LEVELS = {
    # "intro1": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "introLevel.tmx", pixelalpha=True),
    "intro": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "levelTest.tmx", pixelalpha=True),
    "level1": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "levelCastle.tmx", pixelalpha=True),
    "roomboss": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "roomboss.tmx", pixelalpha=True),
}

SOUNDS = {
    # Sonidos de efectos
    "jump": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "jump.wav"),
    "timer": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "timer.wav"),
    "count": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "count.wav"),
    "win": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.wav"),
    "deepgrowl": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "deepgrowl.mp3"),  
    "boss": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "boss.mp3"),  
    "player_death": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "player_death.mp3"),  
    "outro": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "outro.mp3"),  
    
    # Sonidos de ataques 
    "slash1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash1.wav"),
    "slash2": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash2.wav"),
    
    # Temas de fondo
    "principal_theme1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "EclipsedDesolation.wav"),
    "menu_theme1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "CursedCitadel(Intro).wav"),
    "principal_theme": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "smoothMedieval.mp3"),
    "maquinaescribir": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "maquinaescribir.mp3"),
}

DEATH_SOUNDS = {
    "Golem": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "rockDeath.mp3"),
    "MechaGolem": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "rockDeath.mp3"),
    "Executoner": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "parcDead.mp3"),
    "NightBorne": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "nigthtsDead.mp3"),
    "Minotaur": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "demonLaugh.mp3"),
}

# Generar textura del spritesheet
TEXTURES = {

    # TEXTURES para el jugador
    "kingRun": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingRun.png"),
    "kingAttack": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingAttacks.png"),
    "kingJump": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingJump.png"),
    "idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "idle.png"),
    
    # TEXTURES para muerte
    "death": pygame.image.load(BASE_DIR / "assets" / "textures" / "deathAnimation" /"death.png"),
    
    # Frames para objetos animados
    "fireplace": pygame.image.load(BASE_DIR / "assets" / "textures" / "fireplace.png"),
    "torch": pygame.image.load(BASE_DIR / "assets" / "textures" / "torch.png"),
    "castleTorch": pygame.image.load(BASE_DIR / "assets" / "textures" / "torch_big" / "castleTorch.png"),
    "castleTorch1": pygame.image.load(BASE_DIR / "assets" / "textures" / "torch_big_blue" / "castleTorchBlue.png"),
    "key": pygame.image.load(BASE_DIR / "assets" / "textures" / "KeyIcons.png"),
    
    # TEXTURES para las pantallas de menu, death y intro
    "menu": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "slayer.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "death2": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "death2.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "intro2": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "intro2.png"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "outro": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "outro2.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
}


# Generar textura del spritesheet
COMPLEX_TEXTURES = {
    "Player":{
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingRun.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingAttacks.png"),
        "Jump": pygame.image.load(BASE_DIR / "assets" / "textures" / "kingJump.png"),
    },

    "Death":{
        "Death": pygame.image.load(BASE_DIR / "assets" / "textures" / "deathAnimation" / "death.png"), 
    },

    "DeathKnight":{
        "DeathKnight": pygame.image.load(BASE_DIR / "assets" / "textures" / "Death.png"), 
    },
        
    "Golem_DeathB":{
        "Golem_DeathB": pygame.image.load(BASE_DIR / "assets" / "textures" / "Golem" / "Golem_DeathB.png"), 
    },  
    
    "ExecutoreDeathB" : {
        "ExecutoreDeathB": pygame.image.load(BASE_DIR / "assets" / "textures" / "executoner" / "death.png"), 
    },       
     
    "NightBorne":{
        "NightBorne": pygame.image.load(BASE_DIR / "assets" / "textures" / "NightBorne.png"),
    },
    
    "MechaGolem": {
        "MechaGolem": pygame.image.load(BASE_DIR / "assets" / "textures" / "Mecha-stone Golem 0.1" / "mechaGolem.png"),
    },
    
    "Minotaur":{ 
        "Minotaur": pygame.image.load(BASE_DIR / "assets" / "textures" / "minotaur" / "minotaur.png"),
        # "Minotaur": pygame.image.load(BASE_DIR / "assets" / "textures" / "minotaur" / "image.png"),
    },
    
    "Golem":{
        "Idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "Golem" /"Golem_IdleB.png"),
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "Golem" /"Golem_Run.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "Golem" / "Golem_AttackC.png"),
    },

    "Executoner":{
        "Idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "executoner" /"summonIdle.png"),
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "executoner" /"idle2.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "executoner" /"attacking.png"),
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

    "Death":{
        "Death": frames.generate_frames(COMPLEX_TEXTURES["Death"]["Death"], 64, 64),
    },

    "DeathKnight":{
        "DeathKnight": frames.generate_frames(COMPLEX_TEXTURES["DeathKnight"]["DeathKnight"], 128, 64),
    },
        
    "ExecutoreDeathB":{
        "ExecutoreDeathB": frames.generate_frames(COMPLEX_TEXTURES["ExecutoreDeathB"]["ExecutoreDeathB"], 100, 100),
    },
        
    "Golem_DeathB":{
        "Golem_DeathB": frames.generate_frames(COMPLEX_TEXTURES["Golem_DeathB"]["Golem_DeathB"], 64, 64),
    },  
    "NightBorne":{
        "NightBorne": frames.generate_frames(COMPLEX_TEXTURES["NightBorne"]["NightBorne"], enemy1_width, enemy1_height),
    },
    
    "MechaGolem":{
        "MechaGolem": frames.generate_frames(COMPLEX_TEXTURES["MechaGolem"]["MechaGolem"], 100, 100),
    },  
     
    "Minotaur":{
        "Minotaur": frames.generate_frames(COMPLEX_TEXTURES["Minotaur"]["Minotaur"], 288 , 160),
    },
        
    "Golem":{
        "Idle":  frames.generate_frames(COMPLEX_TEXTURES["Golem"]["Idle"], 64 , 64),  
        "Run":  frames.generate_frames(COMPLEX_TEXTURES["Golem"]["Run"], 64 , 64),        
        "Attack": frames.generate_frames(COMPLEX_TEXTURES["Golem"]["Attack"], 64 , 64),
    },
    
    "Executoner":{
        "Idle":  frames.generate_frames(COMPLEX_TEXTURES["Executoner"]["Idle"], 50 , 50),  
        "Run":  frames.generate_frames(COMPLEX_TEXTURES["Executoner"]["Run"], 100 , 100),        
        "Attack": frames.generate_frames(COMPLEX_TEXTURES["Executoner"]["Attack"], 100 , 100),
    },  
}

# Generar frames del sprite
FRAMES = {
    # Frames para el jugador
    "kingRun":  frames.generate_frames(TEXTURES["kingRun"], king_width , king_height - 6),        
    "kingAttack": frames.generate_frames(TEXTURES["kingAttack"], king_width , king_height - 6),
    "kingJump": frames.generate_frames(TEXTURES["kingJump"], king_width, king_height - 6),
    "idle": frames.generate_frames(TEXTURES["idle"], king_width , king_height - 6),
    
    # Frames para objetos animados
    "fireplace": frames.generate_frames(TEXTURES["fireplace"], 64, 64),
    "torch": frames.generate_frames(TEXTURES["torch"], 64, 64),  
    "castleTorch": frames.generate_frames(TEXTURES["castleTorch"], 12, 42),
    "castleTorch1": frames.generate_frames(TEXTURES["castleTorch1"], 12, 42),
    
    # Frames para muerte
    "death": frames.generate_frames(TEXTURES["menu"], 64, 64),
    "key": frames.generate_frames(TEXTURES["key"], 31, 31),
}


ANIMATIONS_ENEMY_DELAYS = {
    "NightBorne": {
        "idle": 100,
        "run": 100,
        "attack": 80,
        "death": 100,
    },
    "Golem": {
        "idle": 100,
        "run": 100,
        "attack": 100,
        "death": 80,
    },
    "Minotaur": {
        "idle": 100,
        "run": 100,
        "attack": 150,
        "death": 100,
    },
    "MechaGolem": {
        "idle": 100,
        "run": 100,
        "attack": 100,
        "death": 100,
    },
    "Executoner": {
        "idle": 180,
        "run": 100,
        "attack": 100,
        "death": 100,
    }
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
    },

    "castleTorchBlue" : {
        "texture" : TEXTURES["castleTorch1"] ,
        "frames" : FRAMES["castleTorch1"] ,
        "correctionX" : 5,
        "correctionY" : 40,  
    },
    
    "key" : {
        "texture" : TEXTURES["key"] ,
        "frames" : FRAMES["key"] ,
        "correctionX" : 0,
        "correctionY" : 0,
    },
}

ANIMATED_DECORATIONS_INDEX = ["fireplace", "torch","castleTorch","castleTorchBlue"]


# Inicializar fuentes
pygame.font.init()
FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 8),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
    "big": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 32),
    "verybig": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 64),
} 