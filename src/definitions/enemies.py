
import settings
import pygame

# Aqui vamos a definir la estadistica de los enemigos, ya que tendremos varios y debemos simplificar el proceso para el anexo data de cada uno de ellos
# Estos datos los vamos a usar en la clase ENEMY 

Enemies = {
    "NightBorne":{
            "speed": settings.ENEMY_SPEED,
            "delay": settings.ANIMATIONS_ENEMY_DELAYS,
            
            # Correcion de la posicion inicial en x
            "position_x_correct": 80,
            "base_rect_width": 25,
            "base_rect_height": 45,
            
            # Coreccion de las posiciones del rectangulo de colision del enemigo
            "enemy_rect_offset_x": 50 , 
            "enemy_rect_offset_y": -45,
            
            "floor_correct": 40,
            
            # Tama;os para los offset del rectangulo de colision (acomodar su posicion inicial en el sprite del enemigo y se vea mas acorde)
            "attack_rect_width": 60,
            # Correccion extra para la posicion en y , para acomodar el sprite del enemigo en Y
            "extra_custom_offset_y": -60,
            
            "scale_factor": 1.6,
            "max_health": 100,
            "attack_range": 60,
            "detection_range": 100,
            "attack_damage": 13,
            
            # Corecccion de la barra de vida del enemigo
            "health_bar_offset_x": 40,   
            "health_bar_offset_y": 0,
   
        },
    "Golem":{
            "speed": settings.ENEMY_SPEED,
            "delay": settings.ANIMATIONS_ENEMY_DELAYS,
            
            # Correccion de posicion en x , ya que manejamos escalas distintas entonces nos ayuda a centrar a nuestro enemigo
            "position_x_correct": 100,
            
            # Tama;o base ancho y alto del rectangulo de colision del enemigo
            "base_rect_width": 50,
            "base_rect_height": 45,
            
            # Tama;os para los offset del rectangulo de colision (acomodar su posicion inicial en el sprite del enemigo y se vea mas acorde)
            "enemy_rect_offset_x": 70 , 
            "enemy_rect_offset_y": -45,
            
            # Agranda el rectangulo de colision para los ataques fisicos
            "attack_rect_width": 80,
            
            # Correccion extra para la posicion en y , para acomodar el sprite del enemigo en Y
            "extra_custom_offset_y": -60,
            
            # Factor de escalado entre mayor el numero mas grande se crea el sprite
            "scale_factor": 3,
            
            # Datos base del enemigo
            "max_health": 200,
            "attack_range": 60,
            "detection_range": 200,
            "attack_damage": 10,
            
            # Correcion en la posicion del piso base del enemigo para que no cambie segun su rectangulo de colision
            "floor_correct": 70,
            
            # Correcccion de la barra de vida del enemigo
            "health_bar_offset_x": 0,   
            "health_bar_offset_y": 0,
    },
    "Minotaur": {
        "speed": settings.ENEMY_SPEED,
        "delay": settings.ANIMATIONS_ENEMY_DELAYS,
            
        # Correccion de posicion en x , ya que manejamos escalas distintas entonces nos ayuda a centrar a nuestro enemigo
        "position_x_correct": 250,
            
        # Tama;o base ancho y alto del rectangulo de colision del enemigo
        "base_rect_width": 60,
        "base_rect_height": 85,
            
        # Tama;os para los offset del rectangulo de colision (acomodar su posicion inicial en el sprite del enemigo y se vea mas acorde)
        "enemy_rect_offset_x": 180 , 
        "enemy_rect_offset_y": -95,
            
        # Agranda el rectangulo de colision para los ataques fisicos
        "attack_rect_width": 200,
            
        # Correccion extra para la posicion en y , para acomodar el sprite del enemigo en Y
        "extra_custom_offset_y": -185,
            
        # Factor de escalado entre mayor el numero mas grande se crea el sprite
        "scale_factor": 1.8,
            
        # Datos base del enemigo
        # "max_health": 200,
        "max_health": 100,
        "attack_range": 10,
        "detection_range": 200,
        "attack_damage": 30,
            
        # Correcion en la posicion del piso base del enemigo para que no cambie segun su rectangulo de colision
        "floor_correct": 70,
            
        # Correcccion de la barra de vida del enemigo
        "health_bar_offset_x": 45,   
        "health_bar_offset_y": 0,
    },
    "MechaGolem": {
        "speed": settings.ENEMY_SPEED,
        "delay": settings.ANIMATIONS_ENEMY_DELAYS,
        
        # Corrección de posición en x
        "position_x_correct": 80,
        
        # Tamaño base del rectángulo de colisión
        "base_rect_width": 50,
        "base_rect_height": 45,
        
        # Offset del rectángulo de colisión
        "enemy_rect_offset_x": 50,
        "enemy_rect_offset_y": -45,
        
        # Rectángulo de ataque
        "attack_rect_width": 60,
        
        # Corrección extra para la posición en Y
        "extra_custom_offset_y": -45,
        
        # Factor de escalado
        "scale_factor": 1.5,
        
        # Datos base del enemigo
        "max_health": 150,
        "attack_range": 60,
        "detection_range": 200,
        "attack_damage": 10,
        
        # Correccion del piso
        "floor_correct": 70,
        
        # Corrección de la barra de vida
        "health_bar_offset_x": 40,
        "health_bar_offset_y": 0,
    },
    "Executoner": {
        "speed": settings.ENEMY_SPEED,
        "delay": settings.ANIMATIONS_ENEMY_DELAYS,
        
        # Corrección de posición en x
        "position_x_correct": 80,
        
        # Tamaño base del rectángulo de colisión
        "base_rect_width": 25,
        "base_rect_height": 45,
        
        # Offset del rectángulo de colisión
        "enemy_rect_offset_x": 50,
        "enemy_rect_offset_y": -45,
        
        # Rectángulo de ataque
        "attack_rect_width": 60,
        
        # Corrección extra para la posición en Y
        "extra_custom_offset_y": -60,
        
        # Factor de escalado 
        "scale_factor": 1.2,
        
        # Datos base del enemigo
        "max_health": 80,
        "attack_range": 60,
        "detection_range": 150,
        "attack_damage": 15,
        
        # Corrección del piso
        "floor_correct": 40,
        
        # Corrección de la barra de vida
        "health_bar_offset_x": 40,
        "health_bar_offset_y": 0,
    },
}