import pygame
import settings

from src.globalUtilsFunctions import extract_animation_moveset , extract_animation_complex_spritesheet, extract_animation_unique_spritesheet
from src.definitions.enemies import Enemies

class Enemy:
    def __init__(self, x, y, name):
        
        # Agregar estado de muerte
        self.death_animation_completed = False
        self.death_animation_timer = 0
        self.start_death = False
        # TENGAMOS EN CUENTA QUE PARA AGREGAR MAS ENEMIGOS DEBEMOS AGREGAR LA DEFINICIONES EN ENEMIES.PY
        # ESTO PARA DEFINIR SUS VALORES DE VIDA ESCALA Y CORRECIONES DE POSICION
          
        # Coldown de persecucioon
        self.pursuit_cooldown = 1000  # 1seg
        self.last_pursuit_time = 0 
        self.attacking_animation_started = False
        
        # Guardamos como se llama el enemigo para poder identificar que enemigo es y asignarle sus estadisticas y animaciones
        self.name = name
        self.velocity = Enemies[self.name]["speed"]
        self.scale_factor = Enemies[self.name]["scale_factor"]
        # Variable para correguir su posicion de piso (por el escalado se mueven las cosas en el mapa)
        self.floor_correct = Enemies[self.name]["floor_correct"]
        
        # Sistema de vida
        self.max_health = Enemies[self.name]["max_health"]  
        self.current_health = self.max_health
        self.is_dead = False
        
        # Mejorar la logica de ataque
            # Rango de ataque 
        self.attack_range = Enemies[self.name]["attack_range"]  
            # Rango de detección 
        self.detection_range = Enemies[self.name]["detection_range"]  
            # Daño que hace el enemigo
        self.attack_damage = Enemies[self.name]["attack_damage"]  
        
        # Cargamos las estadisticas para simular el comportamiento cuando esta "herido" el enemigo
        # Ya que estara herido, no se movera y se empujara hacia atras
        self.hurt = False
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.hurt_timer = 0
        self.hurt_duration = 500  # ms
        self.invulnerable_duration = 1000  # ms
        self.knockback_speed = 200 
        self.hurt_frame = 0  # Frame de herido
    
        # posiciones iniciales del enemigo y hacia donde mirara y que animacion tendra  por defecto
        # los numeros magicos son para ajustar la posicion visualmente un poco mejor
        self.x = x - Enemies[self.name]["position_x_correct"]

        # Determinamos su estado inicial y su direccion, que animacion tendra por defecto y empezara de 0        self.direction = 1
        self.direction = -1
        self.current_state = "idle"
        self.current_frame = 0
        self.animation_timer = 0
        
        # variable para saber si el enemigo esta atacando o si esta en movimiento
        self.horizontal_velocity = 0
        self.attacking = False
        
        # Cooldown del ataque
        self.attack_cooldown = 500  # 0.5 segundos
        self.last_attack_time = 0  # Guardo laultima vez que ataco para descontar el tiempo
        
        # Animaciones (solo un ataque)
        self.animations = {"run": [], "attack": [], "idle": []}
        self.load_animations()
        
        
        # self.scale_factor = 0

        
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
        
        self.initial_x = self.x
        # Variables para el control de caida de los enemigos
        self.on_ground = True
        self.waiting = False
        self.wait_timer = 0
        self.initial_x = self.x
    
    # Verifica si debe golpear al jugador (sin bloquear movimiento)   
    def check_attack_player(self, player):
        if self.rect.colliderect(player.king_rect):
            # Si el enemigo ataca y el jugador no es invulnerable ni está herido
            if self.attacking and not player.invulnerable and not player.hurt:
                player.receive_hit(-1 if player.x < self.x else 1,self.attack_damage)
                self.last_pursuit_time = pygame.time.get_ticks()  # Espera antes de volver a perseguir
    
    # Verifica colisiones con el mundo  
    def check_collision_with_world(self, solid_objects: list):

        for solid in solid_objects:
            if self.rect.colliderect(solid):
                # Calculamos las distancias a cada borde del sólido
                # (desde el rect del enemigo al borde del sólido)
                dist_top = abs(self.rect.bottom - solid.top)
                dist_bottom = abs(self.rect.top - solid.bottom)
                dist_left = abs(self.rect.right - solid.left) 
                dist_right = abs(self.rect.left - solid.right) 

                min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

                # Colisión desde la DERECHA del enemigo 
                if min_dist == dist_left and self.horizontal_velocity > 0:
                    print(f"{self.name} colisión por la derecha del enemigo")
                    self.x = solid.left - (self.enemy_rect_offset_x + self.base_rect_width)
                    self.horizontal_velocity = 0

                # Colisión desde la IZQUIERDA del enemigo 
                elif min_dist == dist_right and self.horizontal_velocity < 0:
                    print(f"{self.name} colisión por la izquierda del enemigo")
                    self.x = solid.right - self.enemy_rect_offset_x
                    self.horizontal_velocity = 0
                
                self.update_rect()
                # break
            
    # Verifica si el enemigo recibe un golpe y no esta invulnerable
    # Si el enemigo recibe un golpe se le aplica knockback y da;o
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

    # Carga las animaciones del enemigo, y las asigna a un array de animaciones
    # Dependiendo de la animacion que se quiera usar
    def load_animations(self):
        # print(self.scale_factor)
        #moveset: (en el settings debemos agregar el mismo nombre para el frame y la textura para que funcione bien)
            # TENEMOS QUE REVISAR LA IMAGEN DEL SPRITESHEET PARA SABER QUE IMAGENES SON LAS QUE SE QUIEREN AGARRAR
            # EN ESTE CASO SE AGARRAN DEL 0 AL 9 (0,1,2,3,4,5,6,7,8,9), cuales son las que se quieren usar depende de la imagen

        # Usamos extract_animation_unique_spritesheet cuando el spritesheet esta enfocado en una sola animacion
        # Ejmplo ataque, idle, etc , entonces le pasa el nombre del enemigo y el nombre de la animacion
        
        # Y Usamos extract_animation_complex_spritesheet cuando el spritesheet tiene varias animaciones en una sola imagen
        # Es decir que esten combinadas en una sola imagen, entonces le pasamos el nombre del enemigo y el rango de sprites q
        # que queremos usar , tengamos en cuenta que estas funciones solo "extraen los recortes" que hace el metodo de frame en settings
        
        # visualmente en setting asignamos el tam;ao de la imagen y el ancho y alto del sprite y el ira "recortando" la imagen con esa altura y ancho
        # e ira formando un array de imagenes o sprites , es un pelo dificil de entender pero visualmente es facil cuando agarren el hilo 
        if self.name == "Golem":
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
            
            #animacion de muerte
            initial_sprite = 0
            sprite_moveset_size = 7
            enemy_animations = extract_animation_complex_spritesheet("Golem_DeathB", self.scale_factor)
            self.animations["death"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
        
        elif self.name == "Executoner":
            # idle moveset
            enemy_animations = extract_animation_unique_spritesheet("Executoner","Idle",self.scale_factor)
            initial_sprite = 0
            sprite_moveset_size = 4
            self.animations["idle"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # run moveset 
            initial_sprite = 0
            sprite_moveset_size = 7
            enemy_animations = extract_animation_unique_spritesheet("Executoner","Run",self.scale_factor)
            self.animations["run"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # attack moveset (para los enemigos es un unico ataque)           
            initial_sprite = 0
            sprite_moveset_size = 12
            enemy_animations = extract_animation_unique_spritesheet("Executoner","Attack",self.scale_factor)
            self.animations["attack"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            #animacion de muerte
            initial_sprite = 0
            sprite_moveset_size = 18
            enemy_animations = extract_animation_complex_spritesheet("ExecutoreDeathB", self.scale_factor)
            self.animations["death"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))  
                                 
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
            
            #animacion de muerte
            initial_sprite = 92
            sprite_moveset_size = 22
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["death"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
              
        elif self.name == "Minotaur":
            # idle moveset
            initial_sprite = 0
            sprite_moveset_size = 15
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["idle"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # run moveset
            initial_sprite = 16
            sprite_moveset_size = 11
            # initial_sprite = 20
            # sprite_moveset_size = 27
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["run"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # attack moveset
            initial_sprite = 33
            sprite_moveset_size = 14
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["attack"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))

            #animacion de muerte
            initial_sprite = 60
            sprite_moveset_size = 11  
            enemy_animations = extract_animation_complex_spritesheet("Death", self.scale_factor)
            self.animations["death"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
        
        elif self.name == "MechaGolem":
            # idle moveset
            initial_sprite = 0
            sprite_moveset_size = initial_sprite + 4
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["idle"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # run moveset
            initial_sprite = 60
            sprite_moveset_size = 9
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["run"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            # attack moveset
            initial_sprite = 40
            sprite_moveset_size = 7
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["attack"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
            
            #animacion de muerte
            initial_sprite = 70
            sprite_moveset_size = 13
            enemy_animations = extract_animation_complex_spritesheet(self.name,self.scale_factor)
            self.animations["death"] = extract_animation_moveset(enemy_animations, (initial_sprite, sprite_moveset_size))
        

                    
    # Actualiza el rectangulo de colision
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

    # Verifica la colision con el jugador
    def check_collision_with_player(self, player):
        self.update_rect()
        if self.rect.colliderect(player.king_rect): 
            print("colisiono con el jugador") 
            return True
        else:
            return False

    # Aplica el knockback al enemigo, que basicamente es un desplazamiento en la direccion opuesta al golpe
    # Y ademas de esto verifica si el enemigo colisiona con el mundo y no se mueve si colisiona
    def apply_knockback(self, delta_time, solid_objects):
        # Calcula el desplazamiento de knockback
        knockback_distance = self.knockback_direction * self.knockback_speed * (delta_time / 1000)

        # # # Verificar si hay piso debajo
        has_ground = self.check_ground(solid_objects)
        if has_ground == False:
            return
        # Verifica colisión con el mundo
        for solid in solid_objects:
            if self.rect.colliderect(solid):
                return  # No aplicar knockback si colisiona
        self.x += knockback_distance
        self.update_rect()
    
        
    def check_ground(self, solid_objects):
        """
        Verifica si hay piso en la dirección del movimiento del enemigo
        """
        # Crear un rectángulo de detección adelante del enemigo en la dirección de movimiento
        ground_check = pygame.Rect(
            self.rect.x + ((self.rect.width + 10) * self.direction)  ,  # Posicion adelante en la dirección de movimiento
            self.rect.bottom ,
            25,
            25  # Altura pequeña para la deteccion
        )
        
        # Verificar si hay algún objeto sólido debajo
        for solid in solid_objects:
            if ground_check.colliderect(solid):
                return True
        return False
    
    def update(self, delta_time, player, solid_objects):
        # Si el enemigo esta muerto, no actualizar
        
        if self.is_dead:      
            if not self.start_death:
                settings.DEATH_SOUNDS[self.name].play()
                settings.DEATH_SOUNDS[self.name].set_volume(1.0)
                self.start_death = True
                 
            if not self.death_animation_completed:
                self.current_state = "death"
                self.death_animation_timer += delta_time
                
                # Actualizar la animación de muerte
                current_delay = settings.ANIMATIONS_ENEMY_DELAYS[self.name]["death"]
                if self.death_animation_timer >= current_delay:
                    self.update_animation(delta_time)
                    self.death_animation_timer = 0
                    
                    # Verificar si la animación de muerte ha terminado
                    if self.current_frame >= len(self.animations["death"]) - 1:
                        self.death_animation_completed = True
                 
     
            return
         
        self.animation_timer += delta_time 
        # self.waiting = False

        # Verificar si hay piso debajo
        has_ground = self.check_ground(solid_objects)

        # Usa el tiempo global para el cooldown
        current_time = pygame.time.get_ticks()
    
        # Logica de ataque al jugador (sin bloquear movimiento)
        self.check_attack_player(player)
        # Si esta herido, aplicar knockback y controlar invulnerabilidad
        if self.hurt:
            self.apply_knockback(delta_time, solid_objects)
            if pygame.time.get_ticks() - self.hurt_timer > self.hurt_duration:
                self.hurt = False
                # self.current_state = "idle"
                # self.current_frame = 0
            self.update_rect() # Actualizar rect por si el knockback cambió x
            
            if self.current_state != "idle": # O un estado "hurt_idle" si lo tienes
                self.current_state = "idle"
                self.current_frame = 0
                self.animation_timer = 0
            
            self.update_animation(delta_time) # Solo para que la anim de idle/hurt avance
            return
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
                
        # Logica de colision de ataque
        if not self.hurt and not player.hurt:
            if self.rect.colliderect(player.king_rect):
                if player.attacking and not self.attacking:
                    self.receive_hit(-1 if self.x < player.x else 1, player.attack_damage)
                elif self.attacking and not player.attacking:
                    player.receive_hit(-1 if player.x < self.x else 1, self.attack_damage)
                    
        # Si no hay piso, solo detener el movimiento horizontal
        if not has_ground:
            self.waiting = True
            self.horizontal_velocity = 0
            # No cambiamos el estado a idle para mantener la animación actual
            if self.current_state == "run":
                self.current_state = "idle"
                self.current_frame = 0
        else:
            self.waiting = False
        
        # Calculamos la distancia horizontal al jugador
        # distance_to_player = abs(self.x - player.x)
        distance_to_player = abs(self.rect.centerx - player.king_rect.centerx)
        # Verificamos si el jugador está dentro del rango de visión horizontal Y a una altura aceptable
        in_range_player = distance_to_player <= self.detection_range
        has_vision = self.has_line_of_sight(player, solid_objects)
        collision = self.check_collision_with_player(player)
        
        planned_direction = self.direction # Por defecto, mantener dirección actual
        self.horizontal_velocity = 0
        # self.attacking se determinará aquí y se usará para update_rect más adelante

        # Logica de Orientación PRIORITARIA si el jugador está detectado y visible
        if has_vision and in_range_player : # Un poco más que detection_range para voltear
            planned_direction = 1 if player.x > self.x else -1  

                              
        # Estado por defecto
        self.horizontal_velocity = 0
            
        # Cooldown de persecución tras golpear o ser golpeado
        if current_time - self.last_pursuit_time < self.pursuit_cooldown:
            if self.current_state == "attack":
                if self.current_frame < len(self.animations["attack"]) - 1:
                    current_delay = settings.ANIMATIONS_ENEMY_DELAYS[self.name][self.current_state]
                    if self.animation_timer >= current_delay:
                        self.update_animation(delta_time)
                        self.animation_timer = 0
                    self.update_rect()
                    return
            else:
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
        
        # Aplicar la dirección decidida
        self.direction = planned_direction # Siempre actualizar la dirección basada en la última lógica de orientación
        
        # Logica de ataque (funciona independientemente de si hay suelo o no)
        # print(f"distancia: ",distance_to_player)
        # print(f"rango: ",distance_to_player)
        if distance_to_player <= self.attack_range and in_range_player and has_vision  :
            if not self.attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
                self.current_state = "attack"
                self.attacking = True
                self.current_frame = 0
                self.last_attack_time = current_time
            elif self.attacking:
                self.current_state = "attack"
                if self.current_frame == len(self.animations["attack"]) - 1:
                    self.attacking = False
                    self.current_state = "idle"
                    self.current_frame = 0
                
        # Solo perseguir si hay suelo
        elif has_ground and in_range_player and has_vision and not collision:
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



        # Solo mover si no hay colision
        if not collision and has_ground:
            self.x += self.horizontal_velocity * (delta_time / 1000)
        else:
            self.horizontal_velocity = 0

   
        self.check_collision_with_world(solid_objects)
        
        # Current delay es para saber cuanto tiempo tiene que pasar para que se cambie el frame de la animacion
        current_delay = settings.ANIMATIONS_ENEMY_DELAYS[self.name][self.current_state]
        # Actualizar animacion
        if self.animation_timer >= current_delay:
            self.update_animation(delta_time)
            self.animation_timer = 0
        
        self.update_rect()
        
    def update_animation(self, delta_time):
        self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_state])

    def draw(self, screen, camera_offset=(0, 0), player=None, solid_objects=None):
    
        if self.is_dead:
            if not self.death_animation_completed:
                # Usar la animacion de muerte del diccionario de animaciones
                current_surface = self.animations["death"][self.current_frame]
                
                if self.direction == -1:
                    current_surface = pygame.transform.flip(current_surface, True, False)
                    
                offset = camera_offset if camera_offset else (0, 0)
                screen.blit(current_surface, (self.x - offset[0], self.y - offset[1] - self.floor_correct))
            return
        
        self.render_health_bar(self.x, self.y, screen, camera_offset)
        
        if self.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        current_surface = self.animations[self.current_state][self.current_frame]
        
        if self.direction == -1:
            current_surface = pygame.transform.flip(current_surface, True, False)
            
        offset = camera_offset if camera_offset else (0, 0)
        # y_render = offset[1] + self.enemy_rect_offset_y * 3 # Aplica el offset vertical
        if self.name == "Minotaur":
            # Ajustar la posición del Minotauro para que se vea bien
            screen.blit(current_surface, (self.x - offset[0] - 160, self.y - offset[1] - self.floor_correct))
        else:
            screen.blit(current_surface, (self.x - offset[0], self.y - offset[1] - self.floor_correct))
        
        # Dibujar el rectangulo de colision 
        # rect_to_draw = pygame.Rect(
        #     self.rect.x - offset[0],
        #     self.rect.y - offset[1],
        #     self.rect.width,
        #     self.rect.height,
        # )
        # pygame.draw.rect(screen, (255, 0, 0), rect_to_draw, 2)
        
        # Dibujar el rectángulo de deteccion de suelo
        # ground_check = pygame.Rect(
        #     self.rect.x + ((self.rect.width + 10) * self.direction)  - offset[0],
        #     self.rect.bottom - offset[1],
        #     25,
        #     25
        # )
        # pygame.draw.rect(screen, (0, 255, 0), ground_check, 2)
        


        # if player is not None:
        #     enemy_pos = (self.rect.centerx - camera_offset[0], self.rect.centery - camera_offset[1])
        #     player_pos = (player.king_rect.centerx - camera_offset[0], player.king_rect.centery - camera_offset[1])
        #     pygame.draw.line(screen, (255, 255, 0), enemy_pos, player_pos, 2)  # Línea amarilla
        
        # for solid in solid_objects:
        #     if not isinstance(solid, pygame.Rect):
        #         solid = pygame.Rect(solid.x, solid.y, solid.width, solid.height)
        #     clipped = solid.clipline(enemy_pos, player_pos)
        #     if clipped:
        #         # Dibuja el segmento recortado en rojo
        #         pygame.draw.line(screen, (255, 0, 0), 
        #                         (clipped[0][0] - camera_offset[0], clipped[0][1] - camera_offset[1]),
        #                         (clipped[1][0] - camera_offset[0], clipped[1][1] - camera_offset[1]), 3)                                        
    
    def render_health_bar(self, x,y,screen,camera_offset):
        # Renderiza la barra de vida del enemigo
        health_bar_width = 50
        health_bar_height = 5
        health_ratio = self.current_health / self.max_health
        # Posicion de la barra de vida
        bar_x = x - camera_offset[0] + self.base_rect_height + health_bar_width // 2 - Enemies[self.name]["health_bar_offset_x"]
        bar_y = y - camera_offset[1] + self.base_rect_height - health_bar_height - self.floor_correct - Enemies[self.name]["health_bar_offset_y"]
        
        # Fondo de la barra (rojo)
        pygame.draw.rect(screen, (255, 0, 0), 
                           (bar_x, bar_y, health_bar_width, health_bar_height))
            
        # Vida actual (verde)
        pygame.draw.rect(screen, (0, 255, 0), 
                           (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))
        
    # Determina si hay un objeto solido en la linea de vision del enemigo y el jugador 
    def has_line_of_sight(self, player, solid_objects):
        enemy_pos = (self.rect.centerx, self.rect.centery)
        player_pos = (player.king_rect.centerx, player.king_rect.centery)

        for solid in solid_objects:
            if not isinstance(solid, pygame.Rect):
                solid = pygame.Rect(solid.x, solid.y, solid.width, solid.height)
            if solid.clipline(enemy_pos, player_pos):
                return False
        return True

