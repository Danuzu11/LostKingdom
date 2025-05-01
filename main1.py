"""
ISPPJ1 2024
Study Case: New Martian (Platformer)

This file contains the main program to run the game.
"""

import pygame
import sys
import settings
from pygame.locals import *
from src.globalUtilsFunctions import update_vertical_acceleration
import random
from gale.input_handler import InputHandler, InputData
import pytmx
import src.Player as Player
import src.Camera as Camera
import src.AnimatedItem as AnimatedItem
import math
import src.TileMap as TileMap
import os

# Inicializamos pygame
pygame.init()
    
class Game:
    
    def __init__(self):
        
         # Lista para almacenar máscaras
        self.masks = []

        # Ejemplo: Cargar una máscara desde los assets
        mask_image = pygame.image.load(settings.BASE_DIR / "assets" / "textures" / "background_layer_3.png").convert_alpha()
        self.masks.append({"image": mask_image, "position": (500, 300)})  # Posición fija como ejemplo
        
        # Inicializamos el reloj    
        self.clock = pygame.time.Clock()

        # Cargamos el tilemap
        self.current_tile_map = TileMap("intro")
        self.map_image = self.current_tile_map.make_map()
        # Obtenemos el rectángulo de colision del tilemap
        self.map_rect = self.map_image.get_rect()

        # Calculamos el factor de escala para ajustar el tilemap al alto virtual de la pantalla
        scale_factor = settings.VIRTUAL_HEIGHT / self.current_tile_map.height
        # Inicializamos la posicion del jugador
        self.player_x, self.player_y = 0, 0
        
        # Inicializar la camara con el tamaño del mundo , para que la camara tenga el tama;o del tilemap y se mueva encima de el
        self.camera = Camera()
        self.camera.set_world_size(self.map_image.get_width(), self.map_image.get_height())

        # Lista para almacenar los objetos solidos
        self.solid_objects = []
        self.offset_obstacle_width = 8
        
        # Lista para almacenar los objetos animados
        self.animated_items = []
        
        #Animacion de frames de la fogata
        self.fireanimations = []
        
        self.object_animations = {}

        for spritesheet_name , spritesheet_data in settings.ANIMATED_DECORATIONS.items():
            
            print(spritesheet_name)
            # Obtenemos la textura y los frames de la animacion del objeto
            spritesheet = spritesheet_data["texture"]
            frames = spritesheet_data["frames"]
            
            # Crear una lista para almacenar las superficies de animación
            animation_frames = []
            
            for frame in frames:
                # Crea una superficie para el frame
                surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
                # Recorta el frame 
                surface.blit(spritesheet, (0, 0), frame)
                # Vamos guardando en la lista los frames de la animacion
                animation_frames.append(surface)
            
            self.object_animations[spritesheet_name] = animation_frames
            
     
        # Metodo manual lo deje porsiaca
        # spritesheet = settings.TEXTURES["fireplace"] 

        # for frame in settings.FRAMES["fireplace"]:
        #     surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
        #     surface.blit(spritesheet, (0, 0), frame)
        #     self.fireanimations.append(surface)
        
        # self.torchanimations = []
        # spritesheet1 = settings.TEXTURES["torch"] 

        # for frame1 in settings.FRAMES["torch"]:
        #     # Crear una superficie del tamaño del frame
        #     surface = pygame.Surface((frame1.width, frame1.height), pygame.SRCALPHA)
        #     # Recortar el frame del spritesheet
        #     surface.blit(spritesheet1, (0, 0), frame1)
        #     self.torchanimations.append(surface)
            
        for objects in self.current_tile_map.tmx_data.objects:
            
            if objects.name == "Player":
                self.player_x = objects.x * scale_factor
                self.player_y = objects.y * scale_factor
                
            if objects.name == "obstacle":
                solid_rect = pygame.Rect(
                    objects.x * scale_factor,
                    objects.y * scale_factor ,
                    objects.width * scale_factor,
                    objects.height * scale_factor ,
                )
                self.solid_objects.append(solid_rect)
                
            if objects.name == "fireplace":
                # Crear un objeto animado para la fireplace
                    # Posiciones reescaladas
                    # Array con animaciones
                    # Timpo entre frames
                fireplace = AnimatedItem(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    self.object_animations[objects.name],  
                    animation_delay=150  
                )
                self.animated_items.append(fireplace)
                
            if objects.name == "torch":
                # Crear un objeto animado para la fogata
                    # Posiciones reescaladas
                    # Array con animaciones
                    # Timpo entre frames
                torch = AnimatedItem(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    self.object_animations[objects.name],    
                    animation_delay=150  
                )
                self.animated_items.append(torch)
           
    
        

                 
        self.player = Player(self.player_x, self.player_y)
        
        self.screen = pygame.display.set_mode(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
             
    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        delta_time = self.clock.get_time()
        self.player.handle_inputs(keys,delta_time)

    def update(self):
        delta_time = self.clock.get_time()
        self.player.update(delta_time, self.solid_objects)
        self.camera.update(self.player.camera_rect,self.screen)
        
        # Actualizar los objetos animados
        for animated_item in self.animated_items:
            animated_item.update(delta_time)

    def draw(self):

        self.screen.fill((0, 0, 0))
        # Dibujar las máscaras por encima de todo
        for mask in self.masks:
            self.screen.blit(mask["image"], mask["position"])
        # Dibujamos el mapa con offset de cámara
        map_pos = (-self.camera.offset_x, -self.camera.offset_y)
        self.screen.blit(self.map_image, map_pos)
        
        # Dibujar los objetos animados
        for animated_item in self.animated_items:
            # Dibujar el objeto animado
            # Ajustar la posición del objeto animado segun la camara
            animated_item.draw(self.screen, (self.camera.offset_x, self.camera.offset_y))
            
        # Dibujar los objetos sólidos
        # for solid in self.solid_objects:
        #     rect_with_offset = pygame.Rect(
        #         solid.x - self.camera.offset_x,
        #         solid.y - self.camera.offset_y,
        #         solid.width,
        #         solid.height
        #     )
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect_with_offset, 2)
        

            
        # # Efecto de iluminación alrededor de las antorchas
        # for torch in self.animated_items:
        #     if isinstance(torch, AnimatedItem):  # Asegúrate de que sea una antorcha
        #         torch_screen_x = torch.x - self.camera.offset_x
        #         torch_screen_y = torch.y - self.camera.offset_y
        #         self.draw_light_effect(torch_screen_x, torch_screen_y, radius=20)
        # Para el jugador, calculamos su posición en pantalla
        
        player_screen_x = self.player.x - self.camera.offset_x
        player_screen_y = self.player.y - self.camera.offset_y
        
        # Dibujamos al jugador en su posición de pantalla
        self.player.draw(self.screen, (player_screen_x, player_screen_y))
        

            
        # Debug info: mostrar posición de la cámara
        debug_info = f"Camera: ({self.camera.offset_x}, {self.camera.offset_y})"
        font = pygame.font.Font(None, 36)
        text = font.render(debug_info, True, (255, 255, 255))
        self.screen.blit(text, (10, 40))
        
        pygame.display.flip()
    
    # def draw_light_effect(self, x, y, radius):
    #     # Crear una superficie transparente para la luz
    #     light_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
    #     # Dibujar un círculo de luz (gradiente) en la superficie
    #     for i in range(radius, 0, -1):
    #         alpha = int(255 * (i / radius))  # Gradiente de transparencia
    #         pygame.draw.circle(light_surface, (255, 255, 100, alpha), (radius, radius), i)
        
    #     # Dibujar la superficie de luz en la pantalla
    #     self.screen.blit(light_surface, (x - radius, y - radius), special_flags=pygame.BLEND_RGBA_ADD)
        
    def run(self):

        settings.SOUNDS["principal_theme"].play(loops=-1)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()            
                        
                if event.type == MOUSEBUTTONDOWN:
                    # Obtener las coordenadas del clic
                    mouse_x, mouse_y = event.pos
                    print(f"Clic en: ({mouse_x}, {mouse_y})")
                    
            self.handle_inputs()
            self.update()
            self.draw()
            self.clock.tick(60)
  
           
if __name__ == "__main__":
    game = Game()
    game.run()
