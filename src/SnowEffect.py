import pygame
import random
import math

class SnowParticle:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 

        # Usamos la distribucion uniforme para variar el tamaño de las partículas
        self.size = random.randint(1, 2) 
        # Usamos la distribucion uniforme para variar la velocidad de las partículas
        self.speed = random.uniform(0.2, 0.4)  

        # Aqui usamos un angulo fijo pero tambien podriamos usar un angulo aleatorio pero meh no guta aun, me gusta que venga defrente
        self.angle = 360   

    # Actualizamos la posición de la partícula mañosa
    def update(self, dt):
        # Mover la partícula en diagonal , el -0.2 es para asignar el angulo de la partícula en x y el 1 es para asignar la velocidad hacia abajo
        self.x += self.speed * dt * -0.2
        self.y += self.speed * dt * 1
   

    def render(self, surface, camera_offset):
        # Dibujar la partícula con el offset de la cámara
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        pygame.draw.circle(surface, (255, 255, 255), (screen_x, screen_y), self.size)

class SnowEffect:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Lista de partículas mañosas
        self.particles = []

        # Maximo de partículas mañosas que podemos tener en pantalla
        self.max_particles = 1000  

        # Temporizador para el spawn de partículas mañosas
        self.spawn_timer = 0

        # Tiempo de espera para que no se creen particula a lo loco
        self.spawn_delay = 5

    def update(self, dt, camera_offset):
        
        # Revisamos las partículas existentes y verificamos si salen de la pantalla
        for particle in self.particles[:]:
            
            # Actualizamos la posición de la partícula mañosa
            particle.update(dt)
            
            # Eliminamos si se van pa la puta
            if particle.y > self.height + 100:
                self.particles.remove(particle)

        # Aumentamos el temporizador
        self.spawn_timer += dt

        # Y si el temporrizador en mas grande que el tiempo de espera creamos otra partícula mañosa
        if self.spawn_timer >= self.spawn_delay and len(self.particles) < self.max_particles:
            
            # Ponemos el temporizador en 0
            self.spawn_timer = 0
            
            # Asignamos una posición aleatoria para la partícula mañosa segun la posicion de la camara
            # El rango en x de generacionsera desde -10 pixeles de la camara hasta +50 pixeles de la camara
            spawn_x = random.randint(
                int(camera_offset[0] ), 
                int(camera_offset[0] + self.width + 100)
            )

            # Y el rango en Y sera +10 mas arriba de la posicion de la camara para simular que caen desde el cielo
            spawn_y = camera_offset[1] - 10

            # Y ahora teniendo las coordenadas de creacion si creamos la partícula mañosa
            self.particles.append(SnowParticle(spawn_x, spawn_y))

    # Ciclo render para dibujar en pantalla todas las particulas que tenemos en la lista de partículas mañosas
    def render(self, surface, camera_offset):
        for particle in self.particles:
            particle.render(surface, camera_offset)