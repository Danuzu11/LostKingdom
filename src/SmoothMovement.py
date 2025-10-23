import pygame
import math

class SmoothMovement:
    """
    Sistema de movimiento suavizado para el jugador.
    Implementa interpolación, easing y momentum para movimientos más fluidos.
    """
    
    def __init__(self):
        # Variables de posición
        self.current_x = 0
        self.target_x = 0
        self.current_y = 0
        self.target_y = 0
        
        # Variables de velocidad
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Parámetros de suavizado
        self.acceleration = 0.8  # Velocidad de aceleración (0-1)
        self.friction = 0.85     # Fricción para desaceleración (0-1)
        self.max_speed = 210     # Velocidad máxima del jugador
        
        # Variables para momentum
        self.momentum_x = 0
        self.momentum_y = 0
        self.momentum_decay = 0.9
        
    def set_target_position(self, x, y):
        """Establece la posición objetivo para el movimiento suavizado."""
        self.target_x = x
        self.target_y = y
        
    def set_velocity(self, velocity_x, velocity_y):
        """Establece la velocidad objetivo."""
        self.target_x = self.current_x + velocity_x
        self.target_y = self.current_y + velocity_y
        
    def update(self, dt):
        """
        Actualiza el movimiento suavizado.
        dt: delta time en milisegundos
        """
        # Calcular diferencia hacia el objetivo
        diff_x = self.target_x - self.current_x
        diff_y = self.target_y - self.current_y
        
        # Aplicar aceleración gradual
        if abs(diff_x) > 1:  # Solo acelerar si hay distancia significativa
            self.velocity_x += diff_x * self.acceleration * (dt / 1000)
            # Limitar velocidad máxima
            self.velocity_x = max(-self.max_speed, min(self.max_speed, self.velocity_x))
        else:
            # Desaceleración gradual cuando está cerca del objetivo
            self.velocity_x *= self.friction
            
        if abs(diff_y) > 1:
            self.velocity_y += diff_y * self.acceleration * (dt / 1000)
            self.velocity_y = max(-self.max_speed, min(self.max_speed, self.velocity_y))
        else:
            self.velocity_y *= self.friction
            
        # Aplicar momentum
        self.velocity_x += self.momentum_x
        self.velocity_y += self.momentum_y
        
        # Decaer momentum
        self.momentum_x *= self.momentum_decay
        self.momentum_y *= self.momentum_decay
        
        # Actualizar posición
        self.current_x += self.velocity_x * (dt / 1000)
        self.current_y += self.velocity_y * (dt / 1000)
        
        # Detener movimiento si la velocidad es muy pequeña
        if abs(self.velocity_x) < 0.5:
            self.velocity_x = 0
        if abs(self.velocity_y) < 0.5:
            self.velocity_y = 0
            
    def add_momentum(self, momentum_x, momentum_y):
        """Añade momentum al movimiento (útil para knockback, saltos, etc.)."""
        self.momentum_x += momentum_x
        self.momentum_y += momentum_y
        
    def get_position(self):
        """Retorna la posición actual suavizada."""
        return self.current_x, self.current_y
        
    def get_velocity(self):
        """Retorna la velocidad actual."""
        return self.velocity_x, self.velocity_y
        
    def reset(self, x, y):
        """Reinicia el sistema de movimiento a una posición específica."""
        self.current_x = x
        self.current_y = y
        self.target_x = x
        self.target_y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.momentum_x = 0
        self.momentum_y = 0


class EasingFunctions:
    """
    Funciones de easing para transiciones suaves.
    """
    
    @staticmethod
    def ease_out_cubic(t):
        """Easing cúbico de salida - rápido al inicio, lento al final."""
        return 1 - pow(1 - t, 3)
        
    @staticmethod
    def ease_in_out_quad(t):
        """Easing cuadrático de entrada y salida - lento al inicio y final."""
        return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2
        
    @staticmethod
    def ease_out_elastic(t):
        """Easing elástico - efecto de rebote."""
        if t == 0 or t == 1:
            return t
        return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1
        
    @staticmethod
    def apply_easing(current, target, progress, easing_func):
        """Aplica una función de easing entre dos valores."""
        return current + (target - current) * easing_func(progress)


class AnimationSmoother:
    """
    Sistema para suavizar las transiciones de animación.
    """
    
    def __init__(self):
        self.current_frame = 0
        self.target_frame = 0
        self.frame_progress = 0.0
        self.animation_speed = 1.0
        self.smooth_transition = False
        self.transition_progress = 0.0
        
    def set_target_frame(self, frame, smooth=True):
        """Establece el frame objetivo con transición suave opcional."""
        if smooth and frame != self.current_frame:
            self.smooth_transition = True
            self.transition_progress = 0.0
        self.target_frame = frame
        
    def update(self, dt, total_frames, animation_delay):
        """
        Actualiza la animación suavizada.
        dt: delta time
        total_frames: número total de frames en la animación
        animation_delay: delay entre frames en ms
        """
        if self.smooth_transition:
            # Transición suave entre frames
            self.transition_progress += dt / (animation_delay * 2)  # Transición en 2x el delay
            if self.transition_progress >= 1.0:
                self.current_frame = self.target_frame
                self.smooth_transition = False
                self.transition_progress = 0.0
        else:
            # Animación normal
            self.frame_progress += dt * self.animation_speed
            if self.frame_progress >= animation_delay:
                self.frame_progress = 0.0
                self.current_frame = (self.current_frame + 1) % total_frames
                
    def get_current_frame(self):
        """Retorna el frame actual considerando transiciones suaves."""
        if self.smooth_transition:
            # Interpolación entre frames
            progress = EasingFunctions.ease_in_out_quad(self.transition_progress)
            return int(self.current_frame + (self.target_frame - self.current_frame) * progress)
        return self.current_frame
