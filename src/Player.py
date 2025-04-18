import pygame
import settings
from src.globalUtilsFunctions import update_vertical_acceleration
import pytmx

class Player:
    
    def __init__(self, x, y):
        # Inicalizamos todas las varibales que usara nuestro jugadorsito
        
        # Variables de posicion
        self.x = x
        self.y = y
        
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
        self.combo_timeout = 500
        
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
        self.ground_collide = False
        
        # Movimiento horizontal
        self.horizontal_velocity = 0

        # Varibles para controlar el ancho de rectangulo de colision del personaje, cuando no hace nada y cuando ataca, (porque no quiero que sean del mismo tama;o que el sprite del jugador)
        # Y cuando ataca el rectangulo de colision crecera
        self.base_rect_width = 30 - 13
        self.base_rect_height = 55 - 10
        self.attack_rect_width = 55

        # Variables de control , para movimiento horizontal
        self.on_ground = False
        self.horizontal_velocity = 0

        # Offset para centrar el rectángulo con el sprite, ya que como el rectangulo se alargara a izquierda o derecha debemos cambia la posicion en x y y de donde inicia
        # son parapetos :p pero era lo mas rapido 
        # Ajustes mañosos 
        self.rect_offset_x = 25 + 5
        self.rect_offset_y = 17 + 3  

        # Aqui ya le agrego la posicion inicial del rectangulo teniendo en cuenta la del player + el offset de control solo para que se vea bonito y sea coherente
        self.pos_player_rectX = self.x + self.rect_offset_x
        self.pos_player_rectY = self.y + self.rect_offset_y
        
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
    
    # Metodo que verifica colisiones con los objetos que le pasemos, por ahora objetos solidos no enemigos    
    def check_collision(self, solid_objects:pygame.Rect):
        
        # Empezamos a recorrer el arreglo de solidos
        for solid in solid_objects:
            
            # Si el solido actual colisiona con el rectangulo de colision del jugador (king_rect) entra en la condicion
            if self.king_rect.colliderect(solid):
                
                # Verificamos Colision con el suelo
                #   Condiciones: 
                #       1- Si el jugador tiene movimiento vertical positivo quiere decir que va hacia abajo osea esta cayendo
                #       2- Si el la parte inferior del rectangulo de colision del jugador es mayor al tope del solido (choca pies con parte de arriba) 
                if self.vertical_velocity > 0 and self.king_rect.bottom >= solid.top:
                    # Print mañoso
                    print("colision suelo")
                    # Correguimos la posicion del jugador a una donde no haya colision
                    self.y = solid.top - self.king_rect.height - 21
                    
                    # Su velocidad pasa a ser 0
                    self.vertical_velocity = 0
                    
                    # Y configuramos las variables para decirle las coordenadas de su nuevo "piso", osea caminara en x sobre esa coordenada en y 
                    self.jumping = False
                    self.ground_y = self.y
                    self.on_ground = True   
                        
                # Verificamos Colision con el techo
                #   Condiciones: 
                #       1- Si el jugador tiene movimiento vertical negativo quiere decir que va hacia arriba osea esta saltando o yendose hacia arriba
                #       2- Si el la parte superior del rectangulo de colision del jugador es menor a la parte de abajo del solido, (choca cabeza con parte de abajo) 
                elif self.vertical_velocity < 0 and self.king_rect.top < solid.bottom:
                    # Print mañoso x2
                    print("colision techo")
                    # Este dio menos guerra que el anterior sabra dios porque :V , pero solo acomodamos su posicion en y para que sea igual a la de la parte de abajo del solido
                    self.y = solid.bottom
                    # Asigamos velocidad cero , para quitarle la velocidad de subida, y ya la gravedad que diosito nos dio (en el metodo update) lo mande para abajo
                    self.vertical_velocity = 0

                # Verificamos Colisiones laterales
                #   Condiciones: 
                #       1- Si el jugador tiene direccion 1 quiere decir que esta viendo a la derecha 
                #       2- Si el la parte derecha del rectangulo de colision del jugador esta en una coordenada del eje x mas grande que la parte izquierda de solido
                elif self.direction == 1 and self.king_rect.right > solid.left:
                    # Prines mañosos
                    print("colision derecha")
                    # Acomodamos la posicion del jugador mas a la izquierda donde no alla colision 
                    # (los numeros que se ven en todas estas correcciones son numeros magicos :3, nadie sabe de donde salio pero funciona XD)
                    self.x = solid.left - self.base_rect_width * 4 - 10
                           
                #   Condiciones: 
                #       1- Si el jugador tiene direccion 1 quiere decir que esta viendo a la derecha 
                #       2- Si el la parte derecha del rectangulo de colision del jugador esta en una coordenada del eje x mas grande que la parte izquierda de solido
                elif self.direction == -1 and self.king_rect.left < solid.right:
                    # Que pereza tanto print pero ayudan :v
                    print("colision izquierda")
                    self.x = solid.right - self.base_rect_width * 3 
                    
    # Metodo update donde actualiza los estados del player y verifica que cambios se hicieron en el 
    def update(self,delta_time,solid_objects):
        # Aumentamos el tiempo de la animacion y el tiempo del combo 
        self.animation_timer += delta_time
        self.combo_timer += delta_time

        if self.current_state == "idle" or self.current_state == "run":
            # Verificar si hay suelo debajo antes de aplicar gravedad
            is_on_ground = self.check_ground(solid_objects)
            
            # Si no hay suelo debajo y no estamos saltando, comenzar a caer, aplicando caida libre
            if not is_on_ground and not self.jumping:
                self.on_ground = False
                
            # Si no hay colisión con el suelo, aplicar "gravedad"
            if not self.on_ground:
                self.vertical_velocity += settings.GRAVITY  # Aceleración constante hacia abajo
                self.y += self.vertical_velocity

        # Verificamos colisiones con objetos solidos
        # En este caso el player no tiene colisiones con enemigos por ahora (evaluar)
        self.check_collision(solid_objects)

        # # Actualizar física del salto primero
        old_jumping = self.jumping
        
        # Aplicamos la logica de aceleracion vertical y caida libre para el salto
        self.vertical_velocity, self.y, self.jumping = update_vertical_acceleration(
            self.vertical_velocity, settings.GRAVITY, self.y, self.ground_y, self.jumping
        )

        # Si estamos saltando, forzar el estado de salto
        if self.current_state == "jump" or self.jumping:
            self.current_state = "jump"
        elif old_jumping and not self.jumping:
            if self.current_state == "jump":
                self.current_state = "idle"
                self.current_frame = 0

        # Current delay es para saber cuanto tiempo tiene que pasar para que se cambie el frame de la animacion
        current_delay = settings.ANIMATIONS_DELAYS[self.current_state]

        # Actualizar animación
        if self.animation_timer >= current_delay:
            self.update_animation()
            self.animation_timer = 0

      
        # Actualizar tamaño del rectángulo de colision, dependiendo de si esta atacando o no
        rect_width = self.attack_rect_width if self.attacking else self.base_rect_width
        
        # Actualizar posicion del rectángulo de colisión
        if self.direction == 1:
            rect_x = self.x + self.rect_offset_x * 2 
        else:
            # correccion para que el rectangulo crezca a la izquierda
            rect_x = self.x + (self.rect_offset_x * 2 - rect_width) + 10
        
        # Crea el nuevo rectangulo de colision para el player (hay que actualizarlo cada vez que se mueve el player)  
        self.king_rect = pygame.Rect(
            rect_x, self.y + self.rect_offset_y, rect_width, self.base_rect_height
        )
         
        # Actualizamos la posicion del rectangulo segun donde este jugador
        self.update_camera_rect()
    
    # Metodo que verifica que teclas se presionaron y que accion tomar en consecuencia
    def handle_inputs(self, keys,delta_time):
     
        # Por defecto, establecemos el estado como idle
        new_state = "idle"
        self.horizontal_velocity = 0

        # Si presiona la tecla espacio salta , solo se permite 1 salto a la vez
        if keys[pygame.K_SPACE] and self.vertical_velocity == 0 and not self.jumping:
            self.jumping = True
            self.vertical_velocity = settings.PLAYER_SPEED_JUMP
            new_state = "jump"
            self.ground_collide = False
            self.current_combo = 1
            self.current_frame = 0
            self.attacking = False

        # Movimiento horizontal
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            new_state = "run"
            self.direction = -1 if keys[pygame.K_LEFT] else 1
            self.x += (
                self.direction * settings.PLAYER_SPEED * delta_time / 1000
            )
            

        # Ataque , solo se puede atacar cuando no se esta saltando
        if keys[pygame.K_x] and not self.jumping :
           
            # Validamos si no estamos atacando ya , si el player no se encuentra atacando entonces comienza el ataque en combo
            if not self.attacking:
                new_state = "attack"
                self.attacking = True
                self.current_frame = 0
                self.combo_timer = 0
                
            # Si ya estamos atacando , verifica que combo se esta ejecutando actualmente y actua en consecuencia
            # Solo tenemos 4 movimiento distintos es decir combos de x4
            elif self.attacking:  
                
                # Almacenamos que frame es el del combo actual que se va a ejecutar
                current_attack_frames = self.attack_moveset[
                    f"attack{self.current_combo}"
                ]
                
                # Verificar si estamos en el último frame o cerca del final, si esta en el ultimo reiniciamos el combo y volvemos a la animacion de attack1
                # Permitir un poco antes del final
                if self.current_frame >= len(current_attack_frames) - 2:
                    if self.current_combo < self.max_combo:
                        self.current_combo += 1
                    else:
                        self.current_combo = 1
                    self.current_frame = 0
                    self.combo_timer = 0
                    
            # Aqui en teoria deberiamos meter un sonido aleatorio pero hay que solucionar el tema de que se reproducen los sonidos montados
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
            
    # Metodo para dibujar o renderizar al player en el frame que este ejecutando   
    def draw(self, screen,camera_offset=None):
        
        # Este es igual al metodo render  , pasa que siguiendo el tutorial le pusieron draw y ya me da pereza cambiarlo XD
        
        # Aqui es simple si esta atacando carga el frame correspondiente al movimiento de ataque actual
        if self.attacking:
            attack_frames = self.attack_moveset[f"attack{self.current_combo}"]
            current_surface = attack_frames[self.current_frame]
            
        # Sino carga el frame de movimiento correspondiente que si caminar , run etc
        else:
            current_surface = self.animations[self.current_state][self.current_frame]

        # Si la direccion es hacia la izquierda simplemente voltea el frame del jugador
        if self.direction == -1:
            current_surface = pygame.transform.flip(current_surface, True, False)
        
        # Dibujar información de debug
        debug_info = f"Estado: {self.current_state} Combo: {self.current_combo} Frame: {self.current_frame}"
        font = pygame.font.Font(None, 36)
        text = font.render(debug_info, True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Usar la posición ajustada por la cámara si está disponible, este es un metodo particular porque aqui la posicion va conforme a la camara
        # Ya que el personaje se movera en conjunto con la camara y los objetos no deben moverse con el
        x, y = camera_offset if camera_offset else (self.x, self.y)
        screen.blit(current_surface, (x, y))
        
        # Metodo viejo de renderizado
        # screen.blit(current_surface, (self.x, self.y))

        # Dibujar el rectángulo de colisión
        # pygame.draw.rect(
        #     screen, (255, 0, 0), self.king_rect, 2
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
                self.animations[animation_type].append(surface)
               
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
    


    
