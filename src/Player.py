import pygame
import settings
from src.globalUtilsFunctions import update_vertical_acceleration , extract_animation_complex_spritesheet
from src.globalUtilsFunctions import extract_animation_moveset , extract_animation_unique_spritesheet
import settings


class Player:
    
    def __init__(self, x, y):

        # Variables para la animación de muerte
        self.death_animation_completed = False
        self.death_animation_timer = 0

        # Nuevos flags para mayor control:
        self.can_move = True # Puede ser False durante ciertas partes del ataque
        self.can_initiate_new_action = True # Para controlar cuándo se pueden iniciar nuevos saltos/ataques
        
        # Sistema de vida
        self.max_health = 500
        self.current_health = self.max_health
        self.is_dead = False
        self.attack_damage = 40  # Daño que hace el jugador
        self.has_key = False
        self.has_door_key = False

        self.current_surface = None
        # Para el da;o
        self.hurt = False
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.hurt_timer = 0
        self.hurt_duration = 500  # ms
        self.invulnerable_duration = 1000  # ms
        self.knockback_speed = 100 
        self.hurt_frame = 0  # Usaremos el primer frame de "jump" como frame de herido

        # Variables de ataque, y generar coldown entre ataques
        self.attack_windup = 400  # ms antes de atacar
        self.attack_windup_timer = 0
        self.attack_recovery = 300  # ms despues de atacar
        self.attack_recovery_timer = 0
        self.in_attack_recovery = False
        self.in_attack_windup = False

        # Inicalizamos todas las variabales que usara nuestro jugadorsito
        
        
        # Variables de posicion
        self.x = x - 10
        self.y = y - 20

     
        # Variables de direccion (para saber si vamos a izquierda (-1) o derecha (1) )
        self.direction = 1
        
        # Variables para saber en que estado se encuentra nuestro jugador mañoso
        self.current_state = "idle"
        
        # Esta variable nos dice en que frame estara nuestro jugador, porque como es inquieto siempre se esta moviendo :V
        # Y esta variable me permite controlar el frame de la animacion correspondiente segun el movimiento, caminar , correr , etc
        # Cada estado tendra 4 frames menos ataque, es decir cuando estamos en estado "idle" continuamente se ejecutaran 4 frames distintos que sera la animacion que vemos
        self.current_frame = 0
        
        # Varibales para controlar ataques y su animaciones
        # La usamos para controlar la velocidad de animacion, sera la que aumente hasta que alcance el tiempo correspondiente, el delay de cada una
        self.animation_timer = 0
        
        # Simple boleano para saber si sigue atacando o no (para verificaciion entra porque con el simple estado me hacia chocoplum)
        self.attacking = False
        
        # Tiempo en ms para mantener el combo, para limitar el tiempo en que se concatena un combo, es decir cuando inicia esto no puedes concatenar  denuevo
        self.combo_timeout = 400
        
        # Variables para el control de combos, para saber en que combo estamos el maximo combo y el tiempo que va combo
        self.current_combo = 1
        self.max_combo = 4
        self.combo_timer = 0
        
        # En este diccionario almacenaremos los diferentes Movimientos DE ATAQUE , es decir attack1 ,2  y asi para saber que frame le ataque pertenece a cual en cada combo
        self.attack_moveset = {}
        # Aqui guardaremos igualmente los diferentes comportamientos de nuestro jugador, recordemos que estos objetos son usados para saber que frame y animacion usaremos para cada estado
        self.animations = {"run": [], "attack": [], "jump": [], "idle": []}
        
        # Y esta belleza es la que le asigna las animaciones a tanto los moveset como las animaciones
        self.load_animations()
        
        # Variables de control de salto y velocidad vertical, y verificar si hay colision con ground o no
        self.jumping = False
        self.vertical_velocity = 0
        self.ground_y = y
        

        # Varibles para controlar el ancho de rectangulo de colision del personaje, cuando no hace nada y cuando ataca, (porque no quiero que sean del mismo tama;o que el sprite del jugador)
        # Y cuando ataca el rectangulo de colision crecera
        self.base_rect_width = 20
        self.base_rect_height = 55
        self.attack_rect_width = 60

        
        # Variables de control , para movimiento horizontal
        self.on_ground = True
        self.horizontal_velocity = 0
        
        scale_factor = settings.SCALE_FACTOR
        self.scale_factor = settings.SCALE_FACTOR
        # Calcula el nuevo offset en Y para centrar el rectángulo con el sprite escalado
        # Suponiendo que el sprite original y el rectángulo estaban alineados antes del escalado:
        self.rect_offset_x = 35  # Puedes ajustar este valor si el rectángulo no está centrado horizontalmente
        self.rect_offset_y = int(-10 * scale_factor)  # Ajusta el offset vertical según el escalado

        # Aqui ya le agrego la posicion inicial del rectangulo teniendo en cuenta la del player + el offset de control solo para que se vea bonito y sea coherente
        self.pos_player_rectX = self.x + self.rect_offset_x
        self.pos_player_rectY = self.y + self.rect_offset_y
        
        # correccion de la posicion en y del jugador para que quede en el piso
        self.offset_positiony = 15
        # self.offset_positiony = self.y
        # Ahora, la posición inicial del jugador debe considerar el nuevo offset
        self.x = x - 10
        self.y = self.y - self.offset_positiony
        # print(self.y)
        # Inicializar el rectángulo de colision del jugador
        self.king_rect = pygame.Rect(
            self.pos_player_rectX,
            self.pos_player_rectY,
            self.base_rect_width,
            self.base_rect_height,
        )
        
        # Esta variable extra se centrara en el rectagulo original del player (ya que al atacar se alarga y genera dos coordenadas posibles y era un desastre con la camara)
        # Entonces esta variable sera estatica para guardar el punto de referencia de la camara para moverse en consecuencia al jugador
        self.camera_rect = self.king_rect
        
        # Cargar animacion de muerte
        self.load_death_animation()

    def load_death_animation(self):
        # Cargar la animacion de muerte
        initial_sprite = 0
        sprite_moveset_size = 4
        death_animations = extract_animation_complex_spritesheet("DeathKnight", self.scale_factor)
        self.animations["death"] = extract_animation_moveset(death_animations, (initial_sprite, sprite_moveset_size))
        print(len(self.animations["death"]))
    # Verificador de colisiones con el mundo
    def check_collision(self, solid_objects:pygame.Rect):
        # Empezamos a recorrer el arreglo de solidos
        for solid in solid_objects:
            # Si el solido actual colisiona con el rectangulo de colision del jugador (king_rect) entra en la condicion
            if self.king_rect.colliderect(solid):
                # Calculamos las distancias a cada borde del sólido
                dist_top = abs(self.king_rect.bottom - solid.top)
                dist_bottom = abs(self.king_rect.top - solid.bottom)
                dist_left = abs(self.king_rect.right - solid.left)
                dist_right = abs(self.king_rect.left - solid.right)

                # Encontramos la distancia minima para determinar el tipo de colisión
                min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

                # Colision desde arriba (cayendo)
                if min_dist == dist_top and self.vertical_velocity > 0:
                    print("colision suelo")
                    self.y = solid.top - self.king_rect.height - self.rect_offset_y
                    self.vertical_velocity = 0
                    self.jumping = False
                    self.ground_y = self.y
                    self.on_ground = True

                # Colision desde abajo (saltando)
                elif min_dist == dist_bottom and self.vertical_velocity < 0:
                    print("colision techo")
                    self.y = solid.bottom * 1.05
                    self.vertical_velocity = 0

                # Colision desde la derecha
                elif min_dist == dist_left and self.direction == 1:
                    print("colision por la derecha del personaje")
                    self.horizontal_velocity = 0
                    self.x = solid.left - self.base_rect_width - self.rect_offset_x * 2 - 2

                # Colision desde la izquierda
                elif min_dist == dist_right and self.direction == -1:
                    print("colision por la izquierda del personaje")
                    self.horizontal_velocity = 0
                    self.x = solid.right - self.base_rect_width - self.rect_offset_x * 1.2 + 1
       
    # Logica para cuando recibe un golpe             
    def receive_hit(self, direction, damage):
        # Logica para recibir el golpe, es decir si el jugador recibe un golpe se activa la variable hurt y se le asigna una direccion de knockback
        # Esto es para que el jugador no pueda recibir mas de un golpe al mismo tiempo, es decir si ya esta herido no puede volver a ser herido
        if not self.invulnerable:
            self.hurt = True
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
            self.hurt_timer = pygame.time.get_ticks()
            self.current_state = "idle"
            self.current_frame = self.hurt_frame
            self.knockback_direction = direction

            self.current_health -= damage
            # Verificar si el jugador muere
            if self.current_health <= 0:
                self.is_dead = True
                self.current_health = 0
                self.current_state = "death"
                self.current_frame = 0
                self.death_animation_completed = False
                self.death_animation_timer = pygame.time.get_ticks()
                # Reproducir sonido de muerte
                settings.SOUNDS["player_death"].play()

    # Metodo update donde actualiza los estados del player y verifica que cambios se hicieron en el 
    def update(self,delta_time,solid_objects):   
        # Aumentamos el tiempo de la animacion y el tiempo del combo 
        self.animation_timer += delta_time 
        
        # Si el jugador esta muerto
        if self.is_dead:
            if not self.death_animation_completed:
                self.death_animation_timer += delta_time
                
                # Actualizar la animación de muerte
                current_delay = settings.ANIMATIONS_DELAYS["death"]
                if self.death_animation_timer >= current_delay:
                    self.update_animation()
                    self.death_animation_timer = 0
                    
                    # Verificar si la animación de muerte ha terminado
                    if self.current_frame >= len(self.animations["death"]) - 1:
                        self.death_animation_completed = True
            return
                 
        # Si esta herido, aplicar knockback y controlar invulnerabilidad
        if self.hurt:          
            self.apply_knockback(delta_time, solid_objects)
            if pygame.time.get_ticks() - self.hurt_timer > self.hurt_duration:
                self.hurt = False
                self.current_state = "idle"
                self.current_frame = 0
                return
          
        # Verificamos si el jugador e invulnerable, si es asi no puede recibir mas golpes      
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False

        # Siempre podra moverse en x , para que se desplace saltando y atacando tambien
        self.x += self.horizontal_velocity * delta_time / 1000
        
        # Aplicamos la logica de aceleracion vertical y caida libre para el salto
        self.vertical_velocity, self.y, self.jumping , self.current_state = update_vertical_acceleration(
            self.vertical_velocity, settings.GRAVITY, self.y, self.ground_y, self.jumping , self.current_state
        )
        
        # --- FÍSICA Y COLISIONES ---
        if self.current_state == "idle" or self.current_state == "run":
            # Verificar si hay suelo debajo antes de aplicar gravedad
            is_on_ground = self.check_ground(solid_objects)
     
            # Si no hay suelo debajo y no estamos saltando, comenzar a caer, aplicando caida libre
            if not is_on_ground and not self.jumping:
                self.on_ground = False
                
            # # Si no hay colisión con el suelo, aplicar "gravedad"
            if not self.on_ground:
                self.vertical_velocity += settings.GRAVITY
                self.y += self.vertical_velocity
                
            
        # Verificamos colisiones con objetos solidos
        # En este caso el player no tiene colisiones con enemigos por ahora (evaluar)
        self.check_collision(solid_objects)
        
        # --- CONTROL DE ESTADOS ---  
        # 1. Al aterrizar (venía de salto o caída)
        if self.current_state == "jump" and self.vertical_velocity == 0 and self.on_ground:
            self.current_state = "idle" 
            self.jumping = False
        # 2. Corriendo (venia de idle )
        if self.current_state == "idle" and self.horizontal_velocity != 0 and self.on_ground:   
            self.current_state = "run"   
            self.jumping = False
        # 3. Quieto (venia de correr)   
        elif self.current_state == "run" and self.horizontal_velocity == 0 and self.on_ground: 
            self.current_state = "idle"       
                            
        # Current delay es para saber cuanto tiempo tiene que pasar para que se cambie el frame de la animacion
        if self.current_state == "fall":
            current_delay = settings.ANIMATIONS_DELAYS["jump"]
        else:
            current_delay = settings.ANIMATIONS_DELAYS[self.current_state]         
  
  
        # Actualizar animacion
        if self.animation_timer >= current_delay:
            self.update_animation()
            self.animation_timer = 0

        if self.attacking:
            self.combo_timer += delta_time
        else:
            self.combo_timer = 0
        

        # Actualizar el rectángulo de colisión del jugador
        self.update_player_rect()  

        # Actualizamos la posicion del rectangulo segun donde este jugador
        self.update_camera_rect()

    # Acutualiza rectangulo de colision
    def update_player_rect(self):
        # Actualizar tamaño del rectangulo de colision, dependiendo de si esta atacando o no
        rect_width = self.attack_rect_width if self.attacking else self.base_rect_width
        
        # Actualizar posicion del rectangulo de colisión
        if self.direction == 1:
            rect_x = self.x + self.rect_offset_x * 2 
        else:
            # correccion para que el rectangulo crezca a la izquierda
            rect_x = self.x + (self.rect_offset_x * 2 - rect_width) + 11
        
        # Crea el nuevo rectangulo de colision para el player (hay que actualizarlo cada vez que se mueve el player)  
        self.king_rect = pygame.Rect(
            rect_x, 
            self.y + self.rect_offset_y, 
            rect_width, 
            self.base_rect_height
        )

    # Metodo para aplicar knockback al jugador, es decir cuando recibe un golpe se mueve hacia atras
    def apply_knockback(self, delta_time, solid_objects):
        knockback_distance = self.knockback_direction * self.knockback_speed * (delta_time / 1000)
        
        for solid in solid_objects:
            if self.king_rect.colliderect(solid):
                return  # No aplicar knockback si colisiona
            
        self.x += knockback_distance
    
    # Metodo para dibujar o renderizar al player en el frame que este ejecutando   
    def render(self, screen,camera_offset=None):
        # Si el jugador esta muerto no renderiza nada
        if self.is_dead:
            if not self.death_animation_completed:
                # Usar la animacion de muerte
                current_surface = self.animations["death"][self.current_frame]
                
                if self.direction == -1:
                    current_surface = pygame.transform.flip(current_surface, True, False)
                    
                x, y = camera_offset if camera_offset else (self.x, self.y)
                y_render = y + self.rect_offset_y * 3
                screen.blit(current_surface, (x, y_render))
            if self.death_animation_completed:
                current_surface = self.animations["death"][3]
                
                if self.direction == -1:
                    current_surface = pygame.transform.flip(current_surface, True, False)
                    
                x, y = camera_offset if camera_offset else (self.x, self.y)
                y_render = y + self.rect_offset_y * 3
                screen.blit(current_surface, (x, y_render))
            return
        
        # Si el jugador está herido y no es invulnerable, alternar la visibilidad del sprite
        if self.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        # Este es igual al metodo render  , pasa que siguiendo el tutorial le pusieron draw y ya me da pereza cambiarlo XD
        if self.vertical_velocity > 0 and not self.on_ground and not self.horizontal_velocity > 0:
            self.current_surface = self.animations["jump"][1]  # Frame 2 (índice 1)
        # Aqui es simple si esta atacando carga el frame correspondiente al movimiento de ataque actual
        elif self.attacking:
            attack_frames = self.attack_moveset[f"attack{self.current_combo}"]
            self.current_surface = attack_frames[self.current_frame]
            
        # Sino carga el frame de movimiento correspondiente que si caminar , run etc
        else:
            self.current_surface = self.animations[self.current_state][self.current_frame]

        # Si la direccion es hacia la izquierda simplemente voltea el frame del jugador
        if self.direction == -1:
            self.current_surface = pygame.transform.flip(self.current_surface, True, False)
        
        # Dibujar información de debug
        # debug_info = f"Estado: {self.current_state} Combo: {self.current_combo} Frame: {self.current_frame}"
        # font = pygame.font.Font(None, 36)
        # text = font.render(debug_info, True, (255, 255, 255))
        # screen.blit(text, (10, 10))

        # Usar la posicion ajustada por la camara si está disponible, este es un metodo particular porque aqui la posicion va conforme a la camara
        # Ya que el personaje se movera en conjunto con la camara y los objetos no deben moverse con el
        x, y = camera_offset if camera_offset else (self.x, self.y)
        y_render = y + self.rect_offset_y * 3 # Aplica el offset vertical
        screen.blit(self.current_surface, (x, y_render))
        
        # Renderizar la barra de salud
        self.render_health_bar(x,y_render,screen)
        
   
       # Dibujar el rectangulo de colision
        # rect_draw_x = self.king_rect.x
        # rect_draw_y = self.king_rect.y
        # if camera_offset:
        #     rect_draw_x = self.king_rect.x - self.x + x
        #     rect_draw_y = self.king_rect.y - self.y + y
        # pygame.draw.rect(
        #     screen,
        #     (255, 0, 0),  # Color rojo
        #     pygame.Rect(rect_draw_x, rect_draw_y, self.king_rect.width, self.king_rect.height),
        #     2,  # Grosor de la línea
        # )
    
    # METODO AUXILIARES
    # Actuliza el rectangulo de colision de la camara, es decir el rectangulo que se usa para mover la camara
    def update_camera_rect(self):
        # Este metodo auxiliar para mantener el rectagulo de colision fijo del jugador 
        # Este rectangulo se evalua exclusivamente con la camara para ella saber cuando moverse
        # Es netamente una variable auxiliar para esta funcionalidad
        self.camera_rect = pygame.Rect(
            self.x + self.rect_offset_x * 2 , self.y + self.rect_offset_y, self.base_rect_width, self.base_rect_height
        )
    
    # Metodo para cargar las animaciones del jugador, aqui esta la logica donde se cargan los spritesheets y se asignan a cada animacion
    # Todo se guarda en arrays para usar luego
    def load_animations(self):
        
        # Cargar spritesheets del king en un array para automatizar las animaciones
        # cabe destacar que esta configurado para trabajar correctamente con 4 frames los ataques
        scale_factor = settings.SCALE_FACTOR
        
        self.sprite_sheets = {
            "run": settings.TEXTURES["kingRun"],
            "attack": settings.TEXTURES["kingAttack"],
            "jump": settings.TEXTURES["kingJump"],
            "idle": settings.TEXTURES["idle"],
        }

        self.frame_data = {
            "run": settings.FRAMES["kingRun"],
            "attack": settings.FRAMES["kingAttack"],
            "jump": settings.FRAMES["kingJump"],
            "idle" : settings.FRAMES["idle"],
        }

        # Recorremos los spritesheets y los frames para asignar las animaciones a cada uno de ellos
        # Este metodo es importante ya que asi recorremos el spritesheet y le asignamos los frames a cada animacion , dependiendo del tamaño del frame sera los sprites que saque
        # Por ejemplo si el frame es de 64x64 y el spritesheet tiene 4 frames de 64x64 entonces el resultado sera 4 sprites distintos
        # Esta configuracion hay que tener en cuenta cuando la agregarmos en la imagen medirla con paint 
        # digamos que es como que le asignamos un tamaño de recorte y cuando hacemos este for vamos recortando el spritesheet en partes iguales y lo guardamos en un array
        for animation_type, frames in self.frame_data.items():
            for frame in frames:
                surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
                surface.blit(self.sprite_sheets[animation_type], (0, 0), frame)
                # Escalar la superficie al tamaño deseado
                scaled_surface = pygame.transform.scale(
                    surface,
                    (
                        int(surface.get_width() * scale_factor),
                        int(surface.get_height() * scale_factor),
                    ),
                )
                self.animations[animation_type].append(scaled_surface)
               

        #     # Tendremos 4 moveset es decir hasta combo de 4
        #     # Como los sprites son continuos agarraremos la continuidad de los mismos, osea 1 , 2 , 3....
        #     # estos numeros representan su posicion en el spritesheet, ejemplo 1 sera el spritesheet uno y asi sucesivamente
                
        #     # Guardamos los diferentes moveset que tendra para cada combo
        #     # En frase simples agarramos por orden del spritesheet:
        #     # attack 1 : contendra las imagenes 1 2 y 3 del spritesheet
        #     # attack 2 : contendra las imagenes 4 5 6 y 7 del spritesheet y asi sucesivamente
        #     # Leyendo el spritesheet de izquierda a derecha

            
        attack_spritesheet = extract_animation_unique_spritesheet("Player","Attack",scale_factor)
          
        initial_sprite = 2
        sprite_moveset_size = 4
        self.attack_moveset["attack1"] = extract_animation_moveset(attack_spritesheet,(initial_sprite,sprite_moveset_size))  
        
        initial_sprite = 6
        sprite_moveset_size = 2
        self.attack_moveset["attack2"] = extract_animation_moveset(attack_spritesheet,(initial_sprite,sprite_moveset_size))    
        
        initial_sprite = 11
        sprite_moveset_size = 3
        self.attack_moveset["attack3"] = extract_animation_moveset(attack_spritesheet,(initial_sprite,sprite_moveset_size))  
        
        initial_sprite = 15
        sprite_moveset_size = 4
        self.attack_moveset["attack4"] = extract_animation_moveset(attack_spritesheet,(initial_sprite,sprite_moveset_size)) 

    # Hay veces que hay que reniciar los combos y devolverlos a su estado principal este metodo es para eso , nada mas simple ahorro de codigo
    def reset_attack(self):
        self.current_combo = 1
        self.current_frame = 0
        self.attacking = False

    # Metodo para verificar si tenemos suelo debajo y saber si debemos caer o no
    def check_ground(self, solid_objects:pygame.Rect):
        
        # Creamos una copia del rectangulo de colision del jugador
        ground_check_rect = self.king_rect.copy()
        
        # Movemos el rectangulo un poco hacia abajo para detectar el suelo si hay suelo
        ground_check_rect.y += 2

        # Recorremos el array de objetos para detectar si colisiona
        for solid in solid_objects:
            if ground_check_rect.colliderect(solid):
                if ground_check_rect.bottom >= solid.top:
                    ground_check_rect.y -= 2
                    return True
        return False

    # Metodo para actualizar el sprite del jugador segun lo que detecte la accion, es decir si detecta que estamos caminando carga los sprite de caminar
    def update_animation(self):
        
        # Aqui manejamos dos logicas porque las animaciones de run e idle por ejemplo es una lista simple, pero las de attack son listas de listas porque cada ataque tiene un moveset
        # Por ende manejan logicas distintas para ejecutarse
        
        # Si esta atacando
        if self.attacking:
            
            # Resetear el combo si ha pasado demasiado tiempo (los combos no son infinitos , son controlados solo puedes generar otro ataque cuando termina el actual)
            # Y si no concatenas el combo en cierto momento el combo se reiniciara
            if self.combo_timer >= self.combo_timeout:
                self.reset_attack()
            else:
                # Determinar que frames usar basado en el combo actual, es decir vemos a que frame de ataque pertenece el combito de perros actual de ataque
                attack_frames = self.attack_moveset[f"attack{self.current_combo}"]
                
                # Si el frame actual es el ultimo, resetear el ataque , osea si es el combo 4 devuelve al primero
                if self.current_frame >= len(attack_frames) - 1:
                    self.reset_attack()
                    
                # De lo contrario sigue explotandolo a combos    
                else:
                    self.current_frame += 1

        else:
            
            # Para animaciones normales (run, jump, idle) simplemente aplica la logica rotativa para ir de aumentando el frame en ciclo
            # Esta formula es una ladilla explicar pero haga de cuenta que sirve pa repetir el ciclo infinitamente 0 1 2 3 luego 0 1 2 3 
            # y repetira el ciclo infinitamente mientras aumenta el +1 , sin necesidad de fors y cosas complicadas
            self.current_frame = (self.current_frame + 1) % len(
                self.animations[self.current_state]
            )
    
    def render_health_bar(self, x,y,screen):
        # Renderizar la barra de salud
        bar_x = x + self.rect_offset_x + self.base_rect_width 
        bar_y = y + 5
        
        # Dibujar barra de vida
        health_bar_width = 50
        health_bar_height = 6
        health_ratio = self.current_health / self.max_health
        # Fondo de la barra (rojo)
        pygame.draw.rect(screen, (255, 0, 0), 
                        (bar_x, bar_y, health_bar_width, health_bar_height))
        
        # Vida actual (verde)
        pygame.draw.rect(screen, (0, 255, 0), 
                        (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))