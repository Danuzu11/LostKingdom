import pygame
import settings

class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.width = settings.VIRTUAL_WIDTH
        self.height = settings.VIRTUAL_HEIGHT
        self.world_width = 0
        self.world_height = 0
        
    def set_world_size(self, width, height):
        # Establece el tamaño del mundo para limitar el movimiento de la camara
        self.world_width = width
        self.world_height = height
        

            
    def update(self, player_rect , screen):
          
        # Centramos al jugador en la pantalla
        target_x = player_rect.centerx - self.width // 2
        target_y = player_rect.centery - self.height // 2

        # Actualiza el offset de la cámara basado en la posición del jugador 
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
        """Aplica el offset de la cámara a una posición"""
        return (x - self.offset_x, y - self.offset_y)
    
    def apply_rect(self, rect):
        """Aplica el offset de la cámara a un rectángulo"""
        return pygame.Rect(
            rect.x - self.offset_x,
            rect.y - self.offset_y,
            rect.width,
            rect.height
        )