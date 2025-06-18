import pygame
import settings
import math

class Lighting:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.darkness = pygame.Surface((width, height))
        self.light_radius = 150
        
        # Crear una superficie para el gradiente de luz
        self.light_surface = pygame.Surface((self.light_radius * 2, self.light_radius * 2), pygame.SRCALPHA)
        for x in range(-self.light_radius, self.light_radius):
            for y in range(-self.light_radius, self.light_radius):
                distance = math.sqrt(x ** 2 + y ** 2)
                if distance < self.light_radius:
                    alpha = int(255 * (1 - distance / self.light_radius))
                    self.light_surface.set_at((x + self.light_radius, y + self.light_radius), (0, 0, 0, alpha))
        
    def update(self, player_x, player_y):
        self.darkness.fill((0, 0, 0))
        # Calcular la posición para centrar la luz en el jugador
        light_x = int(player_x - self.light_radius)
        light_y = int(player_y - self.light_radius)
        # Dibujar la luz en la posición del jugador
        self.darkness.blit(self.light_surface, (light_x, light_y))
    
    def render(self, surface):
        surface.blit(self.darkness, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)