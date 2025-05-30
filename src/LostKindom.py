
import pygame

from gale.game import Game
from gale.state import StateMachine
from gale.input_handler import InputData

import settings

from src import states

class LostKindom(Game):
    def init(self) -> None:
        self.state_machine = StateMachine(
            {
                "video": states.VideoState,
                "intro": states.IntroState,  
                "menu": states.MenuState,# Añadir el nuevo estado
                "play": states.PlayState,
                "pause": states.PauseState,
                "game_over": states.GameOverState,
            }
        )
        self.state_machine.game = self
        self.state_machine.change("play")       
        # settings.SOUNDS["principal_theme"].play(loops=-1)
        
    def update(self, dt: float) -> None:
        self.state_machine.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        # surface.blit(settings.TEXTURES["menu"], (0, 0))
        self.state_machine.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:

        if input_id == "quit" and input_data.pressed:
            self.quit()
        else:
            self.state_machine.on_input(input_id, input_data)