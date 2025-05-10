import pygame
import settings 

class AnimatedItem:
    def __init__(self, x, y, frames, animation_delay=1000):
       
        # :param frames: Lista de superficies (frames) para la animación.
        # :param animation_delay: Tiempo en milisegundos entre cada frame.
 
        self.x = x
        self.y = y
        self.frames = frames
        self.animation_delay = animation_delay
        self.current_frame = 0
        self.animation_timer = 0

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = 0

    def draw(self, screen, camera_offset):
        frame = self.frames[self.current_frame]
        screen.blit(frame, (self.x - camera_offset[0], self.y - camera_offset[1]))