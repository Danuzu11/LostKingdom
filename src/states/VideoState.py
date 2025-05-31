import pygame
from gale.state import BaseState
from moviepy import VideoFileClip 

import tempfile  # Para manejar archivos temporales

class VideoState(BaseState):
    def enter(self, **params: dict):
        """
        Se ejecuta al entrar en el estado.
        """
        self.video_path = "assets/video/intro2Compresed.mp4"  # Ruta del video
        self.video = VideoFileClip(self.video_path)
  
        # Convertir el video en frames para reproducirlo en pygame
        self.video_frames = self.video.iter_frames( dtype="uint8")
        self.video_surface = None
        self.video_finished = False
        
        # Extraer el audio del video
        audio = self.video.audio
        audio.write_audiofile("temp_audio.mp3")  
        pygame.mixer.music.load("temp_audio.mp3")
        pygame.mixer.music.play(-1)
        
    def update(self, dt: float):
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

# import pygame
# from gale.state import BaseState
# from moviepy import VideoFileClip
# import tempfile
# import os

# class VideoState(BaseState):
#     def enter(self, **params: dict):
#         """Se ejecuta al entrar en el estado."""
#         self.video_path = "assets/video/intro2Compresed.mp4"
        
#         # Precargar todo el video en memoria como superficies de Pygame
#         self.frames = []
#         self.current_frame = 0
#         self.video_finished = False
        
#         # Cargar el video
#         clip = VideoFileClip(self.video_path)
#         fps = clip.fps
        
#         # Precargar todos los frames
#         for frame in clip.iter_frames(dtype="uint8"):
#             # Convertir a superficie pygame una sola vez
#             pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
#             self.frames.append(pygame_frame)
        
#         # Configurar el audio
#         audio_path = os.path.join(tempfile.gettempdir(), "temp_audio.mp3")
#         clip.audio.write_audiofile(audio_path)
#         pygame.mixer.music.load(audio_path)
#         pygame.mixer.music.play()
        
#         # Calcular duración por frame en milisegundos
#         self.frame_duration = 1000 / fps
#         self.last_frame_time = pygame.time.get_ticks()
        
#         clip.close()

#     def update(self, dt: float):
#         if not self.video_finished and len(self.frames) > 0:
#             current_time = pygame.time.get_ticks()
            
#             # Avanzar frame solo si ha pasado el tiempo suficiente
#             if current_time - self.last_frame_time >= self.frame_duration:
#                 self.current_frame += 1
#                 self.last_frame_time = current_time
                
#                 if self.current_frame >= len(self.frames):
#                     self.video_finished = True
#                     pygame.mixer.music.stop()
#                     self.state_machine.change("menu")

#     def render(self, surface):
#         if not self.video_finished and self.current_frame < len(self.frames):
#             frame = self.frames[self.current_frame]
#             scaled_frame = pygame.transform.scale(frame, surface.get_size())
#             surface.blit(scaled_frame, (0, 0))

#     def exit(self):
#         pygame.mixer.music.stop()
#         # Limpiar archivo temporal de audio
#         try:
#             os.remove(os.path.join(tempfile.gettempdir(), "temp_audio.mp3"))
#         except:
#             pass