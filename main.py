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

# Inicializamos pygame
pygame.init()

class TileMap:
    def __init__(self,levelMap):
        self.map = settings.LEVELS[levelMap]
        self.width = self.map.width * self.map.tilewidth
        self.height = self.map.height * self.map.tileheight
        self.tmx_data = self.map
    
    def render(self,surface):
        tile_map = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tile_map(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth, 
                                                      y * self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
        
        
class Game:
    def __init__(self):

        # Cargamos el nivel que queremos en el tilemap
        self.current_tile_map = TileMap("intro")
        self.map_image = self.current_tile_map.make_map()
        self.map_rect = self.map_image.get_rect()
        #Fin de cracion de mapa

        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )

        pygame.display.set_caption("King Animation")
        self.clock = pygame.time.Clock()
        self.attack_moveset = {}
        
        # Configurar InputHandler
        self.input_handler = InputHandler()
        # self.input_handler.set_callback(self.on_input)

        # Cargar spritesheets del king
        self.sprite_sheets = {
            "run": settings.TEXTURES["kingRun"],
            "attack": settings.TEXTURES["kingAttack"],
            "jump": settings.TEXTURES["kingJump"],
        }

        self.frame_data = {
            "run": settings.FRAMES["kingRun"],
            "attack": settings.FRAMES["kingAttack"],
            "jump": settings.FRAMES["kingJump"],
        }

        # Almacenar todas las animaciones del knight
        self.animations = {"run": [], "attack": [], "jump": [], "idle": []}

        # Metodo para cargar todas las animaciones de movimiento del knight
        self.load_attack_animations()

        # Variables del personaje
        # Posicion donde empezara el knight
        self.x = 5
        self.y = settings.WINDOW_HEIGHT//2 +275

        # Aqui controlamos si va a izquierda o derecha
        self.direction = 1

        # Manejamos estados para el knight
        self.current_state = "idle"

        # Aqui controlamos los frames de animacion que tendra nuestro knight para idle,run y jump
        self.current_frame = 0
        self.animation_timer = 0

        # Variables para el sistema de combo
        self.current_combo = 1
        self.max_combo = 4
        self.combo_timer = 0

        # Tiempo en ms para mantener el combo
        self.combo_timeout = 500

        # Variables para el salto
        self.jumping = False
        self.jump_velocity = -15  # Velocidad inicial del salto
        self.gravity = 0.8
        self.vertical_velocity = 0
        self.ground_y = self.y  # Posición inicial del suelo

        # Variable para el ataque
        self.attacking = False
        self.attack_timer = 0

        # Velocidad de animaciones para cada estado, entre mas alto mas lento
        self.animation_delays = {"run": 100, "attack": 150, "jump": 100, "idle": 200}

        # Modificar el rectángulo de colisión con dimensiones base
        # Ancho base más pequeño
        self.base_rect_width = 30  
        # Alto base
        self.base_rect_height = 60  
        # Ancho durante ataque
        self.attack_rect_width = 55  

        # Offset para centrar el rectángulo con el sprite
        # Ajustes mañosos 
        self.rect_offset_x = 25  
        self.rect_offset_y = 8  

        # Inicializar el rectángulo
        self.king_rect = pygame.Rect(
            self.x + self.rect_offset_x,
            self.y + self.rect_offset_y,
            self.base_rect_width,
            self.base_rect_height,
        )

    def handle_inputs(self):
        keys = pygame.key.get_pressed()

        # Por defecto, establecemos el estado como idle
        new_state = "idle"

        # Salto
        if keys[K_SPACE] and not self.jumping:
            self.jumping = True
            self.vertical_velocity = self.jump_velocity
            new_state = "jump"

            self.current_combo = 1
            self.current_frame = 0
            self.attacking = False

        # Movimiento horizontal
        elif keys[K_LEFT] or keys[K_RIGHT]:
            self.direction = -1 if keys[K_LEFT] else 1
            self.x += (
                self.direction * settings.PLAYER_SPEED * self.clock.get_time() / 1000
            )
            new_state = "run"

        # Ataque
        if keys[K_x] and not self.jumping:
            # Si no estamos atacando, atacamos

            if not self.attacking:
                new_state = "attack"
                self.attacking = True
                self.attack_timer = 0
                self.current_frame = 0
                self.combo_timer = 0

            elif self.attacking:  # Si ya estamos atacando
                current_attack_frames = self.attack_moveset[
                    f"attack{self.current_combo}"
                ]
                # Verificar si estamos en el último frame o cerca del final
                # Permitir un poco antes del final
                if self.current_frame >= len(current_attack_frames) - 2:
                    if self.current_combo < self.max_combo:
                        self.current_combo += 1
                    else:
                        self.current_combo = 1
                    self.current_frame = 0
                    self.combo_timer = 0
            random_attack = 1
            settings.SOUNDS[f"slash{random_attack}"].stop()
            settings.SOUNDS[f"slash{random_attack}"].play()

        # Actualizar el estado actual
        if new_state != self.current_state:
            self.current_state = new_state
            # Solo resetear frame si no estamos atacando
            if not self.attacking:
                self.current_frame = 0
            self.animation_timer = 0

    def update(self):
        self.animation_timer += self.clock.get_time()
        self.combo_timer += self.clock.get_time()

        # Actualizar física del salto primero
        old_jumping = self.jumping
        self.vertical_velocity, self.y, self.jumping = update_vertical_acceleration(
            self.vertical_velocity, self.gravity, self.y, self.ground_y, self.jumping
        )

        # Si estamos saltando, forzar el estado de salto
        if self.jumping:
            self.current_state = "jump"
        # Si acabamos de aterrizar, volver al estado idle
        elif old_jumping and not self.jumping:
            self.current_state = "idle"
            self.current_frame = 0

        # Current delay es para saber cuanto tiempo tiene que pasar para que se cambie el frame de la animacion
        current_delay = self.animation_delays[self.current_state]

        # Actualizar animación
        if self.animation_timer >= current_delay:
            self.update_animation()
            self.animation_timer = 0

        # Actualizar tamaño del rectángulo de colisión
        rect_width = self.attack_rect_width if self.attacking else self.base_rect_width

        # Actualizar posición del rectángulo de colisión
        if self.direction == 1:
            rect_x = self.x + self.rect_offset_x * 2
        else:
            # correcion para que el rectangulo crezca a la izquierda
            rect_x = self.x + (self.rect_offset_x * 3 - rect_width)

        self.king_rect = pygame.Rect(
            rect_x, self.y + self.rect_offset_y, rect_width, self.base_rect_height
        )

    def load_attack_animations(self):
        # Crear las superficies para cada animación
        for animation_type, frames in self.frame_data.items():
            for frame in frames:
                surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
                surface.blit(self.sprite_sheets[animation_type], (0, 0), frame)
                self.animations[animation_type].append(surface)

        # Crear la animación idle usando frames específicos del ataque (No se porque pusieron los sprites de idle en el ataque)
        # Los frames específicos que queremos usar
        idle_frame_indices = [0, 1, 2]
        for idx in idle_frame_indices:
            self.animations["idle"].append(self.animations["attack"][idx])

        for i in range(4):
            # Tendremos 4 moveset es decir hasta combo de 4
            # Como los sprites son continuos agarraremos la continuidad de los mismos, osea 1 , 2 , 3....
            # estos numeros representan su posicion en el spritesheet, ejemplo 1 sera el spritesheet uno y asi sucesivamente
            start_idx = 3 + i * 4
            # Como los moveset seran siempre de 4 sera siempre su ciclo final
            end_idx = start_idx + 4
            # Guardamos los diferentes moveset que tendra para cada combo
            # En frase simples agarramos por orden del spritesheet:
            # attack 1 : contendra las imagenes 1 2 y 3 del spritesheet
            # attack 2 : contendra las imagenes 4 5 6 y 7 del spritesheet y asi sucesivamente
            # Leyendo el spritesheet de izquierda a derecha
            self.attack_moveset[f"attack{i + 1}"] = self.animations["attack"][
                start_idx:end_idx
            ]

    def reset_attack(self):
        self.current_combo = 1
        self.current_frame = 0
        self.attacking = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map_image, (0, settings.WINDOW_HEIGHT - self.map_image.get_height()))
        # Obtener el frame actual
        if self.attacking:
            attack_frames = self.attack_moveset[f"attack{self.current_combo}"]
            current_surface = attack_frames[self.current_frame]

        else:
            current_surface = self.animations[self.current_state][self.current_frame]

        if self.direction == -1:
            current_surface = pygame.transform.flip(current_surface, True, False)

        # Dibujar información de debug
        debug_info = f"Estado: {self.current_state} Combo: {self.current_combo} Frame: {self.current_frame}"
        font = pygame.font.Font(None, 36)
        text = font.render(debug_info, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        # Dibujar el sprite
        self.screen.blit(current_surface, (self.x, self.y))

        # Dibujar el rectángulo de colisión
        # pygame.draw.rect(
        #     self.screen, (255, 0, 0), self.king_rect, 2
        # ) 

        pygame.display.flip()

    def update_animation(self):
        if self.attacking:
            # Resetear combo si ha pasado demasiado tiempo
            if self.combo_timer >= self.combo_timeout:
                self.reset_attack()
            else:
                # Determinar qué frames usar basado en el combo actual
                attack_frames = self.attack_moveset[f"attack{self.current_combo}"]
                # Si el frame actual es el ultimo, resetear el ataque
                if self.current_frame >= len(attack_frames) - 1:
                    self.reset_attack()
                else:
                    self.current_frame += 1

        else:
            # Para animaciones normales (run, jump, idle)
            self.current_frame = (self.current_frame + 1) % len(
                self.animations[self.current_state]
            )
      
    def run(self):

        settings.SOUNDS["principal_theme"].play(loops=-1)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()            
                
            self.handle_inputs()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
