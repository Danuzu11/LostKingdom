import pytmx
import pygame
import settings

# Aqui se define la clase TileMap, que se encarga de cargar y renderizar un mapa de tiles (el de TILE)
# utilizando la libreria pytmx. La clase tiene un constructor que recibe el nombre del nivel y
# carga el mapa correspondiente. El metodo render se encarga de dibujar los tiles en la pantalla
# y el metodo make_map crea una superficie escalada del mapa de tiles para ajustarse a la pantalla virtual.

class TileMap:
    def __init__(self, levelMap):
        # Cargamos el mapa segun le mandemos por parametro
        self.map = settings.LEVELS[levelMap]
        # Configuramos su ancho y alto TOTAL (EL TAMA;O DEL MAPA TOTAL CREADO EN TILE)
        self.width = self.map.width * self.map.tilewidth
        self.height = self.map.height * self.map.tileheight
        # Esta variable es par toquetiar la configuraciones del mapa porque es un tipo de dato especifico de pytmx
        self.tmx_data = self.map

    def render(self, surface):
        # Sacamos la data del tilemap
        tile_map = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            # print(layer.name)
            # Mera comprobacion para saber si es una capa del tilemap
            if isinstance(layer, pytmx.TiledTileLayer)  and layer.name != "MaskPrincipal":
                # Si es una capa de tilemap, la recorremos y dibujamos los tiles en la superficie
                # gid es el id del tile, x e y son las coordenadas en la capa
                for x, y, gid in layer:
                    tile = tile_map(gid)
                    if tile:
                        # Si el tile existe, lo dibujamos en la superficie
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                            y * self.tmx_data.tileheight))
                 
    # Metodo para crear el Mapa
    def make_map(self):
        # Crear una superficie temporal con las dimensiones originales del tilemap
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        
        # Altura maxima de tiles que quieres mostrar sin escalar (por ejemplo, 70 tiles)
        max_tile_height = 10
        max_pixel_height = max_tile_height * self.tmx_data.tileheight

        # Si el mapa es mas pequeño que el maximo, lo escalamos para que ocupe la pantalla
        if self.height <= max_pixel_height:
            scale_factor = settings.VIRTUAL_HEIGHT / self.height
            scaled_width = int(self.width * scale_factor)
            scaled_height = int(self.height * scale_factor)
            scaled_surface = pygame.transform.smoothscale(temp_surface, (scaled_width, scaled_height))
            return scaled_surface
        else:
            return temp_surface  
         

    # MASCARAS
    def render_mask(self, surface, camera_offset=None):
   
        # Renderiza el layer "MaskPrincipal" con soporte para offset de camara y escalado.
   
        tile_map = self.tmx_data.get_tile_image_by_gid
        scale_factor = settings.VIRTUAL_HEIGHT / self.height  # Calcular el factor de escala

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "MaskPrincipal":
                for x, y, gid in layer:
                    tile = tile_map(gid)
                    if tile:
                        # Escalar el tile
                        scaled_tile = pygame.transform.scale(
                            tile,
                            (
                                int(tile.get_width() * scale_factor),
                                int(tile.get_height() * scale_factor),
                            ),
                        )

                        # Calcular la posicion del tile considerando el offset de la cámara
                        tile_x = x * self.tmx_data.tilewidth * scale_factor
                        tile_y = y * self.tmx_data.tileheight * scale_factor

                        if camera_offset:
                            tile_x -= camera_offset[0]
                            tile_y -= camera_offset[1]

                        # Dibujar el tile escalado
                        surface.blit(scaled_tile, (tile_x, tile_y))
                        
    def make_mask(self):
        # Crear una superficie temporal con las dimensiones originales del tilemap
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render_mask(temp_surface)  # Cambiado de render a render_mask
        
        # Calcular el factor de escala para ajustar el tilemap al alto virtual de la pantalla
        scale_factor = settings.VIRTUAL_HEIGHT / self.height
        scaled_width = int(self.width * scale_factor)
        scaled_height = int(self.height * scale_factor)
        scaled_surface = pygame.transform.smoothscale(temp_surface, (scaled_width, scaled_height))

        return scaled_surface
