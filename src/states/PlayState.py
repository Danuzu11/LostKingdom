from gale.state import BaseState
from src.Player import Player
from src.Camera import Camera
from src.TileMap import TileMap
import src.AnimatedItem as AnimatedItem
from gale.input_handler import InputData
import settings
import pygame
import src.Enemy as Enemy
from src.globalUtilsFunctions import fade 
from src.QuadTree import QuadTree

class PlayState(BaseState):
    def enter(self, **params: dict):
        # Variables para el fade in
        self.fade_alpha = 255
        self.fade_surface = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.fade_speed = 3
       
        self.door_trigger = None
         # Lista de niveles disponibles
        self.available_levels = list(settings.LEVELS.keys())
        self.current_level_index = 0  
        
        if params:  # Si se pasan parametros, restaurar el estado
            self.player = params.get("player")
            self.camera = params.get("camera")
            self.solid_objects = params.get("solid_objects", [])
            self.animated_items = params.get("animated_items", [])
            self.enemies = params.get("enemies", [])
            self.current_tile_map = params.get("current_tile_map")
            self.map_image = params.get("map_image")
            self.fade_in = False 
            self.current_level_index = params.get("current_level_index", 0)

            level_name = params.get("level_name")
            if level_name:
                self.load_level(level_name)

        else:  # Si no se pasan parametros, inicializar desde cero
            self.transition = True
            self.current_level_index = 0
            self.load_level(self.available_levels[self.current_level_index])
            
            
            # Inicializar variables del juego
            # self.transition = True
            # self.current_tile_map = TileMap("intro")
            # # self.current_tile_map = TileMap("roomboss")
            # self.map_image = self.current_tile_map.make_map()
            # self.map_rect = self.map_image.get_rect()
            # self.mask_objects = []
            
            
            # # Escalar el mapa si el mapa creado es mucho mas peque;o que la pantalla
            # scale_factor = settings.VIRTUAL_HEIGHT / self.current_tile_map.height
            
            # # El tama;o maximo de altura sera 16 en tile (relacion por la ventana que tenemos)
            # max_tile_height = 16
            # max_pixel_height = max_tile_height * self.current_tile_map.tmx_data.tileheight
            
            # # Si el mapa es mas grande no hara ningun reescalado
            # if self.current_tile_map.height > max_pixel_height:
            #     scale_factor = 1
            # # scale_factor = 1
            # # Inicializar la cámara
            # self.camera = Camera()
            # self.camera.set_world_size(self.map_image.get_width(), self.map_image.get_height())

            # # Inicializar el jugador
            # self.player_x, self.player_y = 0, 0
            # self.solid_objects = []
            # self.animated_items = []
            # self.object_animations = {}
            # self.enemies = []

            # # Cargar animaciones de objetos (spritesheets cargados desde settings.py)
            # for spritesheet_name, spritesheet_data in settings.ANIMATED_DECORATIONS.items():
            #     spritesheet = spritesheet_data["texture"]
            #     frames = spritesheet_data["frames"]
            #     animation_frames = []
            #     for frame in frames:
            #         surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
            #         surface.blit(spritesheet, (0, 0), frame)
            #         animation_frames.append(surface)
            #     self.object_animations[spritesheet_name] = animation_frames

            # # Cargar objetos del mapa
            # for objects in self.current_tile_map.tmx_data.objects:
            #     if objects.name == "Player":
            #         self.player_x = objects.x * scale_factor
            #         self.player_y = objects.y * scale_factor
            #     elif objects.name == "obstacle":
            #         solid_rect = pygame.Rect(
            #             objects.x * scale_factor,
            #             objects.y * scale_factor,
            #             objects.width * scale_factor,
            #             objects.height * scale_factor,
            #         )
            #         self.solid_objects.append(solid_rect)
            #     elif objects.name in ["fireplace", "torch","castleTorch"]:
            #         animated_item = AnimatedItem(
            #             objects.x * scale_factor - settings.ANIMATED_DECORATIONS[objects.name]["correctionX"],
            #             objects.y * scale_factor - settings.ANIMATED_DECORATIONS[objects.name]["correctionY"],
            #             self.object_animations[objects.name],
            #             animation_delay=150,
            #         )
            #         self.animated_items.append(animated_item)
                
            #     elif objects.name == "NightBorne":
            #         enemy = Enemy(
            #             objects.x * scale_factor,
            #             objects.y * scale_factor,
            #             "NightBorne",
            #         )
            #         self.enemies.append(enemy)
            #     elif objects.name == "Golem":
            #         enemy = Enemy(
            #             objects.x * scale_factor,
            #             objects.y * scale_factor,
            #             "Golem",
            #         )
            #         self.enemies.append(enemy)
            #     elif objects.name == "Minotaur":
            #         enemy = Enemy(
            #             objects.x * scale_factor,
            #             objects.y * scale_factor,
            #             "Minotaur",
            #         )
            #         self.enemies.append(enemy)
                               
            #     elif objects.name == "mask":
            #         mask_rect = pygame.Rect(
            #             objects.x * scale_factor,
            #             objects.y * scale_factor,
            #             objects.width * scale_factor,
            #             objects.height * scale_factor,
            #         )
            #         self.mask_objects.append(mask_rect)
        
            # # Indica que estamos haciendo fade in
            # self.fade_in = True
            
            # # Inicializar el jugador
            # self.player = Player(self.player_x, self.player_y)


    def load_level(self, level_name):
        """Carga un nuevo nivel"""
  
        # Limpiar objetos del nivel anterior
        self.solid_objects = []
        self.animated_items = []
        self.enemies = []
        self.mask_objects = []

      
     
        
        # Cargar el nuevo nivel
        self.current_tile_map = TileMap(level_name)
        self.map_image = self.current_tile_map.make_map()
        self.map_rect = self.map_image.get_rect()
            # Inicializar variables del juego
        self.transition = True
            
        # Escalar el mapa si el mapa creado es mucho mas peque;o que la pantalla
        scale_factor = settings.VIRTUAL_HEIGHT / self.current_tile_map.height
            
        # El tama;o maximo de altura sera 16 en tile (relacion por la ventana que tenemos)
        max_tile_height = 16
        max_pixel_height = max_tile_height * self.current_tile_map.tmx_data.tileheight
            
            # Si el mapa es mas grande no hara ningun reescalado
        if self.current_tile_map.height > max_pixel_height:
            scale_factor = 1
            # scale_factor = 1
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
                print(objects.id)
                solid_rect = pygame.Rect(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    objects.width * scale_factor,
                    objects.height * scale_factor,
                    
                )
                self.solid_objects.append(solid_rect)

            elif objects.name == "door_trigger":
                self.door_trigger = pygame.Rect(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    objects.width * scale_factor,
                    objects.height * scale_factor,
                )
           
            elif objects.name in ["fireplace", "torch","castleTorch","key"]:
                animated_item = AnimatedItem(
                    objects.x * scale_factor - settings.ANIMATED_DECORATIONS[objects.name]["correctionX"],
                    objects.y * scale_factor - settings.ANIMATED_DECORATIONS[objects.name]["correctionY"],
                    self.object_animations[objects.name],
                    animation_delay=150,
                    name = objects.name
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
            elif objects.name == "Minotaur":
                enemy = Enemy(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    "Minotaur",
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
    
        # Indica que estamos haciendo fade in
        self.fade_in = True
        
        # Inicializar el jugador
        # Solo crear un nuevo jugador si no existe uno
        if not hasattr(self, 'player'):
            self.player = Player(self.player_x, self.player_y)
        else:
            # Actualizar la posición del jugador existente
            self.player.x = self.player_x
            self.player.y = self.player_y

    
    # Ahora sí podemos establecer has_key
        self.player.has_key = False
       

    def on_input(self, input_id: str, input_data: InputData) -> None:  
        new_state = "idle"     

        if input_id == "next_level" and input_data.pressed:
            # Avanzar al siguiente nivel
            
         if self.player.has_key and self.door_trigger and self.player.king_rect.colliderect(self.door_trigger):
                # Avanzar al siguiente nivel
                self.current_level_index = (self.current_level_index + 1) % len(self.available_levels)
                next_level = self.available_levels[self.current_level_index]
                
                # Guardar el estado actual para pasarlo al nuevo nivel
                current_state = {
                    "player": self.player,
                    "camera": self.camera,
                    "solid_objects": self.solid_objects,
                    "animated_items": self.animated_items,
                    "enemies": self.enemies,
                    "current_tile_map": self.current_tile_map,
                    "map_image": self.map_image,
                    "current_level_index": self.current_level_index,
                     "level_name": next_level 
                    
                }
                
                # Cargar el nuevo nivel
                self.load_level(next_level)
                print(next_level)

                # Cambiar al nuevo nivel manteniendo el estado
                self.state_machine.change(
                    "play",
                    previous_state=self,
                    **current_state  # Pasamos todos los datos del estado actual
                )
           
        else:
            if not self.player.has_key:
                print("¡Necesitas la llave para avanzar al siguiente nivel!")
            elif not self.door_trigger or not self.player.king_rect.colliderect(self.door_trigger):
                print("¡Debes estar frente a la puerta!")

        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("menu")  # Cambiar al estado de menú
    
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

        if input_id == "move_right":
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
       
        if input_id == "jump" and not self.player.jumping:
            
            if self.player.on_ground and not self.player.jumping:
                self.player.jumping = True
                self.player.current_state = "jump"
                new_state = "jump"
                self.player.jumping = True
                self.player.vertical_velocity = settings.PLAYER_SPEED_JUMP
                self.player.current_combo = 1
                self.player.current_frame = 0
                self.player.attacking = False
                        
        elif input_id == "x" and not self.player.jumping and self.player.horizontal_velocity == 0 :
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
        
        # Manejar el fade in
        if self.fade_in:
            self.fade_alpha = max(0, self.fade_alpha - self.fade_speed)
            if self.fade_alpha == 0:
                self.fade_in = False

        if self.player.current_health <= 0: 
            self.state_machine.change(
                "game_over"
            )   
            return
        
        delta_time = dt * 1000

        # Quadtree para Colisiones ---
        # 1. Definir los limites del Quadtree (un poco más grande que la vista de la camara)
        quadtree_padding = 100 # Píxeles de padding
        quadtree_bounds = pygame.Rect(
            self.camera.offset_x - quadtree_padding,
            self.camera.offset_y - quadtree_padding,
            settings.VIRTUAL_WIDTH + quadtree_padding * 2,
            settings.VIRTUAL_HEIGHT + quadtree_padding * 2
        )
        
        # 2. Crear/Reconstruir el Quadtree
        # Ajusta max_objects y max_depth según sea necesario.
        self.collision_quadtree = QuadTree(quadtree_bounds, max_objects=7, max_depth=6)


            
        # 3. Insertar objetos solidos en el Quadtree
        for solid_rect in self.solid_objects:
            # Solo insertar si el objeto está dentro o cerca del area del Quadtree
            if quadtree_bounds.colliderect(solid_rect): 
                self.collision_quadtree.insert(solid_rect, "solid", solid_rect)

        # 4. Obtener objetos solidos cercanos al jugador para las colisiones
        # Area de busqueda
        player_query_rect = self.player.king_rect.inflate(self.player.king_rect.width, self.player.king_rect.height) 
        nearby_solid_data = self.collision_quadtree.query(player_query_rect)
        solid_objects_for_player = [data['rect'] for data in nearby_solid_data if data['type'] == "solid"]
        
        # Actualizar jugador, pasando solo los sólidos cercanos
        self.player.update(delta_time, solid_objects_for_player) # Modificado: solo sólidos cercanos

          # Verificar colisión con la llave
        for animated_item in self.animated_items[:]:  # Usamos una copia de la lista para poder modificarla
            if animated_item.name == "key":
                # Crear un rectángulo para la llave
                key_rect = pygame.Rect(
                    animated_item.x,
                    animated_item.y,
                    animated_item.frames[0].get_width(),
                    animated_item.frames[0].get_height()
                )
                
                # Verificar colisión con el jugador
                if self.player.king_rect.colliderect(key_rect):
                    # Aquí puedes agregar la lógica cuando el jugador recoge la llave
                    print("¡Has recogido la llave!")
                    self.animated_items.remove(animated_item)  # Eliminar la llave
                    self.player.has_key = True
  

        # Actualizar enemigos
        for enemy in self.enemies:
            # Obtener solidos cercanos para cada enemigo
            enemy_query_rect = enemy.rect.inflate(500, 500) 
            nearby_solid_data_enemy = self.collision_quadtree.query(enemy_query_rect)
            solid_objects_for_enemy = [data['rect'] for data in nearby_solid_data_enemy if data['type'] == "solid"]
            enemy.update(delta_time, self.player, solid_objects_for_enemy) # Pasa sólidos cercanos
            
            
        # for enemy in self.enemies:
        #     enemy.update(delta_time, self.player, self.solid_objects)
        
        # self.player.update(delta_time, self.solid_objects)
        self.camera.update(self.player.camera_rect, None)   
        # Actualizar objetos animados
        for animated_item in self.animated_items:
            animated_item.update(delta_time)

    # Verifica si el jugador ha llegado a la puerta de salida del nivel.
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
        # surface.fill((0, 0, 0))  # Limpiar la pantalla
        camera_view_rect = pygame.Rect(
            self.camera.offset_x, self.camera.offset_y,
            settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT 
        )
        # Dibujar el mapa
        map_pos = (-self.camera.offset_x, -self.camera.offset_y)
        surface.blit(self.map_image, map_pos)
            
        # # Dibujar objetos animados
        # for animated_item in self.animated_items:
        #     animated_item.draw(surface, (self.camera.offset_x, self.camera.offset_y))
            

        
        # # Dibujar enemigos
        # for enemy in self.enemies:
        #     enemy.draw(surface, (self.camera.offset_x , self.camera.offset_y))
          
        # Dibujar objetos animados (solo los visibles)
        for animated_item in self.animated_items:
            # Obtener el frame actual para determinar sus dimensiones
            if animated_item.frames: # Asegurarse de que la lista de frames no está vacía
                current_sprite_frame = animated_item.frames[animated_item.current_frame]
                item_width = current_sprite_frame.get_width()
                item_height = current_sprite_frame.get_height()
                
                # Crear el rectángulo del item en coordenadas del MUNDO
                item_world_rect = pygame.Rect(animated_item.x, animated_item.y, item_width, item_height)
                
                # Comprobar si este rectángulo es visible en la cámara
                if camera_view_rect.colliderect(item_world_rect):
                    # El método draw ya maneja el offset de la cámara
                    animated_item.draw(surface, (self.camera.offset_x, self.camera.offset_y))
            # else:
                # Podrías tener un manejo para items sin frames si fuera posible,
                # pero según tu init, siempre deberían tener frames.
         # Mostrar indicador de interacción solo si tiene la llave
        if self.player.has_key and self.door_trigger and self.player.king_rect.colliderect(self.door_trigger):
            # Calcular posición del indicador (por ejemplo, arriba del jugador)
            indicator_x = self.player.king_rect.centerx - self.camera.offset_x
            indicator_y = self.player.king_rect.top - 30 - self.camera.offset_y
            
            # Dibujar el indicador (por ejemplo, un triángulo)
            pygame.draw.polygon(surface, (255, 255, 0), [
                (indicator_x, indicator_y),
                (indicator_x - 10, indicator_y + 10),
                (indicator_x + 10, indicator_y + 10)
            ])
            
            # Opcional: Mostrar texto de interacción
            font = pygame.font.Font(None, 24)
            text = font.render("Presiona Z para abrir", True, (255, 255, 255))
            text_rect = text.get_rect(center=(indicator_x, indicator_y - 15))
            surface.blit(text, text_rect)

        # Dibujar enemigos (solo los visibles)
        for enemy in self.enemies:
            # Asumiendo que Enemy tiene un método get_world_rect() o atributos x,y,width,height
            # enemy_world_rect = enemy.get_world_rect() # Idealmente
            # O si tiene .rect que está en coordenadas del mundo:
            
            if hasattr(enemy, 'rect') and camera_view_rect.colliderect(enemy.rect):
                enemy.draw(surface, (self.camera.offset_x, self.camera.offset_y),self.player,self.solid_objects)
            elif hasattr(enemy, 'x') and hasattr(enemy, 'current_surface'): # Si tiene x,y y una superficie actual
                enemy_world_rect = enemy.current_surface.get_rect(topleft=(enemy.x, enemy.y))
                if camera_view_rect.colliderect(enemy_world_rect):
                    enemy.draw(surface, (self.camera.offset_x, self.camera.offset_y),self.player,self.solid_objects)
                      
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
        
        # Aplicar el fade in
        if self.fade_in:
            self.fade_surface.set_alpha(self.fade_alpha)
            surface.blit(self.fade_surface, (0, 0))

        
        # Debug info
        # debug_info = f"Camera: ({self.camera.offset_x}, {self.camera.offset_y})"
        # font = pygame.font.Font(None, 36)
        # text = font.render(debug_info, True, (255, 255, 255))
        # surface.blit(text, (10, 40))