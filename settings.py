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

# Asignacion de tamaño de la ventana
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{WINDOW_WIDTH//4},{WINDOW_HEIGHT//4}"
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Nombre de la ventana
pygame.display.set_caption("Lost Kingdom")

# Rutas y recursos
BASE_DIR = pathlib.Path(__file__).parent

# width significa el ancho de la imagen
# height significa el alto de la imagen

# Factor de escala de la textura del jugador (Hacerlo mas grande o mas pequeño)
SCALE_FACTOR = 1.3

# Configuración del jugador
PLAYER_SPEED = 200
PLAYER_SPEED_JUMP = -7.8

# Velocidad de los enemigos
ENEMY_SPEED = 115


# Valor global que tendremos para la gravedad
GRAVITY = 0.33

# Asigamos el objeto que contiene el mapa de cada nivel, cada nivel se lee por orden , por ende level 1 , 2 , 3 dependera de la posicion de los niveles en el array
LEVELS = {
    # "intro1": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "introLevel.tmx", pixelalpha=True),
    "intro": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "levelTest.tmx", pixelalpha=True),
    "level1": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "levelCastle.tmx", pixelalpha=True),
    "roomboss": pytmx.load_pygame(BASE_DIR / "assets" / "tilemaps" / "roomboss.tmx", pixelalpha=True),
}

# Asignacion de sonidos
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
    "door_open": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "doorOpening.mp3"),  

    # Sonidos de ataques 
    "slash1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash1.wav"),
    "slash2": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "slash2.wav"),
    
    # Temas de fondo
    "principal_theme1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "EclipsedDesolation.wav"),
    "menu_theme1": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "CursedCitadel(Intro).wav"),
    "principal_theme": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "smoothMedieval.mp3"),
    "maquinaescribir": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "maquinaescribir.mp3"),
}

# Sonidos de muerte de los enemigos
DEATH_SOUNDS = {
    "Golem": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "rockDeath.mp3"),
    "MechaGolem": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "rockDeath.mp3"),
    "Executoner": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "parcDead.mp3"),
    "NightBorne": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "nigthtsDead.mp3"),
    "Minotaur": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "demonLaugh.mp3"),
}

# Texturas, frames y estructura para objetos estaticos
STATIC_TEXTURES = {
    "DoorClosed": pygame.image.load(BASE_DIR / "assets" / "textures" / "Decorations" / "door.png"),
    "DoorOpen": pygame.image.load(BASE_DIR / "assets" / "textures" / "Decorations" / "doorOpen.png"),
}

STATIC_FRAMES = {
    "DoorClosed": frames.generate_frames(STATIC_TEXTURES["DoorClosed"], 128, 128),
    "DoorOpen": frames.generate_frames(STATIC_TEXTURES["DoorOpen"], 128, 128),
}

STATIC_DECORATIONS = {
    "DoorClosed": {
        "texture": STATIC_TEXTURES["DoorClosed"],
        "frames": STATIC_FRAMES["DoorClosed"],
        "correctionX": 20,
        "correctionY": 54,
    },
    "DoorOpen": {
        "texture": STATIC_TEXTURES["DoorOpen"],
        "frames": STATIC_FRAMES["DoorOpen"],
        "correctionX": 20,
        "correctionY": 54,
    },
}

STATIC_DECORATIONS_INDEX = ["DoorClosed", "DoorOpen"]

# Generar textura del spritesheet
TEXTURES = {
 
    # TEXTURES para muerte
    "death": pygame.image.load(BASE_DIR / "assets" / "textures" / "deathAnimation" /"death.png"),
    
    # Frames para objetos animados
    "fireplace": pygame.image.load(BASE_DIR / "assets" / "textures" / "animateItems" /"fireplace.png"),
    "torch": pygame.image.load(BASE_DIR / "assets" / "textures" / "animateItems" / "torch.png"),
    "castleTorch": pygame.image.load(BASE_DIR / "assets" / "textures" / "animateItems" / "torch_big" / "castleTorch.png"),
    "castleTorch1": pygame.image.load(BASE_DIR / "assets" / "textures" / "animateItems" / "torch_big_blue" / "castleTorchBlue.png"),
    "key": pygame.image.load(BASE_DIR / "assets" / "textures" / "animateItems" / "Keys" / "KeyIcons.png"),
    
    # TEXTURES para las pantallas de menu, death y intro
    "menu": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "wallpapers"/ "slayer.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "death2": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "wallpapers" / "death2.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "intro2": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "wallpapers" / "intro2.png"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
    "outro": pygame.transform.scale(pygame.image.load(BASE_DIR / "assets" / "textures" / "wallpapers" / "outro2.jpg"),(VIRTUAL_WIDTH,VIRTUAL_HEIGHT)),
}

# Generar textura del spritesheet
COMPLEX_TEXTURES = {
    "Player":{
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "knight" /"run.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "knight" / "attacks.png"),
        "Jump": pygame.image.load(BASE_DIR / "assets" / "textures" / "knight" / "jump.png"),
        "Idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "knight" / "idle.png"),
        "Death": pygame.image.load(BASE_DIR / "assets" / "textures" / "knight" / "death.png"),
    },

    "Death":{
        "Death": pygame.image.load(BASE_DIR / "assets" / "textures" / "deathAnimation" / "death.png"), 
    },

    "Golem_DeathB":{
        "Golem_DeathB": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "Golem" / "Golem_DeathB.png"), 
    },  
    
    "ExecutoreDeathB" : {
        "ExecutoreDeathB": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "executoner" / "death.png"), 
    },       
     
    "NightBorne":{
        "NightBorne": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "NightBorne" / "NightBorne.png"),
    },
    
    "MechaGolem": {
        "MechaGolem": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "MechaGolem" / "mechaGolem.png"),
    },
    
    "Minotaur":{ 
        "Minotaur": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "minotaur" / "minotaur.png"),
    },
    
    "Golem":{
        "Idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "Golem" /"Golem_IdleB.png"),
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "Golem" /"Golem_Run.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "Golem" / "Golem_AttackC.png"),
    },

    "Executoner":{
        "Idle": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "executoner" /"summonIdle.png"),
        "Run": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "executoner" /"idle2.png"),
        "Attack": pygame.image.load(BASE_DIR / "assets" / "textures" / "enemies" / "executoner" /"attacking.png"),
    },  
}

