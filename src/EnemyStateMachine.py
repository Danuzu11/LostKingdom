import pygame
from src.definitions.enemies import Enemies

class EnemyStateMachine:
    """
    Sistema de estados mejorado para enemigos.
    Respeta completamente el sistema de escalado y correcciones de enemies.py
    """
    
    def __init__(self, enemy):
        self.enemy = enemy
        self.states = {
            'idle': IdleState(),
            'patrol': PatrolState(),
            'chase': ChaseState(),
            'attack': AttackState(),
            'stunned': StunnedState(),
            'hurt': HurtState()
        }
        self.current_state = 'idle'
        self.state_timer = 0
        self.last_player_position = None
        self.patrol_direction = 1  # 1 = derecha, -1 = izquierda
        self.patrol_distance = 100  # Distancia de patrullaje
        self.patrol_start_x = enemy.x
    
    def update(self, delta_time, player, solid_objects):
        """Actualiza el estado actual del enemigo respetando las definiciones de enemies.py"""
        # Solo actualizar estados cada cierto tiempo para evitar cambios muy frecuentes
        if self.state_timer > 100:  # 100ms entre cambios de estado
            current_state_obj = self.states[self.current_state]
            new_state = current_state_obj.update(self.enemy, player, solid_objects, delta_time, self)
            
            if new_state and new_state != self.current_state:
                self.transition_to(new_state)
                self.state_timer = 0  # Reset timer después de cambio de estado
            else:
                self.state_timer = 0  # Reset timer si no hay cambio
        
        self.state_timer += delta_time
    
    def transition_to(self, new_state):
        """Transición suave entre estados manteniendo las correcciones de escalado"""
        if new_state in self.states:
            self.states[self.current_state].exit(self.enemy)
            self.current_state = new_state
            self.states[self.current_state].enter(self.enemy)
            self.state_timer = 0
            # Resetear frame de animación al cambiar de estado
            self.enemy.current_frame = 0
    
    def get_distance_to_player(self, player):
        """Calcula la distancia al jugador respetando el escalado"""
        return abs(self.enemy.x - player.x)
    
    def can_see_player(self, player, solid_objects):
        """Verifica si puede ver al jugador respetando el rango de detección"""
        distance = self.get_distance_to_player(player)
        return distance <= self.enemy.detection_range
    
    def is_in_attack_range(self, player):
        """Verifica si está en rango de ataque respetando las definiciones"""
        distance = self.get_distance_to_player(player)
        return distance <= self.enemy.attack_range

class IdleState:
    """Estado de reposo - busca al jugador respetando el sistema de escalado"""
    
    def update(self, enemy, player, solid_objects, delta_time, state_machine):
        # Verificar si puede ver al jugador
        if state_machine.can_see_player(player, solid_objects):
            return 'chase'
        
        # Si no puede ver al jugador, patrullar ocasionalmente
        if state_machine.state_timer > 2000:  # 2 segundos
            return 'patrol'
        
        return 'idle'
    
    def enter(self, enemy):
        enemy.current_state = "idle"
        enemy.horizontal_velocity = 0
    
    def exit(self, enemy):
        pass

class PatrolState:
    """Estado de patrullaje - movimiento básico respetando escalado"""
    
    def update(self, enemy, player, solid_objects, delta_time, state_machine):
        # Verificar si puede ver al jugador
        if state_machine.can_see_player(player, solid_objects):
            return 'chase'
        
        # Patrullaje básico
        patrol_distance = abs(enemy.x - state_machine.patrol_start_x)
        if patrol_distance >= state_machine.patrol_distance:
            state_machine.patrol_direction *= -1
            state_machine.patrol_start_x = enemy.x
        
        # Mover en dirección de patrullaje
        enemy.horizontal_velocity = state_machine.patrol_direction * enemy.velocity
        enemy.direction = state_machine.patrol_direction
        enemy.current_state = "run"
        
        # Volver a idle después de un tiempo
        if state_machine.state_timer > 3000:  # 3 segundos
            return 'idle'
        
        return 'patrol'
    
    def enter(self, enemy):
        enemy.current_state = "run"
    
    def exit(self, enemy):
        pass

class ChaseState:
    """Estado de persecución - sigue al jugador respetando escalado"""
    
    def update(self, enemy, player, solid_objects, delta_time, state_machine):
        # Verificar si está en rango de ataque
        if state_machine.is_in_attack_range(player):
            return 'attack'
        
        # Verificar si perdió de vista al jugador
        if not state_machine.can_see_player(player, solid_objects):
            return 'idle'
        
        # Perseguir al jugador
        if player.x > enemy.x:
            enemy.horizontal_velocity = enemy.velocity
            enemy.direction = 1
        else:
            enemy.horizontal_velocity = -enemy.velocity
            enemy.direction = -1
        
        enemy.current_state = "run"
        return 'chase'
    
    def enter(self, enemy):
        enemy.current_state = "run"
    
    def exit(self, enemy):
        pass

class AttackState:
    """Estado de ataque - respeta el sistema de cooldown y escalado"""
    
    def update(self, enemy, player, solid_objects, delta_time, state_machine):
        # Verificar si está en rango de ataque
        if not state_machine.is_in_attack_range(player):
            return 'chase'
        
        # Verificar cooldown de ataque
        current_time = pygame.time.get_ticks()
        if current_time - enemy.last_attack_time >= enemy.attack_cooldown:
            # Realizar ataque
            enemy.attacking = True
            enemy.current_state = "attack"
            enemy.last_attack_time = current_time
            
            # Aplicar daño al jugador si está en rango
            if enemy.rect.colliderect(player.king_rect):
                player.receive_hit(enemy.direction, enemy.attack_damage)
        
        # Volver a chase después del ataque
        if state_machine.state_timer > 1000:  # 1 segundo
            enemy.attacking = False
            return 'chase'
        
        return 'attack'
    
    def enter(self, enemy):
        enemy.current_state = "attack"
        enemy.attacking = True
    
    def exit(self, enemy):
        enemy.attacking = False

class StunnedState:
    """Estado de aturdimiento - cuando recibe daño"""
    
    def update(self, enemy, player, solid_objects, delta_time, state_machine):
        # Volver a idle después del aturdimiento
        if state_machine.state_timer > 500:  # 0.5 segundos
            return 'idle'
        
        return 'stunned'
    
    def enter(self, enemy):
        enemy.current_state = "idle"
        enemy.horizontal_velocity = 0
    
    def exit(self, enemy):
        pass

class HurtState:
    """Estado de herido - cuando recibe daño respetando el sistema de escalado"""
    
    def update(self, enemy, player, solid_objects, delta_time, state_machine):
        # Volver a idle después de recibir daño
        if state_machine.state_timer > enemy.hurt_duration:
            enemy.hurt = False
            return 'idle'
        
        return 'hurt'
    
    def enter(self, enemy):
        enemy.current_state = "idle"
        enemy.hurt = True
    
    def exit(self, enemy):
        enemy.hurt = False
