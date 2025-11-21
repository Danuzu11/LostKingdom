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
from src.SnowEffect import SnowEffect
from src.EnemyPool import EnemyPool

class PlayState(BaseState):
    
    def enter(self, **params: dict):
        
        # Sistema de culling mejorado
        self.visible_enemies = []
        self.visible_animated_items = []
        self.culling_padding = 100  # Píxeles de padding para suavizar transiciones
        
        # Sistema de Object Pooling para enemigos
        self.enemy_pool = EnemyPool(max_size=20)
        
        # Variables para el fade in
        self.fade_alpha = 255
        self.fade_surface = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.fade_speed = 3
        self.door_trigger = None
        self.fade_in = True
        self.fade_out = False
        # settings.SOUNDS["relaxtheme"].stop()
        # settings.SOUNDS["relaxtheme"].play(loops=-1) 
        # settings.SOUNDS["relaxtheme"].set_volume(1)
        
        # Velocidad más lenta para el fade out
        self.fade_out_speed = 0.7
        
        # Para saber porque se esta haciendo el fade out
        self.fade_out_reason = None 
        
         # Lista de niveles disponibles
        self.available_levels = list(settings.LEVELS.keys())
        self.current_level_index = 0  
        
        # Inicializar el efecto de nieve
        self.snow_effect = SnowEffect(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)

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
            self.door_trigger = params.get("door_trigger", None)
            self.doors = params.get("doors",None)
            
            if self.current_level_index == 2:
                settings.SOUNDS["principal_theme"].stop()
                settings.SOUNDS["deepgrowl"].play()  # Reproducir música de jefe si es el tercer nivel
                settings.SOUNDS["boss"].play(-1)  # Reproducir música de jefe si es el tercer nivel
                
            level_name = params.get("level_name")
            
            if level_name:
                self.load_level(level_name)

        else:  # Si no se pasan parametros, inicializar desde cero
            self.transition = True
            self.current_level_index = 0
            self.load_level(self.available_levels[self.current_level_index])
            
    # Carga el nivel en el que estamos (el mapa correspondiente al nivel que le mandemos)
    # Aqui es donde se precargan los objetos estaticos y los objetos animados, solidos y enemigos antes de renderizarlos
    def load_level(self, level_name):
  
        # Limpiar objetos 
        self.solid_objects = []
        self.animated_items = []
        self.enemies = []
        self.mask_objects = []
        self.object_animations = {}
        self.static_decorations = {}
        self.doors = []

        # Cargar nuevo nivel, el cual es el mapa correspondiente al nivel que le mandemos con su rectangulo de colision
        self.current_tile_map = TileMap(level_name)
        self.map_image = self.current_tile_map.make_map()
        self.map_rect = self.map_image.get_rect()
        
        # Variables para controlar la transicion entre niveles con el fade in y fade out
        self.transition = True
            
        # Escalar el mapa si el mapa creado es mucho mas peque;o que la pantalla
        scale_factor = settings.VIRTUAL_HEIGHT / self.current_tile_map.height
            
        # El tama;o maximo de altura sera 16 en tile (relacion por la ventana que tenemos (revisar settings.py ))
        max_tile_height = 16
        max_pixel_height = max_tile_height * self.current_tile_map.tmx_data.tileheight
            
        # Si el mapa es mas grande no hara ningun reescalado
        if self.current_tile_map.height > max_pixel_height:
            scale_factor = 1
            settings.SCALE_FACTOR = 1
        else:
            # Si el mapa es mas peque;o que la ventana, se escala el mapa para que se vea mas grande
            settings.SCALE_FACTOR = 1.4
      
        # Inicializar la cámara, con el tama;o total del mapa para que se pueda ver todo y se mueva en el
        self.camera = Camera()
        self.camera.set_world_size(self.map_image.get_width(), self.map_image.get_height())

        # Inicializar el jugador en 0.0 si no se encuentra el objeto player en el mapa
        self.player_x, self.player_y = 0, 0
 

        # Cargar animaciones de objetos animados
        for spritesheet_name, spritesheet_data in settings.ANIMATED_DECORATIONS.items():

            # Obtenemos la textura y los frames de cada animacion
            spritesheet = spritesheet_data["texture"]
            frames = spritesheet_data["frames"]
            animation_frames = []

            # Recorremos los frames guardados para cada animacion y le creamos sus superficies a cada frame
            for frame in frames:
                surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
                surface.blit(spritesheet, (0, 0), frame)

                # Guardamos la superficie de cada frame en la lista de frames de la animacion
                animation_frames.append(surface)

            # Guardamos la lista de frames de la animacion en el diccionario de animaciones
            self.object_animations[spritesheet_name] = animation_frames

        # Cargar los objetos (Todo lo que creas en la capa "Capa de objetos en Tiled") del mapa  
        for objects in self.current_tile_map.tmx_data.objects:

            # Detecta objeto para jugador y saber donde colocarlo en el mapa
            if objects.name == "Player":
                self.player_x = objects.x * scale_factor
                self.player_y = objects.y * scale_factor

            # Detecta objetos solidos del mundo, como paredes, bloques, etc.
            elif objects.name == "obstacle" :
                solid_rect = pygame.Rect(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    objects.width * scale_factor,
                    objects.height * scale_factor,
                )
                self.solid_objects.append(solid_rect)
            
            # Detecta objetos que van en la puerta de salida del nivel, lo usamos para saber cuando el jugador esta frente a la puerta
            elif objects.name == "door_trigger":
                self.door_trigger = pygame.Rect(
                            objects.x * scale_factor,
                            objects.y * scale_factor,
                            objects.width * scale_factor,
                            objects.height * scale_factor,
                )
                print(f"Door trigger cargado: {self.door_trigger}")
                # NO agregar a solid_objects ya que door_trigger no es un objeto sólido
            
            # Detecta objetos animados del mundo, como antorchar fogatas, etc.
            elif objects.name in settings.ANIMATED_DECORATIONS:
                animated_item = AnimatedItem(
                    objects.x * scale_factor - settings.ANIMATED_DECORATIONS[objects.name]["correctionX"],
                    objects.y * scale_factor - settings.ANIMATED_DECORATIONS[objects.name]["correctionY"],
                    self.object_animations[objects.name],
                    animation_delay=150,
                    name = objects.name
                )
                self.animated_items.append(animated_item)

            # Detecta objetos animados del mundo, como antorchar fogatas, etc.
            elif objects.name == "door":
                # Obtener los datos de la decoración estática
                decoration_data = settings.STATIC_DECORATIONS["DoorClosed"]
                
                # Crear un rectángulo para la decoración
                decoration_rect = pygame.Rect(
                    objects.x * scale_factor - decoration_data["correctionX"],
                    objects.y * scale_factor - decoration_data["correctionY"],
                    decoration_data["texture"].get_width() ,
                    decoration_data["texture"].get_height() 
                )
                
                # Guardar la puerta en el array de puertas
                self.doors.append({
                    "rect": decoration_rect,
                    "texture": decoration_data["texture"],
                    "frames": decoration_data["frames"]
                })

            # Aqui empezamos a cargar los enemigos , debemos poner el mismo nombre del enemigo tanto en settings como en Tiled
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
            elif objects.name == "MechaGolem":
                enemy = Enemy(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    "MechaGolem",
                )
                self.enemies.append(enemy) 
            elif objects.name == "Executoner":
                enemy = Enemy(
                    objects.x * scale_factor,
                    objects.y * scale_factor,
                    "Executoner",
                )
                self.enemies.append(enemy)      
            # FIN DE LOS ENEMIGOS
            
             
            # Esta apartado es especial , se usa para cargar lo que coloques objetos como mascaras (Por encima del jugador) en Tiled                      
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
            if self.current_tile_map.height > max_pixel_height:
                self.player.jump_offset = 1.03
                self.player.scale_factor = 1.3
            self.player = Player(self.player_x, self.player_y)
        else:
            # Actualizar la posición del jugador existente
            self.player.x = self.player_x
            self.player.y = self.player_y
            
            if self.current_tile_map.height > max_pixel_height:
                self.player.jump_offset = 1.03
                self.player.scale_factor = 1.3
                self.player.load_animations()
                self.player.load_death_animation()
            
            
        # Inicializar el jugador
        # self.player = Player(self.player_x, self.player_y)   
    
        # Inicializamos que el jugador no tiene llave para avanzar al siguiente nivel
        self.player.has_key = False
       
    # Detecta cuando el usuario presiona alguna tecla (para agregar nuevas teclas ir a settings.py)
    def on_input(self, input_id: str, input_data: InputData) -> None:  
        new_state = "idle"     

        # if input_id == "enter" and input_data.pressed:
        #     self.state_machine.change("menu")  # Cambiar al estado de menú
 
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
                map_image=self.map_image,
                door_trigger=self.door_trigger,
                doors = self.doors
            )

        # Verifica si se presiono la tecla F para interactuar por ahora solo con la puerta
        if input_id == "f":

            # Avanzar al siguiente nivel, solo si el jugador tiene la llave y esta frente a la puerta
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

                    # Cambiar al nuevo nivel manteniendo el estado
                    self.state_machine.change(
                        "play",
                        previous_state=self,
                        **current_state  # Pasamos todos los datos del estado actual
                    )

        # Mueve a la izquierda                     
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

        # Mueve a la derecha
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
       
        # Detecta la tecla de salto con sistema de buffer mejorado
        if input_id == "jump":
            if input_data.pressed:
                # Añadir input al buffer
                self.player.input_buffer.add_input("jump")
                # Intentar ejecutar inmediatamente
                if self.player.handle_buffered_input("jump", pygame.time.get_ticks()):
                    new_state = "jump"
                        
        # Sistema de ataques mejorado con detección de primer tick
        elif input_id == "x":
            if input_data.pressed:
                # Solo detectar el primer tick, no mantener presionado
                if self.handle_attack_input():
                    new_state = "attack"
        
        # Verifica si se cambio la animacion del jugador  , si ocurre esto se reinicia el timer de la animacion y empieza la siguiente animacion            
        if new_state != self.player.current_state:
            self.player.current_state = new_state
            self.player.animation_timer = 0    

    # Actualiza el tiempo y los estados del juego, es el que permite que todo avance y se mueva          
    def update(self, dt: float) -> None:
        
        # Sistema de culling mejorado - solo procesar objetos visibles
        self.update_visible_objects()

        # Manejar el fade in
        if self.fade_in:
            self.fade_alpha = max(0, self.fade_alpha - self.fade_speed)
            if self.fade_alpha == 0:
                self.fade_in = False

        # Cuando el jugador muera, se cambia al estado de game over, despues de terminar la animacion de muerte
        if self.player.current_health <= 0 and self.player.death_animation_completed: 
            self.state_machine.change(
                "game_over"
            )   
            return
                  
        # Manejar el fade out
        if self.fade_out:
            self.fade_alpha = min(255, self.fade_alpha + self.fade_out_speed)
            if self.fade_alpha == 255:
                self.fade_out = False
                if self.fade_out_reason == "next_level":
                    print("siguiente nivel")
                elif self.fade_out_reason == "victory":
                    self.state_machine.change("outro")
              
        # Verificar si el jefe final ha sido derrotado
        if self.current_level_index == 2:
        # if self.current_level_index == len(self.available_levels) - 1: 
            boss_defeated = True
            for enemy in self.enemies:
                if enemy.name == "Minotaur" and enemy.current_health > 0: 
                    boss_defeated = False
                    break
            
            if boss_defeated and not self.fade_out:
                self.fade_out = True
                self.fade_out_reason = "victory"
                self.fade_alpha = 0
        


        # Convertimos el tiempo de delta a milisegundos para irlo aumentando, luego de las verificaciones de fade in y fade out y muerte
        delta_time = dt * 1000
        
        # self.snow_effect.update(delta_time)
        self.snow_effect.update(delta_time, (self.camera.offset_x, self.camera.offset_y))
        # Quadtree para Colisiones y optimizar el rango de busqueda de objetos de colision ---

        # 1. Definir los limites del Quadtree (un poco más grande que la vista de la camara)
        quadtree_padding = 100 # Píxeles de padding
        quadtree_bounds = pygame.Rect(
            self.camera.offset_x - quadtree_padding,
            self.camera.offset_y - quadtree_padding,
            settings.VIRTUAL_WIDTH + quadtree_padding * 2,
            settings.VIRTUAL_HEIGHT + quadtree_padding * 2
        )
        
        # 2. Crear/Reconstruir el Quadtree con parámetros dinámicos
        # Parámetros dinámicos basados en la cantidad de objetos para optimizar rendimiento
        object_count = len(self.solid_objects)
        if object_count < 10:
            max_objects = 4
            max_depth = 3
        elif object_count < 50:
            max_objects = 6
            max_depth = 4
        else:
            max_objects = 8
            max_depth = 5
        
        self.collision_quadtree = QuadTree(quadtree_bounds, max_objects=max_objects, max_depth=max_depth)
 
        # Insertamos los objetos solidos en el Quadtree
        for solid_rect in self.solid_objects:
            # Solo insertar si el objeto está dentro o cerca del area del Quadtree
            if quadtree_bounds.colliderect(solid_rect): 
                self.collision_quadtree.insert(solid_rect, "solid", solid_rect)

        # Obtenemos los objetos solidos cercanos al jugador para las colisiones
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
                    settings.SOUNDS["door_open"].play()
                    self.animated_items.remove(animated_item)  # Eliminar la llave
                    self.player.has_key = True
  
        # Actualizar enemigos (solo los visibles)
        for enemy in self.visible_enemies:
            # Obtener solidos cercanos para cada enemigo
            enemy_query_rect = enemy.rect.inflate(500, 500) 
            nearby_solid_data_enemy = self.collision_quadtree.query(enemy_query_rect)
            solid_objects_for_enemy = [data['rect'] for data in nearby_solid_data_enemy if data['type'] == "solid"]
            enemy.update(delta_time, self.player, solid_objects_for_enemy)
        
        # Limpiar enemigos muertos del mapa (sistema original)
        enemies_to_remove = []
        for enemy in self.enemies:
            if enemy.is_dead and enemy.death_animation_completed:
                enemies_to_remove.append(enemy)
        
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)
        
        # Limpiar enemigos muertos del pool
        self.enemy_pool.cleanup_dead_enemies() 
            
        # Actualiza la posicion de la camara
        self.camera.update(self.player.camera_rect, None)   
        
        # Actualizar objetos animados (solo los visibles)
        for animated_item in self.visible_animated_items:
            animated_item.update(delta_time)

    # Renderizar el estado de juego
    def render(self, surface):

        # Creamos el rectangulo de la camara para saber que parte del mapa se va a renderizar
        camera_view_rect = pygame.Rect(
            self.camera.offset_x, self.camera.offset_y,
            settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT 
        )

        # Dibujar el mapa
        map_pos = (-self.camera.offset_x, -self.camera.offset_y)
        surface.blit(self.map_image, map_pos)
            
   
        # Dibujar objetos animados (solo los visibles - sistema de culling mejorado)
        for animated_item in self.visible_animated_items:
            # Obtener el frame actual para determinar sus dimensiones
            if animated_item.frames: 
                current_sprite_frame = animated_item.frames[animated_item.current_frame]
                item_width = current_sprite_frame.get_width()
                item_height = current_sprite_frame.get_height()
                
                # Crear el rectángulo del item en coordenadas del MUNDO
                item_world_rect = pygame.Rect(animated_item.x, animated_item.y, item_width, item_height)
                
                # Comprobar item animado se esta viendo en la camara
                if camera_view_rect.colliderect(item_world_rect):
                    # Dibujamos el objeto animado en la pantalla ya con el offset de la camara
                    animated_item.draw(surface, (self.camera.offset_x, self.camera.offset_y))

 
        # Renderizar las puertas
        for door in self.doors:
            if camera_view_rect.colliderect(door["rect"]):
                screen_x = door["rect"].x - self.camera.offset_x
                screen_y = door["rect"].y - self.camera.offset_y
                # Si el jugador tiene la llave, usar la textura de puerta abierta
                if self.player.has_key:
                    surface.blit(settings.STATIC_DECORATIONS["DoorOpen"]["texture"], (screen_x, screen_y))
                else:
                    surface.blit(door["texture"], (screen_x, screen_y))

        # Mostrar indicador de interacción solo si tiene la llave
        if self.player.has_key and self.door_trigger and self.player.king_rect.colliderect(self.door_trigger):
            surface = self.draw_door_indicator("Presiona F para ENTRAR", surface, (255, 255, 0), (255, 255, 255))

        # Si el jugador no tiene la llave, se muestra un indicador de que necesita la llave para abrir la puerta
        elif not self.player.has_key and self.door_trigger and self.player.king_rect.colliderect(self.door_trigger):
            surface = self.draw_door_indicator("Necesitas la llave para abrir", surface, (255, 0, 0), (255, 255, 255))

        # Dibujar enemigos (solo los visibles - sistema de culling mejorado)
        for enemy in self.visible_enemies:
            # Si el enemigo tiene un rectangulo, se dibuja en la pantalla
            if hasattr(enemy, 'rect'):
                # Dibujamos el enemigo en la pantalla ya con el offset de la camara
                enemy.draw(surface, (self.camera.offset_x, self.camera.offset_y),self.player,self.solid_objects)
        
        # Debug: Mostrar información de enemigos
        # if len(self.visible_enemies) > 0:
        #     debug_info = f"Enemigos visibles: {len(self.visible_enemies)}/{len(self.enemies)}"
        #     font = pygame.font.Font(None, 24)
        #     text = font.render(debug_info, True, (255, 255, 255))
        #     surface.blit(text, (10, 10))
            
                      
        # Dibujar al jugador
        player_screen_x = self.player.x - self.camera.offset_x
        player_screen_y = self.player.y - self.camera.offset_y
        self.player.render(surface, (player_screen_x, player_screen_y))
        
        # Renderizar la máscara con el offset de la cámara
        self.current_tile_map.render_mask(surface, (self.camera.offset_x, self.camera.offset_y))
            
        # DRAW PARA DEBUGS

        #Dibujar los objetos sólidos
        # for solid in self.solid_objects:
        #     rect_with_offset = pygame.Rect(
        #         solid.x - self.camera.offset_x,
        #         solid.y - self.camera.offset_y,
        #         solid.width,
        #         solid.height
        #     )
        #     pygame.draw.rect(surface, (255, 0, 0), rect_with_offset, 2)
        
        # Debug info
        # debug_info = f"Camera: ({self.camera.offset_x}, {self.camera.offset_y})"
        # font = pygame.font.Font(None, 36)
        # text = font.render(debug_info, True, (255, 255, 255))
        # surface.blit(text, (10, 40))

        # FIN DE DLINEAS DE DEBUGS

        # Renderizar el efecto de nieve
        self.snow_effect.render(surface, (self.camera.offset_x, self.camera.offset_y))

        # Aplicar el fade in O fade out
        if self.fade_in or self.fade_out:
            self.fade_surface.set_alpha(self.fade_alpha)
            surface.blit(self.fade_surface, (0, 0))

        # FIN DE DRAW PARA DEBUGS

    def update_visible_objects(self):
        """Sistema de culling mejorado - solo procesar objetos visibles."""
        # Crear rectángulo de cámara expandido para suavizar transiciones
        camera_rect = pygame.Rect(
            self.camera.offset_x - self.culling_padding,
            self.camera.offset_y - self.culling_padding,
            settings.VIRTUAL_WIDTH + self.culling_padding * 2,
            settings.VIRTUAL_HEIGHT + self.culling_padding * 2
        )
        
        # Filtrar enemigos visibles (combinando enemigos del mapa y del pool)
        self.visible_enemies = []
        # Usar enemigos del mapa (cargados desde TMX) y del pool
        all_enemies = self.enemies + self.enemy_pool.get_active_enemies()
        for enemy in all_enemies:
            if self.should_render_object(enemy.rect, camera_rect):
                self.visible_enemies.append(enemy)
        
        # Filtrar objetos animados visibles
        self.visible_animated_items = []
        for animated_item in self.animated_items:
            # Verificar que el objeto tiene 'rect' antes de usarlo
            if hasattr(animated_item, 'rect'):
                # Las llaves siempre son visibles para que se puedan recoger
                if animated_item.name == "key" or self.should_render_object(animated_item.rect, camera_rect):
                    self.visible_animated_items.append(animated_item)
    
    def should_render_object(self, obj_rect, camera_rect):
        """Determina si un objeto debe ser renderizado basado en la cámara."""
        return camera_rect.colliderect(obj_rect)
    

    # Dibuja el indicador cuando el jugador esta frente a la puerta
    def draw_door_indicator(self, text , surface , colorPolygon , colorText ):
        indicator_x = self.player.king_rect.centerx - self.camera.offset_x
        indicator_y = self.player.king_rect.top - 30 - self.camera.offset_y
        
        # Dibujar el indicador (por ejemplo, un triangulo)
        pygame.draw.polygon(surface, colorPolygon, [
            (indicator_x, indicator_y ),
            (indicator_x - 10, indicator_y + 10),
            (indicator_x + 10, indicator_y + 10)
        ])
            
        # Mostramos el texto de que necesita la llave para abrir la puerta
        font = settings.FONTS["small"]
        text = font.render(text, True, colorText)
        text_rect = text.get_rect(center=(indicator_x, indicator_y - 15))
        surface.blit(text, text_rect)

        return surface
    
    # Método para manejar inputs de ataque con detección de primer tick
    def handle_attack_input(self):
        """Maneja inputs de ataque detectando solo el primer tick."""
        if self.player.is_dead or self.player.hurt:
            return False
            
        # Si no está atacando, iniciar nuevo ataque
        if not self.player.attacking:
            # Iniciar nuevo combo
            self.player.attacking = True
            self.player.current_combo = 1
            self.player.current_frame = 0
            self.player.combo_timer = 0
            
            # Reproducir sonido de ataque
            random_attack = 1
            settings.SOUNDS[f"slash{random_attack}"].stop()
            settings.SOUNDS[f"slash{random_attack}"].play()
            
            return True
        else:
            # Si ya está atacando, verificar si se puede continuar el combo
            attack_frames = self.player.attack_moveset[f"attack{self.player.current_combo}"]
            
            # Verificar si estamos cerca del final del ataque actual
            if self.player.current_frame >= len(attack_frames) - 2:
                # Avanzar al siguiente combo
                if self.player.current_combo < self.player.max_combo:
                    self.player.current_combo += 1
                else:
                    self.player.current_combo = 1
                
                self.player.current_frame = 0
                self.player.combo_timer = 0
                
                # Reproducir sonido de ataque
                random_attack = 1
                settings.SOUNDS[f"slash{random_attack}"].stop()
                settings.SOUNDS[f"slash{random_attack}"].play()
                
                return True
            else:
                # No se puede continuar el combo aún
                return False
        