# AQUI MANEJAMOS EL ANALISIS PARA ENEMIGOS Y JUGADORES PERO UN POQUITO MAS COMPLEJO
# YA QUE QUEREMOS QUE PUEDA ANALIZAR TODO UN SPRITESHEET DE TODOS LOS MOVIMIENTOS
# O UN SPTRITESHEET DE UN SOLO MOVIMIENTO , COMO POR EJEMPLO EL DE PLAYER
COMPLEX_FRAMES = {

    # Generate_frames es una funcion que recortar los frames del spritesheet
        # El primer parametro es la textura
        # El segundo parametro es el ancho de la textura
        # El tercer parametro es el alto de la textura
    # Debemos rectificar muy bien el ancho y alto de cada sprite porque influira en el array resultante que contenga cada frame de movimiento

    "Player":{
        "Run":  frames.generate_frames(COMPLEX_TEXTURES["Player"]["Run"], 128 , 64 ),        
        "Attack": frames.generate_frames(COMPLEX_TEXTURES["Player"]["Attack"], 128 , 64),
        "Jump": frames.generate_frames(COMPLEX_TEXTURES["Player"]["Jump"], 128, 64),
        "Idle": frames.generate_frames(COMPLEX_TEXTURES["Player"]["Idle"], 128 , 64),
        "Death": frames.generate_frames(COMPLEX_TEXTURES["Player"]["Death"], 128, 64),
        
    },

    "Death":{
        "Death": frames.generate_frames(COMPLEX_TEXTURES["Death"]["Death"], 64, 64),
    },
      
    "ExecutoreDeathB":{
        "ExecutoreDeathB": frames.generate_frames(COMPLEX_TEXTURES["ExecutoreDeathB"]["ExecutoreDeathB"], 100, 100),
    },
        
    "Golem_DeathB":{
        "Golem_DeathB": frames.generate_frames(COMPLEX_TEXTURES["Golem_DeathB"]["Golem_DeathB"], 64, 64),
    },  
    "NightBorne":{
        "NightBorne": frames.generate_frames(COMPLEX_TEXTURES["NightBorne"]["NightBorne"], 80, 80),
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
    # Frames para objetos animados
    "fireplace": frames.generate_frames(TEXTURES["fireplace"], 64, 64),
    "torch": frames.generate_frames(TEXTURES["torch"], 64, 64),  
    "castleTorch": frames.generate_frames(TEXTURES["castleTorch"], 12, 42),
    "castleTorch1": frames.generate_frames(TEXTURES["castleTorch1"], 12, 42),
    
    # Frames para muerte
    "death": frames.generate_frames(TEXTURES["menu"], 64, 64),
    "key": frames.generate_frames(TEXTURES["key"], 31, 31),
}

# Tiempos de restraso de animacion de los jugadores , a mayor tiempo mayor valor , mayor retraso de animacion (va mas lento)
ANIMATIONS_DELAYS = {
    "run": 100, 
    "attack": 120, 
    "jump": 190, 
    "idle": 120,
    "death": 400,
    "attack1": 40,  # Delay para el primer ataque (más rápido)
    "attack2": 50, # Delay para el segundo ataque
    "attack3": 60, # Delay para el tercer ataque
    "attack4": 100, # Delay para el cuarto ataque (más lento)
}

# Tiempos de restraso de animacion de los enemigos , a mayor tiempo mayor valor , mayor retraso de animacion (va mas lento)
# Esto se hace para que la transicion de sprites de animacion de los enemigos sea mas suave
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
        "attack": 70,
        "death": 100,
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
        "attack": 50,
        "death": 100,
    },
    "Executoner": {
        "idle": 180,
        "run": 100,
        "attack": 100,
        "death": 100,
    }
}



# Animaciones de los objetos animados
    # Se le asigna una textura , un arreglo de frames , y un desplazamiento para que se vea correctamente
    # las correcciones se hacen porque con el reescalado de la textura se pierde la posicion inicial de la textura y se debe ajustar
        # El desplazamiento en X es para que se vea correctamente en el mapa, Positivo a la izquierda , negativo a la derecha
        # El desplazamiento en Y es para que se vea correctamente en el mapa, Positivo hacia arriba , negativo hacia abajo
    
ANIMATED_DECORATIONS = {
    "fireplace" : {
        "texture" : TEXTURES["fireplace"] ,
        "frames" : FRAMES["fireplace"] ,
        "correctionX" : 20,
        "correctionY" : 60,
    },
    "torch" : {
        "texture" : TEXTURES["torch"] ,
        "frames" : FRAMES["torch"]   ,
        "correctionX" : 32,
        "correctionY" : 60,
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
        "correctionX" : 10,
        "correctionY" : 25,
    },
}

# Se le asigna un indice a cada objeto animado para que se pueda acceder a ellos en el mapa, asi podemos acceder a ellos mas facil en el mapa
ANIMATED_DECORATIONS_INDEX = ["fireplace", "torch","castleTorch","castleTorchBlue"]


# Inicializar fuentes
pygame.font.init()
FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 8),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 16),
    "big": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 32),
    "verybig": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 64),
} 