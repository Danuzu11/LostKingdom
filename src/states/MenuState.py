import pygame
from gale.state import BaseState
from gale.input_handler import InputData
import settings

class MenuState(BaseState):
    def enter(self):
        """
        Se ejecuta al entrar en el estado.
        """
        self.font = pygame.font.Font(None, 48)  # Fuente para el texto

    def render(self, surface):
        """
        Renderiza el menú en la pantalla.
        """
        surface.fill((0, 0, 0))  # Fondo negro
        text = self.font.render("Press ENTER to Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text, text_rect)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        """
        Maneja las entradas del usuario.
        """
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("play")
