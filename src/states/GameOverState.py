import pygame
from gale.state import BaseState
from gale.input_handler import InputData
import settings

class GameOverState(BaseState):
    def enter(self):
        settings.SOUNDS["principal_theme"].play(loops=-1)
        self.font = pygame.font.Font(None, 48)  # Fuente para el texto

    def render(self, surface):
        surface.fill((0, 0, 0))  # Fondo negro
        # surface.blit(settings.TEXTURES["menu"], (0, 0))
        gameOverText = self.font.render("Game Over", True, (255, 0, 0))
        gameOverText_rect = gameOverText.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
        surface.blit(gameOverText, gameOverText_rect)
        text = self.font.render("Press ENTER to Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text, text_rect)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("menu")
