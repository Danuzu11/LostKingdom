import pygame
import settings

class Camera:
    def __init__(self):
        
        # Asignamos las posiciones por defecto de nuestra camarita
        self.offset_x = 0
        self.offset_y = 0
        self.width = settings.VIRTUAL_WIDTH
        self.height = settings.VIRTUAL_HEIGHT
        self.world_width = 0
        self.world_height = 0
        
    def set_world_size(self, width, height):
        # Establece el tamaño total de la camara para limitar el movimiento de la camara, en este caso con el del mundo (el Tilemap)
        self.world_width = width
        self.world_height = height
                  
    def update(self, player_rect , screen):
        
        # el screen podriamos usarlo para algo como depuracion de mensajes etc
          
        # Centramos al jugador en la pantalla
        target_x = player_rect.centerx - self.width // 2
        target_y = player_rect.centery - self.height // 2

        # Actualiza el offset de la cámara basado en la posicion del jugador 
        # Aplicamos límites para que la cámara no se salga del mundo
        self.offset_x = max(0, min(target_x, self.world_width - self.width))
        self.offset_y = max(0, min(target_y, self.world_height - self.height))
        # Asegurarnos de que los offsets no sean negativos
        self.offset_x = max(0, self.offset_x)
        self.offset_y = max(0, self.offset_y)


        # font = pygame.font.Font(None, 24)  # Fuente predeterminada con tamaño 24
        # color = (255, 0, 0)  # Rojo

        # # Mensajes de depuración
        # debug_messages = [
        #     f"Player center: ({player_rect.centerx}, {player_rect.centery})",
        #     f"Target camera position: ({target_x}, {target_y})",
        #     f"World size: ({self.world_width}, {self.world_height})",
        #     f"Final camera offset: ({self.offset_x}, {self.offset_y})"
        # ]

        # # Posición inicial para dibujar los mensajes (arriba a la derecha)
        # x = settings.VIRTUAL_WIDTH - 300  # Ajusta según el ancho de la pantalla
        # y = 10

        # # Dibujar cada mensaje en la pantalla
        # for message in debug_messages:
        #     text_surface = font.render(message, True, color)
        #     screen.blit(text_surface, (x, y))
        #     y += 20  # Incrementar la posición vertical para el siguiente mensaje
    
    def apply(self, x, y):
        # Simplemente aplica el offset a las coordenadas de posicion de la camara
        return (x - self.offset_x, y - self.offset_y)
    
    def apply_rect(self, rect):
        # Hace lo mismo que el anterior pero para el rectangulo de colision de la camara
        # Tengamos en cuenta este es el que usaremos para evaluar la "colision" entre el personaje y la camara , para que despues de cierto punto la camara "persiga" al jugador
        return pygame.Rect(
            rect.x - self.offset_x,
            rect.y - self.offset_y,
            rect.width,
            rect.height
        )