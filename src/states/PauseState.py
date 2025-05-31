import pygame
from gale.state import BaseState
from gale.input_handler import InputData
import settings

class PauseState(BaseState):
    def enter(self, **params: dict):
        self.params = params
        self.player = params.get("player")
        self.font = settings.FONTS["medium"]  # Fuente para el texto

    def render(self, surface):
        # Renderizar el estado anterior
        self.params["previous_state"].render(surface)

        # Mostrar el mensaje de pausa
        text = self.font.render("Juego en pausa. Presione 'P' para continuaar", True, (255, 255, 255))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text, text_rect)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            # Volver al estado anterior
            self.state_machine.change("play", **self.params)