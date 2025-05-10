import pygame
from gale.state import BaseState
from moviepy import VideoFileClip 

import tempfile  # Para manejar archivos temporales

class VideoState(BaseState):
    def enter(self, **params: dict):
        """
        Se ejecuta al entrar en el estado.
        """
        self.video_path = "assets/video/intro1.mp4"  # Ruta del video
        self.screen = params.get("screen")
        self.video = VideoFileClip(self.video_path)

        # Convertir el video en frames para reproducirlo en pygame
        self.video_frames = self.video.iter_frames(fps=60, dtype="uint8")
        self.video_surface = None
        self.video_finished = False
        
        # Extraer el audio del video
        audio = self.video.audio
        audio.write_audiofile("temp_audio.mp3")  
        pygame.mixer.music.load("temp_audio.mp3")
        pygame.mixer.music.play(-1)
        
    def update(self, dt: float):
        """
        Actualiza la lógica del estado.
        """
        if not self.video_finished:
            try:
                # Obtener el siguiente frame del video
                frame = next(self.video_frames)
                self.video_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            except StopIteration:
                # El video ha terminado
                self.video_finished = True
                pygame.mixer.music.stop() 
                self.state_machine.change("menu") 

    def render(self, surface):
        if self.video_surface:
            scaled_surface = pygame.transform.scale(self.video_surface, surface.get_size())
            surface.blit(scaled_surface, (0, 0))

    def exit(self):
        self.video.close()