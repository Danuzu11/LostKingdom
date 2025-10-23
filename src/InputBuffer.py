import pygame

class InputBuffer:
    """
    Sistema de buffer de inputs para mejorar la responsividad del combate.
    Permite que los inputs se registren con anticipación para combos más fluidos.
    """
    
    def __init__(self, buffer_time=200):
        self.buffer_time = buffer_time  # Tiempo en ms que se mantiene el input
        self.buffered_inputs = {}
        self.input_history = []
        self.max_history = 10  # Máximo de inputs en el historial
        
    def add_input(self, input_type, timestamp=None):
        """
        Añade un input al buffer.
        input_type: tipo de input ('attack', 'jump', 'move_left', etc.)
        timestamp: tiempo del input (si no se proporciona, usa el tiempo actual)
        """
        if timestamp is None:
            timestamp = pygame.time.get_ticks()
            
        self.buffered_inputs[input_type] = timestamp
        
        # Añadir al historial
        self.input_history.append((input_type, timestamp))
        if len(self.input_history) > self.max_history:
            self.input_history.pop(0)
            
    def get_buffered_input(self, input_type, current_time=None):
        """
        Verifica si hay un input en el buffer.
        Retorna True si el input está disponible y no ha expirado.
        """
        if current_time is None:
            current_time = pygame.time.get_ticks()
            
        if input_type in self.buffered_inputs:
            input_time = self.buffered_inputs[input_type]
            if current_time - input_time <= self.buffer_time:
                return True
        return False
        
    def consume_input(self, input_type):
        """
        Consume un input del buffer (lo elimina).
        Retorna True si el input estaba disponible.
        """
        if input_type in self.buffered_inputs:
            del self.buffered_inputs[input_type]
            return True
        return False
        
    def clear_input(self, input_type):
        """Elimina un input específico del buffer."""
        if input_type in self.buffered_inputs:
            del self.buffered_inputs[input_type]
            
    def clear_all(self):
        """Limpia todos los inputs del buffer."""
        self.buffered_inputs.clear()
        
    def get_available_inputs(self, current_time=None):
        """Retorna una lista de todos los inputs disponibles en el buffer."""
        if current_time is None:
            current_time = pygame.time.get_ticks()
            
        available = []
        for input_type, timestamp in self.buffered_inputs.items():
            if current_time - timestamp <= self.buffer_time:
                available.append(input_type)
        return available
        
    def cleanup_expired_inputs(self, current_time=None):
        """Limpia los inputs que han expirado del buffer."""
        if current_time is None:
            current_time = pygame.time.get_ticks()
            
        expired = []
        for input_type, timestamp in self.buffered_inputs.items():
            if current_time - timestamp > self.buffer_time:
                expired.append(input_type)
                
        for input_type in expired:
            del self.buffered_inputs[input_type]


class ComboSystem:
    """
    Sistema mejorado de combos con input buffer y timing más flexible.
    """
    
    def __init__(self, max_combo_time=800, combo_reset_time=1000):
        self.max_combo_time = max_combo_time  # Tiempo máximo entre ataques para mantener combo
        self.combo_reset_time = combo_reset_time  # Tiempo para resetear combo completamente
        self.combo_chain = []
        self.combo_timer = 0
        self.last_attack_time = 0
        self.current_combo = 1
        self.max_combo = 4
        self.combo_active = False
        
        # Timing específico para cada combo
        self.combo_timings = {
            1: 600,  # Primer ataque - ventana más larga
            2: 500,  # Segundo ataque
            3: 400,  # Tercer ataque
            4: 300   # Cuarto ataque - ventana más corta
        }
        
    def can_continue_combo(self, current_time):
        """Verifica si se puede continuar el combo."""
        if not self.combo_active:
            return True
            
        time_since_last = current_time - self.last_attack_time
        return time_since_last <= self.max_combo_time
        
    def add_attack_input(self, current_time):
        """
        Añade un input de ataque al combo.
        Retorna True si el combo se puede continuar.
        """
        if self.can_continue_combo(current_time):
            self.combo_active = True
            self.combo_timer = current_time
            self.last_attack_time = current_time
            
            # Avanzar al siguiente combo
            if self.current_combo < self.max_combo:
                self.current_combo += 1
            else:
                self.current_combo = 1  # Reiniciar al primer combo
                
            return True
        return False
        
    def reset_combo(self):
        """Reinicia el combo a su estado inicial."""
        self.current_combo = 1
        self.combo_active = False
        self.combo_chain.clear()
        
    def update(self, current_time):
        """Actualiza el sistema de combos."""
        if self.combo_active:
            time_since_last = current_time - self.last_attack_time
            if time_since_last > self.combo_reset_time:
                self.reset_combo()
                
    def get_current_combo(self):
        """Retorna el combo actual."""
        return self.current_combo
        
    def is_combo_active(self):
        """Verifica si hay un combo activo."""
        return self.combo_active
        
    def get_combo_timing(self):
        """Retorna el timing específico para el combo actual."""
        return self.combo_timings.get(self.current_combo, 500)


class AttackCancelSystem:
    """
    Sistema de cancelación de ataques para mayor fluidez.
    """
    
    def __init__(self):
        self.cancel_frames = {
            'attack1': [2, 3],  # Frames donde se puede cancelar el primer ataque
            'attack2': [1, 2],  # Frames donde se puede cancelar el segundo ataque
            'attack3': [2],     # Frames donde se puede cancelar el tercer ataque
            'attack4': []       # El cuarto ataque no se puede cancelar
        }
        
        self.cancel_to_states = {
            'jump': True,       # Se puede cancelar a salto
            'run': False,       # No se puede cancelar a correr
            'idle': False       # No se puede cancelar a idle
        }
        
    def can_cancel_attack(self, attack_type, current_frame):
        """Verifica si se puede cancelar el ataque actual."""
        if attack_type in self.cancel_frames:
            return current_frame in self.cancel_frames[attack_type]
        return False
        
    def can_cancel_to_state(self, target_state):
        """Verifica si se puede cancelar a un estado específico."""
        return self.cancel_to_states.get(target_state, False)
        
    def get_cancel_frames(self, attack_type):
        """Retorna los frames donde se puede cancelar un ataque."""
        return self.cancel_frames.get(attack_type, [])
