import pygame

class QuadTree:
    def __init__(self, boundary_rect, max_objects=4, max_depth=4, depth=0, parent=None):
        self.boundary = boundary_rect # pygame.Rect que define los límites de este nodo
        self.max_objects = max_objects # Número máximo de objetos antes de subdividir
        self.max_depth = max_depth     # Profundidad máxima del árbol
        self.depth = depth             # Profundidad actual de este nodo

        self.objects = []      # Lista para almacenar {'rect': pygame.Rect, 'type': str, 'obj_ref': obj}
        self.nodes = []        # Hijos de este nodo (otros QuadTrees)
        self.parent = parent   # Referencia al nodo padre

    def subdivide(self):
        # Crea 4 subnodos
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height
        hw, hh = w / 2, h / 2

        # nw (noroeste), ne (noreste), sw (suroeste), se (sureste)
        nw = pygame.Rect(x, y, hw, hh)
        ne = pygame.Rect(x + hw, y, hw, hh)
        sw = pygame.Rect(x, y + hh, hw, hh)
        se = pygame.Rect(x + hw, y + hh, hw, hh)

        self.nodes.append(QuadTree(nw, self.max_objects, self.max_depth, self.depth + 1, self))
        self.nodes.append(QuadTree(ne, self.max_objects, self.max_depth, self.depth + 1, self))
        self.nodes.append(QuadTree(sw, self.max_objects, self.max_depth, self.depth + 1, self))
        self.nodes.append(QuadTree(se, self.max_objects, self.max_depth, self.depth + 1, self))

        # Mover objetos de este nodo a los subnodos si es posible
        objects_to_stay = []
        for obj_data in self.objects:
            moved = False
            for node in self.nodes:
                if node.boundary.contains(obj_data['rect']): # Si el subnodo contiene completamente al objeto
                    node.insert_data(obj_data)
                    moved = True
                    break # El objeto se movió a un subnodo
            if not moved: # Si no cabe completamente en ningún subnodo, se queda en este nodo (objetos grandes o en bordes)
                objects_to_stay.append(obj_data)
        self.objects = objects_to_stay


    def insert_data(self, obj_data): # obj_data es {'rect': rect, 'type': type_str, 'obj_ref': original_object}
        # Si este nodo tiene subnodos, intentar insertar en ellos
        if self.nodes:
            for node in self.nodes:
                if node.boundary.contains(obj_data['rect']):
                    node.insert_data(obj_data)
                    return True # Insertado en un hijo
            # Si no cabe en ningún hijo, se queda en este nodo (grande o en bordes)
        
        self.objects.append(obj_data)

        # Si se excede la capacidad y no se ha alcanzado la profundidad máxima, subdividir
        if len(self.objects) > self.max_objects and self.depth < self.max_depth:
            if not self.nodes: # Subdividir solo una vez
                self.subdivide()
        return True

    def insert(self, rect_obj, type_str, original_object_ref=None):
        """Inserta un objeto (pygame.Rect) en el Quadtree."""
        # Solo insertar si el objeto está dentro de los límites de este nodo
        if not self.boundary.colliderect(rect_obj):
            return False # El objeto está fuera de los límites de este nodo raíz
        
        obj_data = {'rect': rect_obj, 'type': type_str, 'obj_ref': original_object_ref}
        return self.insert_data(obj_data)


    def query(self, query_rect):
        """Devuelve una lista de objetos que podrían colisionar con query_rect."""
        found_objects = []

        # Si query_rect no intersecta los límites de este nodo, no buscar más
        if not self.boundary.colliderect(query_rect):
            return found_objects

        # Añadir objetos de este nodo si intersectan
        for obj_data in self.objects:
            if query_rect.colliderect(obj_data['rect']):
                found_objects.append(obj_data)

        # Si hay subnodos, consultar recursivamente
        if self.nodes:
            for node in self.nodes:
                found_objects.extend(node.query(query_rect))
        
        # Eliminar duplicados si un objeto está en varios nodos de la consulta (no debería pasar con 'contains')
        # Sin embargo, si un objeto está en un nodo padre y también es recogido por una consulta a un hijo,
        # podría haber duplicados si la lógica de inserción lo permite.
        # La forma más robusta es usar un set de IDs de objeto si los tienes, o confiar en la estructura.
        # Para simplificar, no se manejan duplicados aquí asumiendo que la inserción es correcta.
        return found_objects

    def clear(self):
        """Limpia el Quadtree para la siguiente actualización (reconstrucción)."""
        self.objects = []
        for node in self.nodes:
            node.clear()
        self.nodes = [] # Importante resetear los nodos hijos

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0, color=(255,255,255)):
        """Dibuja los límites del Quadtree para debug."""
        bounds_on_screen = self.boundary.move(-camera_offset_x, -camera_offset_y)
        pygame.draw.rect(surface, color, bounds_on_screen, 1)
        if self.nodes:
            for node in self.nodes:
                node.draw(surface, camera_offset_x, camera_offset_y, (100,100,100)) # Color más oscuro para hijos