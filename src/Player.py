import pygame
import settings
from src.globalUtilsFunctions import update_vertical_acceleration
import pytmx

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1
        self.current_state = "idle"
        self.current_frame = 0
        self.animation_timer = 0
        self.jumping = False
        self.vertical_velocity = 0
        self.ground_y = y
        self.attacking = False
        self.attack_timer = 0
        self.current_combo = 1
        self.max_combo = 4
        self.combo_timer = 0
        self.horizontal_velocity = 0
        
        self.ground_collide = False
        # Tiempo en ms para mantener el combo
        self.combo_timeout = 500

        # Movimientos
        self.attack_moveset = {}
        # Velocidad de animaciones para cada estado, entre mas alto mas lento

        self.animations = {"run": [], "attack": [], "jump": [], "idle": []}
        self.load_animations()


        self.base_rect_width = 30 - 13
        self.base_rect_height = 55 - 10
        self.attack_rect_width = 55

        # Nuevas variables
        self.on_ground = False
        self.horizontal_velocity = 0

        # Offset para centrar el rectángulo con el sprite
        # Ajustes mañosos 
        self.rect_offset_x = 25 + 5
        self.rect_offset_y = 17 + 3  

        self.pos_player_rectX = self.x + self.rect_offset_x
        self.pos_player_rectY = self.y + self.rect_offset_y
        
        # Inicializar el rectángulo de colision del jugador
        self.king_rect = pygame.Rect(
            self.pos_player_rectX,
            self.pos_player_rectY,
            self.base_rect_width,
            self.base_rect_height,
        )
        
        self.camera_rect = self.king_rect
        
    def update_camera_rect(self):
        # Este metodo auxiliar para mantener el rectagulo de colision fijo del jugador 
        # Este rectangulo se evalua exclusivamente con la camara para ella saber cuando moverse
        # Es netamente una variable auxiliar para esta funcionalidad
        self.camera_rect = pygame.Rect(
            self.x + self.rect_offset_x * 2 , self.y + self.rect_offset_y, self.base_rect_width, self.base_rect_height
        )
    
    def load_animations(self):

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

    def handle_inputs(self, keys,delta_time):
     
        # Por defecto, establecemos el estado como idle
        new_state = "idle"
        self.horizontal_velocity = 0

        # Salto
        # print(self.vertical_velocity)
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
            

        # Ataque
        if keys[pygame.K_x] and not self.jumping :
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

    def check_ground(self, solid_objects:pygame.Rect):
        """Verifica si hay suelo un pixel debajo del jugador"""
        # Creamos un rectángulo de detección justo debajo del jugador
        ground_check_rect = self.king_rect.copy()
        # Movemos el rectángulo un poco hacia abajo para detectar el suelo
        ground_check_rect.y += 2

        for solid in solid_objects:
            if ground_check_rect.colliderect(solid):
                if ground_check_rect.bottom >= solid.top:
                    ground_check_rect.y -= 2
                    return True
        return False

    def check_collision(self, solid_objects:pygame.Rect):
       
        for solid in solid_objects:
            if self.king_rect.colliderect(solid):
                # Colisión con el suelo
                if self.vertical_velocity > 0 and self.king_rect.bottom >= solid.top:
                    print("colision suelo")
                    self.y = solid.top - self.king_rect.height - 21
                    self.vertical_velocity = 0
                    self.jumping = False
                    self.ground_y = self.y
                    self.on_ground = True       
                # Colisión con el techo
                elif self.vertical_velocity < 0 and self.king_rect.top < solid.bottom:
                    self.y = solid.bottom
                    self.vertical_velocity = 0

                # # Colisiones laterales
                elif self.direction == 1 and self.king_rect.right > solid.left:
                    print("colision derecha")
                    self.x = solid.left - self.base_rect_width * 4 - 10
                elif self.direction == -1 and self.king_rect.left < solid.right:
                    print("colision izquierda")
                    self.x = solid.right - self.base_rect_width * 3 
        
    def update(self,delta_time,solid_objects):
        self.animation_timer += delta_time
        self.combo_timer += delta_time

        if self.current_state == "idle" or self.current_state == "run":
            # Verificar si hay suelo debajo antes de aplicar gravedad
            is_on_ground = self.check_ground(solid_objects)
            
            # Si no hay suelo debajo y no estamos saltando, comenzar a caer
            if not is_on_ground and not self.jumping:
                self.on_ground = False
                
            # Si no hay colisión con el suelo, aplicar "gravedad"
            if not self.on_ground:
                self.vertical_velocity += settings.GRAVITY  # Aceleración constante hacia abajo
                self.y += self.vertical_velocity

        self.check_collision(solid_objects)

        # # Actualizar física del salto primero
        old_jumping = self.jumping
        
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

      
        # Actualizar tamaño del rectángulo de colisión
        rect_width = self.attack_rect_width if self.attacking else self.base_rect_width
        
        # Actualizar posición del rectángulo de colisión
        if self.direction == 1:
            rect_x = self.x + self.rect_offset_x * 2 
        else:
            # correcion para que el rectangulo crezca a la izquierda
            rect_x = self.x + (self.rect_offset_x * 2 - rect_width) + 10
                
        self.king_rect = pygame.Rect(
            rect_x, self.y + self.rect_offset_y, rect_width, self.base_rect_height
        )
         
        # Actualizamos la posicion del rectangulo segun donde este jugador
        self.update_camera_rect()
        
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
    
    def draw(self, screen,camera_offset=None):
        
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
        screen.blit(text, (10, 10))

        # Usar la posición ajustada por la cámara si está disponible
        x, y = camera_offset if camera_offset else (self.x, self.y)
        screen.blit(current_surface, (x, y))
        # screen.blit(current_surface, (self.x, self.y))

        # Dibujar el rectángulo de colisión
        # pygame.draw.rect(
        #     screen, (255, 0, 0), self.king_rect, 2
        # ) 

    
