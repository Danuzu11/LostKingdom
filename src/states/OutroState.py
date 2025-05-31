import pygame
from gale.state import BaseState
from gale.input_handler import InputData
import settings
import textwrap

class OutroState(BaseState):
    def enter(self):
        # Variables para el fade in/out
        self.fade_alpha = 255
        self.fade_surface = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.fade_speed = 3
        self.fade_in = True
        self.fade_out = False
        
        settings.SOUNDS["boss"].stop()  
        settings.SOUNDS["outro"].play(-1)
        settings.SOUNDS["outro"].set_volume(1.0)
        # Variables para el texto
        self.font = settings.FONTS["medium"]
        self.font2 = settings.FONTS["small"]
        self.current_text = ""
        self.full_text = ""
        self.text_speed = 0.05
        self.text_timer = 0
        self.current_paragraph = 0
        self.waiting_for_input = False
        
        # Variables para el texto en multiples líneas
        self.wrapped_lines = []
        self.current_line = 0
        self.max_width = settings.WINDOW_WIDTH - 100

        self.story_paragraphs = [
            "Con un golpe final, el Rey Oscuro cae derrotado. Su corona se desvanece en el aire, liberando al reino de su maldición...",
            "Las sombras que una vez cubrían estas tierras comienzan a disiparse. La luz del sol, olvidada durante tanto tiempo, vuelve a bañar los muros del castillo.",
            "Pero mientras contemplas la victoria, una inquietante sensación te invade. ¿Realmente has derrotado al verdadero mal?",
            "En las profundidades del reino, algo más oscuro y antiguo despierta. Esta batalla, que parecía el final, es solo el comienzo de una aventura mucho mayor...",
            "El Reino Perdido ha sido liberado, pero nuevas sombras se ciernen en el horizonte. ¿Estás listo para enfrentar lo que está por venir?"
        ]

    def wrap_text(self, text):
        """Envolver el texto en múltiples líneas"""
        return textwrap.wrap(text, width=50)

    def update(self, dt: float) -> None:
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

        # Actualizar el texto si no estamos esperando input
        if not self.waiting_for_input:
            self.text_timer += dt
            if self.text_timer >= self.text_speed:
                self.text_timer = 0
                if len(self.current_text) < len(self.full_text):
                    self.current_text = self.full_text[:len(self.current_text) + 1]
                    # Actualizar las líneas envueltas cada vez que cambia el texto
                    self.wrapped_lines = self.wrap_text(self.current_text)
                else:
                    self.waiting_for_input = True

    def render(self, surface):
        # Fondo negro
        # surface.fill((0, 0, 0))  

        surface.blit(settings.TEXTURES["outro"], (0, 0))

        # Renderizar el texto actual en multiples lineas
        if self.current_paragraph < len(self.story_paragraphs):
            y_position = surface.get_height() // 2 - (len(self.wrapped_lines) * 20)
            for line in self.wrapped_lines:
                text = self.font.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(surface.get_width() // 2, y_position))
                surface.blit(text, text_rect)
                y_position += 25

            if self.waiting_for_input:
                continue_text = self.font2.render("Presiona ENTER para continuar...", True, (200, 200, 200))
                continue_rect = continue_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 150))
                surface.blit(continue_text, continue_rect)

        # Aplicar el fade in o fade out
        if self.fade_in or self.fade_out:
            self.fade_surface.set_alpha(self.fade_alpha)
            surface.blit(self.fade_surface, (0, 0))

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            if self.waiting_for_input:
                # Detener el sonido actual si está sonando
                settings.SOUNDS["maquinaescribir"].stop()
                # Reproducir el sonido de máquina de escribir
                settings.SOUNDS["maquinaescribir"].play(loops=-1)
                
                self.current_paragraph += 1
                if self.current_paragraph < len(self.story_paragraphs):
                    self.full_text = self.story_paragraphs[self.current_paragraph]
                    self.current_text = ""
                    self.wrapped_lines = []
                    self.waiting_for_input = False
                else:
                    # Detener el sonido cuando termina el outro
                    settings.SOUNDS["maquinaescribir"].stop()
                    self.fade_out = True
                    self.fade_alpha = 0

        # Permitir saltar el outro con la tecla ESC
        if input_id == "escape" and input_data.pressed:
            # Detener el sonido si se salta el outro
            settings.SOUNDS["maquinaescribir"].stop()
            self.fade_out = True
            self.fade_alpha = 0