import pygame
from src.definitions.enemies import Enemies

class EnemyPool:
    """
    Sistema de Object Pooling para enemigos.
    Optimiza la gestión de memoria reutilizando objetos Enemy.
    Respeta el sistema de escalado y correcciones manuales de enemies.py
    """
    
    def __init__(self, max_size=20):
        self.max_size = max_size
        self.available_enemies = []
        self.active_enemies = []
        
        # Pre-crear enemigos para el pool
        self._precreate_enemies()
    
    def _precreate_enemies(self):
        """Pre-crea enemigos para el pool respetando las definiciones de enemies.py"""
        # Crear un enemigo de cada tipo para el pool
        enemy_types = ["NightBorne", "Golem", "Minotaur", "MechaGolem", "Executoner"]
        
        for enemy_type in enemy_types:
            # Crear enemigo temporal para el pool
            temp_enemy = self._create_enemy_base(enemy_type)
            temp_enemy.is_dead = True  # Marcar como inactivo
            temp_enemy.pool_type = enemy_type  # Guardar el tipo para reutilización
            self.available_enemies.append(temp_enemy)
    
    def _create_enemy_base(self, enemy_type):
        """Crea un enemigo base respetando las definiciones de enemies.py"""
        from src.Enemy import Enemy
        return Enemy(0, 0, enemy_type)
    
    def get_enemy(self, x, y, enemy_type):
        """
        Obtiene un enemigo del pool o crea uno nuevo si es necesario.
        Respeta completamente el sistema de escalado y correcciones de enemies.py
        """
        # Buscar enemigo disponible del tipo correcto
        for i, enemy in enumerate(self.available_enemies):
            if hasattr(enemy, 'pool_type') and enemy.pool_type == enemy_type:
                # Reutilizar enemigo del pool
                enemy = self.available_enemies.pop(i)
                self._reset_enemy(enemy, x, y, enemy_type)
                self.active_enemies.append(enemy)
                return enemy
        
        # Si no hay enemigos disponibles del tipo correcto, crear uno nuevo
        if len(self.active_enemies) < self.max_size:
            new_enemy = self._create_enemy_base(enemy_type)
            self._reset_enemy(new_enemy, x, y, enemy_type)
            self.active_enemies.append(new_enemy)
            return new_enemy
        
        # Si el pool está lleno, reutilizar el enemigo más antiguo
        if self.active_enemies:
            oldest_enemy = self.active_enemies.pop(0)
            self._reset_enemy(oldest_enemy, x, y, enemy_type)
            self.active_enemies.append(oldest_enemy)
            return oldest_enemy
        
        # Fallback: crear enemigo sin pool
        return self._create_enemy_base(enemy_type)
    
    def _reset_enemy(self, enemy, x, y, enemy_type):
        """
        Reinicializa un enemigo respetando todas las correcciones de enemies.py
        """
        # Reinicializar con las definiciones correctas
        enemy.__init__(x, y, enemy_type)
        enemy.is_dead = False
        enemy.pool_type = enemy_type
    
    def return_enemy(self, enemy):
        """
        Devuelve un enemigo al pool.
        Respeta el sistema de escalado al mantener las definiciones
        """
        if enemy in self.active_enemies:
            self.active_enemies.remove(enemy)
            enemy.is_dead = True
            enemy.pool_type = getattr(enemy, 'pool_type', enemy.name)
            self.available_enemies.append(enemy)
    
    def cleanup_dead_enemies(self):
        """
        Limpia enemigos muertos del pool.
        Mantiene las definiciones de escalado intactas
        """
        enemies_to_remove = []
        for enemy in self.active_enemies:
            if enemy.is_dead and enemy.death_animation_completed:
                enemies_to_remove.append(enemy)
        
        for enemy in enemies_to_remove:
            self.return_enemy(enemy)
    
    def get_active_enemies(self):
        """Retorna solo los enemigos activos (vivos)"""
        return [enemy for enemy in self.active_enemies if not enemy.is_dead]
    
    def get_pool_stats(self):
        """Información del estado del pool para debugging"""
        return {
            'available': len(self.available_enemies),
            'active': len(self.active_enemies),
            'total': len(self.available_enemies) + len(self.active_enemies)
        }
