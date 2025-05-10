import pygame
import settings

from src.globalUtilsFunctions import extract_animation_moveset , extract_animation_complex_spritesheet, extract_animation_unique_spritesheet
from src.definitions.enemies import Enemies

class Enemy:
    def __init__(self, x, y, name):
        

        
        # Coldown de persecucióon
        self.pursuit_cooldown = 1000  # Coldown de persecucion e 1seg
        self.last_pursuit_time = 0 

        # Guardamos como se llama el enemigo para poder identificar que enemigo es y asignarle sus estadisticas y animaciones
        self.name = name
        self.scale_factor = Enemies[self.name]["scale_factor"]
        # Variable para correguir su posicion de piso (por el escalado se mueven las cosas en el mapa)
        self.floor_correct = Enemies[self.name]["floor_correct"]
        
        # Sistema de vida
        self.max_health = Enemies[self.name]["max_health"]  # Agregar esto en el diccionario de enemigos
        self.current_health = self.max_health
        self.is_dead = False
        
        # Mejorar la lógica de ataque
        self.attack_range = Enemies[self.name]["attack_range"]  # Rango de ataque en píxeles
        self.detection_range = Enemies[self.name]["detection_range"]  # Rango de detección en píxeles
        self.attack_damage = Enemies[self.name]["attack_damage"]  # Daño que hace el enemigo
        
        # Cargamos las estadisticas para simular el comportamiento cuando esta "herido" el enemigo
        # Ya que estara herido, no se movera y se empujara hacia atras
        self.hurt = False
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.hurt_timer = 0
        self.hurt_duration = 500  # ms
        self.invulnerable_duration = 1000  # ms
        self.knockback_speed = 200 
        self.hurt_frame = 0  # Usaremos el primer frame de "jump" como frame de herido
    
        # posiciones iniciales del enemigo y hacia donde mirara y que animacion tendra  por defecto
        # los numeros magicos son para ajustar la posicion visualmente un poco mejor
        self.x = x - Enemies[self.name]["position_x_correct"]

        self.direction = 1
        self.current_state = "idle"
        self.current_frame = 0
        self.animation_timer = 0
        
        # variable para saber si el enemigo esta atacando o si esta en movimiento
        self.horizontal_velocity = 0
        self.attacking = False
        
        # Cooldown del ataque
        self.attack_cooldown = 500  # En milisegundos (1 segundo)
        self.last_attack_time = 0  # Guardo laultima vez que ataco para descontar el tiempo
        
        # Animaciones (solo un ataque)
        self.animations = {"run": [], "attack": [], "idle": []}
        self.load_animations()
        
        self.scale_factor = 0

        # self.position_x_correct = Enemies[self.name]["position_x_correct"]
        # Aqui empiezan los ajustes para centrar el rectangulo de colision con el sprite y su ancho
        # Rectangulo de colision y offset 
        self.base_rect_width = Enemies[self.name]["base_rect_width"]
        self.base_rect_height = Enemies[self.name]["base_rect_height"]

        # self.scale_factor =  Enemies[self.name]["scale_factor"] 
        # Offset para centrar el rectángulo con el sprite, ya que como el rectangulo se alargara a izquierda o derecha debemos cambia la posicion en x y y de donde inicia
        # son parapetos :p pero era lo mas rapido 
        # Ajustes mañosos 
        self.enemy_rect_offset_x = Enemies[self.name]["enemy_rect_offset_x"] 
        self.enemy_rect_offset_y = Enemies[self.name]["enemy_rect_offset_y"]
       
        # Ajustes para el ataque, ya que el rectangulo de ataque es diferente al de colision normal
        self.attack_rect_width = Enemies[self.name]["attack_rect_width"]
        
        # Aqui ya le agrego la posicion inicial del rectangulo teniendo en cuenta la del player + el offset de control solo para que se vea bonito y sea coherente
        self.pos_rect_offset_x = self.x + self.enemy_rect_offset_x
        self.pos_rect_offset_y = y + self.enemy_rect_offset_y 
        
        # Ahora, la posición inicial del jugador debe considerar el nuevo offset
        # self.x = x - 10
        self.y = y + Enemies[self.name]["extra_custom_offset_y"]
        
        # Inicializar el rectangulo de colision del jugador
        self.rect = pygame.Rect(
            self.pos_rect_offset_x,
            self.pos_rect_offset_y,
            self.base_rect_width,
            self.base_rect_height,
        )

    def check_attack_player(self, player):
        """Verifica si debe golpear al jugador (sin bloquear movimiento)."""
        if self.rect.colliderect(player.king_rect):
            # Si el enemigo ataca y el jugador no es invulnerable ni está herido
            if self.attacking and not player.invulnerable and not player.hurt:
                player.receive_hit(-1 if player.x < self.x else 1,self.attack_damage)
                self.last_pursuit_time = pygame.time.get_ticks()  # Espera antes de volver a perseguir

    def check_collision_with_world(self, solid_objects):
        for solid in solid_objects:
            if self.rect.colliderect(solid):
                # Colisión por la derecha
                if self.direction == 1 and self.rect.right > solid.left:
                    self.x = solid.left - self.rect.width - self.enemy_rect_offset_x
                # Colisión por la izquierda
                elif self.direction == -1 and self.rect.left < solid.right:
                    self.x = solid.right - self.enemy_rect_offset_x
                self.horizontal_velocity = 0
                self.update_rect()

    def receive_hit(self, direction, damage):
        if not self.invulnerable:
            self.horizontal_velocity = 0
            self.hurt = True
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
            self.hurt_timer = pygame.time.get_ticks()
            self.current_state = "idle"  # O el estado para el frame de herido
            self.current_frame = self.hurt_frame
            self.knockback_direction = direction

            # Restarle el daño al enemigo
            self.current_health -= damage
            # Verificar si el enemigo muere
            if self.current_health <= 0:
                self.is_dead = True
                self.current_health = 0

    def load_animations(self):
        # print(self.scale_factor)
        #moveset: (en el settings debemos agregar el mismo nombre para el frame y la textura para que funcione bien)
            # TENEMOS QUE REVISAR LA IMAGEN DEL SPRITESHEET PARA SABER QUE IMAGENES SON LAS QUE SE QUIEREN AGARRAR
            # EN ESTE CASO SE AGARRAN DEL 0 AL 9 (0,1,2,3,4,5,6,7,8,9), cuales son las que se quieren usar depende de la imagen

        if self.name == "Golem":
            print("entro")
            # idle moveset
            enemy_animations = extract_animation_unique_spritesheet("Golem","Idle",self.scale_factor)
            initial_sprite = 0
            sprite_moveset_size = 4
            self.animations["idle"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # run moveset 
            initial_sprite = 0
            sprite_moveset_size = 4
            enemy_animations = extract_animation_unique_spritesheet("Golem","Run",self.scale_factor)
            self.animations["run"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # attack moveset (para los enemigos es un unico ataque)
                      
            initial_sprite = 0
            sprite_moveset_size = 5
            enemy_animations = extract_animation_unique_spritesheet("Golem","Attack",self.scale_factor)
            self.animations["attack"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
        elif self.name == "NightBorne":
            # idle moveset
            initial_sprite = 0
            sprite_moveset_size = 9
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["idle"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # run moveset
            initial_sprite = 24
            sprite_moveset_size = 5
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["run"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # attack moveset (para los enemigos es un unico ataque)
            initial_sprite = 53
            sprite_moveset_size = 6
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["attack"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
        
    def update_rect(self):
  
         # Actualizar tamaño del rectángulo de colision, dependiendo de si esta atacando o no
        rect_width = self.attack_rect_width if self.attacking else self.base_rect_width
        
        # Actualizar la posición del rectángulo según la dirección y el estado de ataque
        if self.attacking:
            if self.direction == 1:  # Mirando a la derecha
                rect_x = self.x + self.enemy_rect_offset_x
            else:  # Mirando a la izquierda
                rect_x = self.x + self.enemy_rect_offset_x - (rect_width - self.base_rect_width)
        else:
            # Si no está atacando, usar la posición base
            rect_x = self.x + self.enemy_rect_offset_x
        
        # Crea el nuevo rectangulo de colision para el player (hay que actualizarlo cada vez que se mueve el player)  
        self.rect = pygame.Rect(
            rect_x, 
            self.pos_rect_offset_y, 
            rect_width , 
            self.base_rect_height
        )
           
    def check_collision_with_player(self, player):
        self.update_rect()
        if self.rect.colliderect(player.king_rect):  
            return True
        else:
            return False

    def apply_knockback(self, delta_time, solid_objects):
        # Calcula el desplazamiento de knockback
        knockback_distance = self.knockback_direction * self.knockback_speed * (delta_time / 1000)
        # new_x = self.x + knockback_distance
        # Simula el nuevo rectángulo
        # rect_width = self.attack_rect_width if self.attacking else self.base_rect_width
        # if self.direction == 1:
        #     rect_x = new_x + self.enemy_rect_offset_x * 2
        # else:
        #     rect_x = new_x + (self.enemy_rect_offset_x * 2 - rect_width) + 10
        # test_rect = pygame.Rect(rect_x, self.y + self.enemy_rect_offset_y, rect_width, self.base_rect_height)
        # Verifica colisión con el mundo
        for solid in solid_objects:
            if self.rect.colliderect(solid):
                return  # No aplicar knockback si colisiona
        # self.x = new_x 
        self.x += knockback_distance

    def update(self, delta_time, player, solid_objects):
        # Si el enemigo está muerto, no actualizar
        if self.is_dead:
            return
        
        # Calculamos la distancia horizontal al jugador
        distance_to_player_x = abs(self.x - player.x)
        
        # Calculamos la diferencia de altura entre el enemigo y el jugador
        height_difference = abs(self.y - player.y)

        # print(f"height_difference: {height_difference}")
        # Definimos un rango de altura aceptable para la detección (ajusta este valor según necesites)
        vision_height_range = 100  # El enemigo solo detectara al jugador si está dentro de este rango de altura
        
        # Verificamos si el jugador está dentro del rango de visión horizontal Y a una altura aceptable
        can_see_player = distance_to_player_x <= self.detection_range 
    

        self.animation_timer += delta_time 
        
        distance_to_player = abs(self.x - player.x)
        collision = self.check_collision_with_player(player)

        # Usa el tiempo global para el cooldown
        current_time = pygame.time.get_ticks()

        # Logica de ataque al jugador (sin bloquear movimiento)
        self.check_attack_player(player)

        # Logica de colision de ataque
        if not self.hurt and not player.hurt:
            if self.rect.colliderect(player.king_rect):
                if player.attacking and not self.attacking:
                    self.receive_hit(-1 if self.x < player.x else 1, player.attack_damage)
                elif self.attacking and not player.attacking:
                    player.receive_hit(-1 if player.x < self.x else 1, self.attack_damage)

        # Si está herido, aplicar knockback y controlar invulnerabilidad
        if self.hurt:
            self.apply_knockback(delta_time, solid_objects)
            if pygame.time.get_ticks() - self.hurt_timer > self.hurt_duration:
                self.hurt = False
                self.current_state = "idle"
                self.current_frame = 0

        if self.invulnerable:
            if pygame.time.get_ticks() - self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
        
        # Estado por defecto
        self.horizontal_velocity = 0

        # Cooldown de persecución tras golpear o ser golpeado
        if current_time - self.last_pursuit_time < self.pursuit_cooldown:
            # Permitir que la animación de ataque termine antes de aplicar el cooldown
            if self.current_state == "attack":
                # Si la animación de ataque no ha terminado, no cambiar de estado
                if self.current_frame < len(self.animations["attack"]) - 1:
                    current_delay = settings.ANIMATIONS_ENEMY_DELAYS[self.name][self.current_state]
                    if self.animation_timer >= current_delay:
                        self.update_animation(delta_time)
                        self.animation_timer = 0
                    self.update_rect()
                    return
            else:
                # Si no está atacando, aplicar el cooldown normalmente
                self.current_state = "idle"
                self.attacking = False
                current_delay = settings.ANIMATIONS_ENEMY_DELAYS[self.name][self.current_state]
                if self.animation_timer >= current_delay:
                    self.update_animation(delta_time)
                    self.animation_timer = 0
                self.horizontal_velocity = 0
                self.update_rect()
                self.check_collision_with_world(solid_objects)
                return
        
        # Logica de ataque
        if distance_to_player <= self.attack_range and can_see_player:
            # ¿Puede atacar?
            if not self.attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
                self.current_state = "attack"
                self.attacking = True
                self.current_frame = 0
                self.last_attack_time = current_time
            elif self.attacking:
                self.current_state = "attack"
                # Cuando termina la animación de ataque, vuelve a idle y espera cooldown
                if self.current_frame == len(self.animations["attack"]) - 1:
                    self.attacking = False
                    self.current_state = "idle"
                    self.current_frame = 0
            else:
                self.current_state = "idle" 
                self.current_frame = 0
        # elif distance_to_player <= self.detection_range and not collision:
        elif can_see_player and not collision:
            if self.current_state != "run":
                self.current_frame = 0
            self.current_state = "run"
            self.direction = -1 if self.x > player.x else 1
            self.horizontal_velocity = self.direction * settings.ENEMY_SPEED
            self.attacking = False
        else:
            if self.current_state != "idle":
                self.current_frame = 0
            self.current_state = "idle"
            self.attacking = False

        # Solo mover si no hay colisión
        if not collision:
            self.x += self.horizontal_velocity * (delta_time / 1000)
        else:
            self.horizontal_velocity = 0

   
        self.check_collision_with_world(solid_objects)
        
        # Current delay es para saber cuanto tiempo tiene que pasar para que se cambie el frame de la animacion
        current_delay = settings.ANIMATIONS_ENEMY_DELAYS[self.name][self.current_state]
        # Actualizar animación
        if self.animation_timer >= current_delay:
            self.update_animation(delta_time)
            self.animation_timer = 0
        
        self.update_rect()
        
        # self.update_animation(delta_time)

    def update_animation(self, delta_time):
        self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_state])

    def draw(self, screen, camera_offset=None):
    
        if self.is_dead:
            return
        
        health_bar_width = 30
        health_bar_height = 4
        health_ratio = self.current_health / self.max_health
        # Posición de la barra de vida
        bar_x = self.x - camera_offset[0] - health_bar_width/2
        bar_y = self.y - camera_offset[1] 
        
        # Fondo de la barra (rojo)
        pygame.draw.rect(screen, (255, 0, 0), 
                           (bar_x, bar_y, health_bar_width, health_bar_height))
            
        # Vida actual (verde)
        pygame.draw.rect(screen, (0, 255, 0), 
                           (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))
        
        if self.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        current_surface = self.animations[self.current_state][self.current_frame]
        
        if self.direction == -1:
            current_surface = pygame.transform.flip(current_surface, True, False)
            
        offset = camera_offset if camera_offset else (0, 0)
        # y_render = offset[1] + self.enemy_rect_offset_y * 3 # Aplica el offset vertical
        screen.blit(current_surface, (self.x - offset[0], self.y - offset[1] - self.floor_correct))
        
        # Dibujar el rectángulo de colisión (en rojo)
        rect_to_draw = pygame.Rect(
            self.rect.x - offset[0],
            self.rect.y - offset[1],
            self.rect.width,
            self.rect.height,
        )
        pygame.draw.rect(screen, (255, 0, 0), rect_to_draw, 2)