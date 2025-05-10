import pygame
import settings

def update_vertical_acceleration(vertical_velocity, gravity , y , ground_y , vertical_movement):
    if vertical_movement:
        vertical_velocity += gravity
        y += vertical_velocity
                
        # Verificar si hemos llegado al suelo
        if y >= ground_y:
            y = ground_y
            vertical_movement = False
            vertical_velocity = 0

    return vertical_velocity, y, vertical_movement

def extract_animation_unique_spritesheet(sprite_sheet_name,moveset_name,scale_factor=1):

    textures = settings.COMPLEX_TEXTURES[sprite_sheet_name][moveset_name]
    frames = settings.COMPLEX_FRAMES[sprite_sheet_name][moveset_name]
    animations = []
  
    for frame in frames:
        surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
        surface.blit(textures, (0, 0), frame)
        scaled_surface = pygame.transform.scale(
            surface,
            (
                int(surface.get_width() * scale_factor),
                int(surface.get_height() * scale_factor),
            ),
        )
        animations.append(scaled_surface)  
                  
    return animations

def extract_animation_complex_spritesheet(sprite_sheet_name,scale_factor=1):

    textures = settings.COMPLEX_TEXTURES[sprite_sheet_name][sprite_sheet_name]
    frames = settings.COMPLEX_FRAMES[sprite_sheet_name][sprite_sheet_name]
    animations = []
    
    for frame in frames:
        surface = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
        surface.blit(textures, (0, 0), frame)
        scaled_surface = pygame.transform.scale(
            surface,
            (
                int(surface.get_width() * scale_factor),
                int(surface.get_height() * scale_factor),
            ),
        )
        animations.append(scaled_surface)  
                  
    return animations

def extract_animation_moveset(spritsheet_surface, range:tuple):

    start_idx = range[0]
    end_idx = start_idx  + range[1]     
    moveset = spritsheet_surface[
            start_idx:end_idx
    ]
    
    return moveset
    


        
