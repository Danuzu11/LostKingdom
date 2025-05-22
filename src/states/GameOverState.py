import pygame
from gale.state import BaseState
from gale.input_handler import InputData
import settings

class GameOverState(BaseState):
    def enter(self):
        
        self.fade_alpha = 255  
        self.fade_surface = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.fade_speed = 3 
        self.fade_in = True  
        self.fade_out = False 
        settings.SOUNDS["principal_theme"].stop()
        
        # settings.SOUNDS["principal_theme"].play(loops=-1)
        self.font = pygame.font.Font(None, 48)  # Fuente para el texto
    
    def update(self, dt: float) -> None:
        """
        Actualiza la lógica del estado.
        """
        # Manejar el fade in
        if self.fade_in:
            self.fade_alpha = max(0, self.fade_alpha - self.fade_speed)
            if self.fade_alpha == 0:
                self.fade_in = False
        
        # Manejar el fade out   
        if self.fade_out:
            self.fade_alpha = min(255, self.fade_alpha + self.fade_speed)
            if self.fade_alpha == 255:
                self.state_machine.change("menu") 
                
    def render(self, surface):
        surface.fill((0, 0, 0))  # Fondo negro
        surface.blit(settings.TEXTURES["death2"], (0, 0))
        gameOverText = self.font.render("Game Over", True, (255, 0, 0))
        gameOverText_rect = gameOverText.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
        surface.blit(gameOverText, gameOverText_rect)
        text = self.font.render("Press ENTER to Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 1.5))
        surface.blit(text, text_rect)
        
        # Aplicar el fade in o fade out
        if self.fade_in or self.fade_out:
            self.fade_surface.set_alpha(self.fade_alpha)
            surface.blit(self.fade_surface, (0, 0))

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("menu")
            # Iniciar el fade out
            self.fade_out = True
            self.fade_alpha = 0  # Reiniciar el alpha para el fade out