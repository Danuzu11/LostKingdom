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

# Inicializamos pygame
pygame.init()

class TileMap:
    def __init__(self, levelMap):
        self.map = settings.LEVELS[levelMap]
        self.width = self.map.width * self.map.tilewidth
        self.height = self.map.height * self.map.tileheight
        self.tmx_data = self.map

    def render(self, surface):
        tile_map = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tile_map(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                            y * self.tmx_data.tileheight))

    def make_map(self):
        # Crear una superficie temporal con las dimensiones originales del tilemap
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        
        # Calcular el factor de escala para ajustar el tilemap al alto virtual de la pantalla
        scale_factor = settings.VIRTUAL_HEIGHT / self.height

        # Escalar el tilemap
        scaled_width = int(self.width * scale_factor)
        scaled_height = int(self.height * scale_factor)
        scaled_surface = pygame.transform.smoothscale(temp_surface, (scaled_width, scaled_height))

        return scaled_surface
        
class Game:
    def __init__(self):
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
        
        # Inicializar la camara con el tamaño del mundo
        self.camera = Camera()
        self.camera.set_world_size(self.map_image.get_width(), self.map_image.get_height())

        # Lista para almacenar los objetos solidos
        self.solid_objects = []
        self.offset_obstacle_width = 8
        
        # Lista para almacenar los objetos animados
        self.animated_items = []
        
        #Animacion de frames de la fogata
        self.fireanimations = []
        
        spritesheet = settings.TEXTURES["fireplace"]  # Asegúrate de que esta sea la textura del spritesheet
        print(spritesheet)
        for frame in settings.FRAMES["fireplace"]:
            surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
            surface.blit(spritesheet, (0, 0), frame)
            self.fireanimations.append(surface)
        
        self.torchanimations = []
        spritesheet1 = settings.TEXTURES["torch"]  # Asegúrate de que esta sea la textura del spritesheet

        for frame1 in settings.FRAMES["torch"]:
            # Crear una superficie del tamaño del frame
            surface = pygame.Surface((frame1.width, frame1.height), pygame.SRCALPHA)
            # Recortar el frame del spritesheet
            surface.blit(spritesheet1, (0, 0), frame1)
            self.torchanimations.append(surface)
            
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
                # Crear un objeto animado para la fogata
                    # Posiciones reecaladas
                    # Array con animaciones
                    # Timpo entre frames
                fogata = AnimatedItem(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    self.fireanimations,  
                    animation_delay=150  
                )
                self.animated_items.append(fogata)
                
            if objects.name == "torch":
                # Crear un objeto animado para la fogata
                    # Posiciones reecaladas
                    # Array con animaciones
                    # Timpo entre frames
                torch = AnimatedItem(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    self.torchanimations,  
                    animation_delay=150  
                )
                self.animated_items.append(torch)
           
    
        

                 
        self.player = Player(self.player_x, self.player_y)
        
        self.screen = pygame.display.set_mode(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
            
        pygame.display.set_caption("King Animation")
         
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
        
        # Dibujamos el mapa con offset de cámara
        map_pos = (-self.camera.offset_x, -self.camera.offset_y)
        self.screen.blit(self.map_image, map_pos)
        
        # Dibujar los objetos sólidos
        # for solid in self.solid_objects:
        #     rect_with_offset = pygame.Rect(
        #         solid.x - self.camera.offset_x,
        #         solid.y - self.camera.offset_y,
        #         solid.width,
        #         solid.height
        #     )
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect_with_offset, 2)
        
        # Dibujar los objetos animados
        for animated_item in self.animated_items:
            animated_item.draw(self.screen, (self.camera.offset_x, self.camera.offset_y))

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
        
        # # Efecto de iluminación alrededor de las antorchas
        # for torch in self.animated_items:
        #     if isinstance(torch, AnimatedItem):  # Asegúrate de que sea una antorcha
        #         torch_screen_x = torch.x - self.camera.offset_x
        #         torch_screen_y = torch.y - self.camera.offset_y
        #         self.draw_light_effect(torch_screen_x, torch_screen_y, radius=20)
                

        pygame.display.flip()
        

      
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

    # def create_vignette(width, height, radius=0.75, color=(0, 0, 0)):
    #     """Versión optimizada usando dibujo de círculos"""
    #     vignette = pygame.Surface((width, height), pygame.SRCALPHA)
        
    #     # Dibujar rectángulo oscuro que cubra toda la pantalla
    #     pygame.draw.rect(vignette, (*color, 200), (0, 0, width, height))
        
    #     # Dibujar círculo transparente en el centro
    #     center = (width//2, height//2)
    #     max_radius = int(math.sqrt(width**2 + height**2) * radius)
        
    #     for r in range(max_radius, 0, -10):
    #         alpha = int(255 * (1 - r/max_radius))
    #         pygame.draw.circle(vignette, (*color, alpha), center, r)
        
    #     return vignette
    
        
    # def draw_light_effect(self, x, y, radius):
    #     """
    #     Dibuja un efecto de iluminación alrededor de un punto.
        
    #     :param x: Coordenada x del centro de la luz.
    #     :param y: Coordenada y del centro de la luz.
    #     :param radius: Radio del efecto de iluminación.
    #     """
    #     light_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    #     color = (78, 50, 38)
    #     intensity = 0.1
    #     for r in range(radius, 0, -1):
    #         alpha = int(255 * intensity * (1 - r/radius)**2)
    #         pygame.draw.circle(light_surface, (*color, 255), (radius, radius), r)
            
    #     self.screen.blit(light_surface, (x + 9, y + 23 ), special_flags=pygame.BLEND_RGBA_ADD)
        
# class Obstacle(pygame.sprite.Sprite):
 
 
#     def __init__(self, x, y, width, height):
#         """
#         Inicializa un objeto sólido (obstáculo).
        
#         :param x: Coordenada x del obstáculo.
#         :param y: Coordenada y del obstáculo.
#         :param width: Ancho del obstáculo.
#         :param height: Alto del obstáculo.
#         """
#         self.rect = pygame.Rect(x, y, width, height)

#     def draw(self, screen, color=(0, 255, 0)):
#         """
#         Dibuja el rectángulo del obstáculo en la pantalla (para depuración).
        
#         :param screen: Superficie de Pygame donde se dibujará.
#         :param color: Color del rectángulo (por defecto verde).
#         """
#         pygame.draw.rect(screen, color, self.rect, 2)   
           
if __name__ == "__main__":
    game = Game()
    game.run()
