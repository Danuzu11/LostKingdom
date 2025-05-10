from gale.state import BaseState
from src.Player import Player
from src.Camera import Camera
from src.TileMap import TileMap
import src.AnimatedItem as AnimatedItem
from gale.input_handler import InputData
import settings
import pygame
import src.Enemy as Enemy

class PlayState(BaseState):
    def enter(self, **params: dict):
        
        if params:  # Si se pasan parámetros, restaurar el estado
            self.player = params.get("player")
            self.camera = params.get("camera")
            self.solid_objects = params.get("solid_objects", [])
            self.animated_items = params.get("animated_items", [])
            self.enemies = params.get("enemies", [])
            self.current_tile_map = params.get("current_tile_map")
            self.map_image = params.get("map_image")
            # self.horizontal_velocity = params.get("horizontal_velocity", 0)
            # self.vertical_velocity = params.get("vertical_velocity", 0)
            # self.player_x = .self.player
            # self.player_y = objects.y * scale_factor
                    
        else:  # Si no se pasan parámetros, inicializar desde cero
            # Inicializar variables del juego
            self.current_tile_map = TileMap("intro")
            self.map_image = self.current_tile_map.make_map()
            self.map_rect = self.map_image.get_rect()
            self.mask_objects = []
            # Escalar el mapa
            scale_factor = settings.VIRTUAL_HEIGHT / self.current_tile_map.height

            # Inicializar la cámara
            self.camera = Camera()
            self.camera.set_world_size(self.map_image.get_width(), self.map_image.get_height())

            # Inicializar el jugador
            self.player_x, self.player_y = 0, 0
            self.solid_objects = []
            self.animated_items = []
            self.object_animations = {}
            self.enemies = []

            # Cargar animaciones de objetos (spritesheets cargados desde settings.py)
            for spritesheet_name, spritesheet_data in settings.ANIMATED_DECORATIONS.items():
                spritesheet = spritesheet_data["texture"]
                frames = spritesheet_data["frames"]
                animation_frames = []
                for frame in frames:
                    surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
                    surface.blit(spritesheet, (0, 0), frame)
                    animation_frames.append(surface)
                self.object_animations[spritesheet_name] = animation_frames

            # Cargar objetos del mapa
            for objects in self.current_tile_map.tmx_data.objects:
                if objects.name == "Player":
                    self.player_x = objects.x * scale_factor
                    self.player_y = objects.y * scale_factor
                elif objects.name == "obstacle":
                    solid_rect = pygame.Rect(
                        objects.x * scale_factor,
                        objects.y * scale_factor,
                        objects.width * scale_factor,
                        objects.height * scale_factor,
                    )
                    self.solid_objects.append(solid_rect)
                elif objects.name in ["fireplace", "torch","castleTorch"]:
                    animated_item = AnimatedItem(
                        objects.x * scale_factor,
                        objects.y * scale_factor,
                        self.object_animations[objects.name],
                        animation_delay=150,
                    )
                    self.animated_items.append(animated_item)
                elif objects.name == "NightBorne":
                    enemy = Enemy(
                        objects.x * scale_factor,
                        objects.y * scale_factor,
                        "NightBorne",
                    )
                    self.enemies.append(enemy)
                elif objects.name == "Golem":
                    enemy = Enemy(
                        objects.x * scale_factor,
                        objects.y * scale_factor,
                        "Golem",
                    )
                    self.enemies.append(enemy)
                    
                elif objects.name == "mask":
                    mask_rect = pygame.Rect(
                        objects.x * scale_factor,
                        objects.y * scale_factor,
                        objects.width * scale_factor,
                        objects.height * scale_factor,
                    )
                    self.mask_objects.append(mask_rect)
                 
            # Inicializar el jugador
            self.player = Player(self.player_x, self.player_y)


    def on_input(self, input_id: str, input_data: InputData) -> None:    
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                previous_state=self,
                player=self.player,
                camera=self.camera,
                solid_objects=self.solid_objects,
                animated_items=self.animated_items,
                enemies=self.enemies,
                current_tile_map=self.current_tile_map,
                map_image=self.map_image
            )
            
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("menu")  # Cambiar al estado de menú
        new_state = "idle"      
        if input_id == "move_left":
            if input_data.pressed:
                self.player.horizontal_velocity = -settings.PLAYER_SPEED
                self.player.direction = -1
                # Si está en el aire, mantener el estado "jump"
                if not self.player.on_ground:
                    self.player.current_state = "jump"
                # Si está en el suelo, cambiar a "run"
                elif self.player.on_ground and not self.player.jumping:
                    self.player.current_state = "run"
            elif input_data.released:
                self.player.horizontal_velocity = 0
                # Cambiar a "idle" solo si está en el suelo
                if self.player.on_ground and not self.player.jumping:
                    self.player.current_state = "idle"

        elif input_id == "move_right":
            if input_data.pressed:
                self.player.horizontal_velocity = settings.PLAYER_SPEED
                self.player.direction = 1
                # Si está en el aire, mantener el estado "jump"
                if not self.player.on_ground:
                    self.player.current_state = "jump"
                # Si está en el suelo, cambiar a "run"
                elif self.player.on_ground and not self.player.jumping:
                    self.player.current_state = "run"
            elif input_data.released:
                self.player.horizontal_velocity = 0
                # Cambiar a "idle" solo si está en el suelo
                if self.player.on_ground and not self.player.jumping:
                    self.player.current_state = "idle"
       
        elif input_id == "jump" and self.player.vertical_velocity == 0 and not self.player.jumping:
            if self.player.on_ground and not self.player.jumping:

                self.player.jumping = True
                self.player.current_state = "jump"
                new_state = "jump"
                self.player.jumping = True
                self.player.vertical_velocity = settings.PLAYER_SPEED_JUMP
                self.player.ground_collide = False
                self.player.current_combo = 1
                self.player.current_frame = 0
                self.player.attacking = False
                        
        elif input_id == "x" and not self.player.jumping :
            random_attack = 1
            # Validamos si no estamos atacando ya , si el player no se encuentra atacando entonces comienza el ataque en combo
            if not self.player.attacking:
                new_state = "attack"
                self.player.attacking = True
                self.player.current_frame = 0
                self.player.combo_timer = 0
                settings.SOUNDS[f"slash{random_attack}"].stop()
                settings.SOUNDS[f"slash{random_attack}"].play()
            # Si ya estamos atacando , verifica que combo se esta ejecutando actualmente y actua en consecuencia
            # Solo tenemos 4 movimiento distintos es decir combos de x4
            elif self.player.attacking:  
                
                # Almacenamos que frame es el del combo actual que se va a ejecutar
                current_attack_frames = self.player.attack_moveset[
                    f"attack{self.player.current_combo}"
                ]
                
                # Verificar si estamos en el último frame o cerca del final, si esta en el ultimo reiniciamos el combo y volvemos a la animacion de attack1
                # Permitir un poco antes del final
                if self.player.current_frame >= len(current_attack_frames) - 2:
                    if self.player.current_combo < self.player.max_combo:
                        self.player.current_combo += 1
                        # Aqui en teoria deberiamos meter un sonido aleatorio pero hay que solucionar el tema de que se reproducen los sonidos montados
                        settings.SOUNDS[f"slash{random_attack}"].stop()
                        settings.SOUNDS[f"slash{random_attack}"].play()
                    else:
                        self.player.current_combo = 1
                 
                    self.player.current_frame = 0
                    self.player.combo_timer = 0
                              
        if new_state != self.player.current_state:
            self.player.current_state = new_state
            # Solo resetear frame si no estamos atacando
            if not self.player.attacking:
                self.player.current_frame = 0
            self.player.animation_timer = 0    
                
    def update(self, dt: float) -> None:

        if self.player.current_health <= 0: 
            self.state_machine.change(
                "game_over"
            )   
            
        delta_time = dt * 1000

        # Actualizar enemigos
        for enemy in self.enemies:
            enemy.update(delta_time, self.player, self.solid_objects)
        
        self.player.update(delta_time, self.solid_objects)
        self.camera.update(self.player.camera_rect, None)   
        # Actualizar objetos animados
        for animated_item in self.animated_items:
            animated_item.update(delta_time)
            
    def verify_door_next_level(self):
        """
        Verifica si el jugador ha llegado a la puerta de salida del nivel.
        """
        for door in self.current_tile_map.tmx_data.objects:
            if door.name == "door":
                if self.player.get_collision_rect().colliderect(door):
                    return True
        return False
        
    def render(self, surface):
        """
        Renderiza el estado de juego.
        """
        surface.fill((0, 0, 0))

        # Dibujar el mapa
        map_pos = (-self.camera.offset_x, -self.camera.offset_y)
        surface.blit(self.map_image, map_pos)

        # Dibujar objetos animados
        for animated_item in self.animated_items:
            animated_item.draw(surface, (self.camera.offset_x, self.camera.offset_y))
            

        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(surface, (self.camera.offset_x , self.camera.offset_y))
            
        # Dibujar al jugador
        player_screen_x = self.player.x - self.camera.offset_x
        player_screen_y = self.player.y - self.camera.offset_y
        self.player.render(surface, (player_screen_x, player_screen_y))
        
        # Renderizar la máscara con el offset de la cámara
        self.current_tile_map.render_mask(surface, (self.camera.offset_x, self.camera.offset_y))
            
            
        #Dibujar los objetos sólidos
        for solid in self.solid_objects:
            rect_with_offset = pygame.Rect(
                solid.x - self.camera.offset_x,
                solid.y - self.camera.offset_y,
                solid.width,
                solid.height
            )
            pygame.draw.rect(surface, (255, 0, 0), rect_with_offset, 2)
        # Debug info
        # debug_info = f"Camera: ({self.camera.offset_x}, {self.camera.offset_y})"
        # font = pygame.font.Font(None, 36)
        # text = font.render(debug_info, True, (255, 255, 255))
        # surface.blit(text, (10, 40))