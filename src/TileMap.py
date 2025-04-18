import pytmx
import pygame
import settings

class TileMap:
    def __init__(self, levelMap):
        self.map = settings.LEVELS[levelMap]
        self.width = self.map.width * self.map.tilewidth
        self.height = self.map.height * self.map.tileheight
        self.tmx_data = self.map

    def render(self, surface):
        tile_map = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tile_map(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                            y * self.tmx_data.tileheight))

    def make_map(self):
        # Crear una superficie temporal con las dimensiones originales del tilemap
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        
        # Calcular el factor de escala para ajustar el tilemap al alto virtual de la pantalla
        scale_factor = settings.VIRTUAL_HEIGHT / self.height

        # Escalar el tilemap
        scaled_width = int(self.width * scale_factor)
        scaled_height = int(self.height * scale_factor)
        scaled_surface = pygame.transform.smoothscale(temp_surface, (scaled_width, scaled_height))

        return scaled_surface