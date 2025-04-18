import pygame

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





        
