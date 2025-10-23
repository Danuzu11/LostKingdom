import pygame
import settings 

class AnimatedItem:
    def __init__(self, x, y, frames, animation_delay=1000, name=None):
       
        # :param frames: Lista de superficies (frames) para la animación.
        # :param animation_delay: Tiempo en milisegundos entre cada frame.
 
        self.x = x
        self.y = y
        self.frames = frames
        self.animation_delay = animation_delay
        self.current_frame = 0
        self.animation_timer = 0
        self.name = name
        
        # Añadir rectángulo para el sistema de culling
        if len(frames) > 0:
            frame_width = frames[0].get_width()
            frame_height = frames[0].get_height()
            self.rect = pygame.Rect(x, y, frame_width, frame_height)
        else:
            self.rect = pygame.Rect(x, y, 32, 32)  # Tamaño por defecto

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = 0
        
        # Actualizar rectángulo para el sistema de culling
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen, camera_offset):
        frame = self.frames[self.current_frame]
        screen.blit(frame, (self.x - camera_offset[0], self.y - camera_offset[1]))