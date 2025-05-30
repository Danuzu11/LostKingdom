import pygame
import settings

def fade(screen, width, height, fade_in=False, duration=500):
    """
    Realiza un efecto de fade in o fade out.

    Args:
        screen: La superficie de la pantalla de Pygame.
        width: El ancho de la pantalla.
        height: La altura de la pantalla.
        fade_in: True para fade in, False para fade out.
        duration: La duración del efecto en milisegundos.
    """
    fade_surface = pygame.Surface((width, height))
    # Ponemos por defecto el color negro
    fade_surface.fill((0, 0, 0))  
    if fade_in:
        alpha_start, alpha_end = 255, 0
    else:
        alpha_start, alpha_end = 0, 255

    # Numero de pasos por defecto
    steps = 50  
    delay = duration / steps

    for i in range(steps + 1):
        alpha = alpha_start + (alpha_end - alpha_start) * i / steps
        fade_surface.set_alpha(int(alpha))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(delay))
        
        
def update_vertical_acceleration(vertical_velocity, gravity , y , ground_y , vertical_movement, current_state):
    if vertical_movement:
        vertical_velocity += gravity
        y += vertical_velocity
        current_state= "jump"        
        # Verificamos si hemos llegado al piso
        if y >= ground_y:
            y = ground_y
            vertical_movement = False
            vertical_velocity = 0
            current_state= "idle"   

    return vertical_velocity, y, vertical_movement , current_state

# Funcion que me permite extraer los sprites de una hoja de animacion de un unico moveset
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

# Funcion que me permite extraer los sprites de una hoja de animacion de muchos movesets
# En este caso debemos escoger el rango de sprites que queremos extraer segun querramos
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
        # Como los sprite del monotauro esta volteado , debemos voltearlos todos
        if sprite_sheet_name == "Minotaur":
            scaled_surface = pygame.transform.flip(scaled_surface, True, False)

        animations.append(scaled_surface)  
                  
    return animations

def extract_animation_moveset(spritsheet_surface, range:tuple):

    start_idx = range[0]
    end_idx = start_idx  + range[1]     
    moveset = spritsheet_surface[
            start_idx:end_idx
    ]
    
    return moveset
    


        
