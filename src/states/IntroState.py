import pygame
from gale.state import BaseState
from gale.input_handler import InputData
import settings
import textwrap 

class IntroState(BaseState):
    def enter(self):
        # Variables para el fade in/out
        self.fade_alpha = 255
        self.fade_surface = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.fade_speed = 3
        self.fade_in = True
        self.fade_out = False

        # Variables para el texto
        # self.font = pygame.font.Font(None, 32)
        self.font = settings.FONTS["medium"]
        self.font2 = settings.FONTS["medium"]
        self.current_text = ""
        self.full_text = ""
        self.text_speed = 0.05
        self.text_timer = 0
        self.current_paragraph = 0
        self.waiting_for_input = False
        
        self.wrapped_lines = []
        self.current_line = 0
        
        # Margen de 50px a cada lado
        self.max_width = settings.WINDOW_WIDTH - 100  

        # Parrafos de la historia
        self.story_paragraphs = [
            "En un reino olvidado por el tiempo, donde las sombras danzan entre las ruinas de un imperio caído, una antigua profecía resuena en los vientos...",
            "El Rey Oscuro, una vez guardián de la luz, sucumbió a la corrupción de un artefacto maldito. Su reino, antes próspero, se convirtió en un laberinto de pesadillas y criaturas abominables.",
            "Pero aún hay esperanza. Una antigua leyenda habla de un guerrero elegido, capaz de restaurar el equilibrio y liberar al reino de su eterna oscuridad.",
            "Tú eres ese guerrero. Armado con tu espada y tu determinación, debes atravesar las tierras malditas, enfrentarte a las criaturas de la noche y encontrar el artefacto que corrompió al rey.",
            "El destino del Reino Perdido está en tus manos. ¿Estás listo para enfrentar la oscuridad y reclamar la luz?"
        ]

    def wrap_text(self, text):
        # Ajustar el ancho de las lineas
        return textwrap.wrap(text, width=60) 

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
                self.state_machine.change("play")

        # Actualizar el texto si no estamos esperando input
        if not self.waiting_for_input:
            self.text_timer += dt
            if self.text_timer >= self.text_speed:
                self.text_timer = 0
                if len(self.current_text) < len(self.full_text):
                    self.current_text = self.full_text[:len(self.current_text) + 1]
                    # Actualizar las llineas neas envueltas cada vez que cambia el texto
                    self.wrapped_lines = self.wrap_text(self.current_text)
                else:
                    self.waiting_for_input = True

    def render(self, surface):
      
        # surface.fill((0, 0, 0))
        surface.blit(settings.TEXTURES["intro2"], (0, 0))     
        # Renderizar el texto actual en multiples lineas
        if self.current_paragraph < len(self.story_paragraphs):
            y_position = (surface.get_height() // 2)-100 - (len(self.wrapped_lines) * 20)  
            for line in self.wrapped_lines:
                text = self.font.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(surface.get_width() // 2, y_position))
                surface.blit(text, text_rect)
                # Espaciado entre lineas
                y_position += 25  

            # Mostrar indicador de "Presiona ENTER" cuando se completa el texo o pueda skipear
            if self.waiting_for_input:
                settings.SOUNDS["maquinaescribir"].stop()
                continue_text = self.font2.render("Presiona ENTER para continuar o 'X' para saltar Intro.......", True, (200, 200, 200))
                continue_rect = continue_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 238))
                surface.blit(continue_text, continue_rect)

        # Aplicar el fade in o fade out
        if self.fade_in or self.fade_out:
            self.fade_surface.set_alpha(self.fade_alpha)
            surface.blit(self.fade_surface, (0, 0))

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            if self.waiting_for_input:
        
                settings.SOUNDS["maquinaescribir"].stop()
                settings.SOUNDS["maquinaescribir"].play(loops=-1)
                
                self.current_paragraph += 1
                if self.current_paragraph < len(self.story_paragraphs):
                    self.full_text = self.story_paragraphs[self.current_paragraph]
                    self.current_text = ""
                    self.wrapped_lines = []
                    self.waiting_for_input = False
                else:
                    # Detener el sonido cuando termina la intro
                    settings.SOUNDS["maquinaescribir"].stop()
                    self.fade_out = True
                    self.fade_alpha = 0

        # Permitir saltar la intro con la tecla x
        if input_id == "x" and input_data.pressed:
            # Detener el sonido si se salta la intro
            settings.SOUNDS["maquinaescribir"].stop()
            self.fade_out = True
            self.fade_alpha = 0