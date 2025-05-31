import pygame

class QuadTree:
    def __init__(self, boundary_rect, max_objects=4, max_depth=4, depth=0, parent=None):
        
        # pygame.Rect que define los limites de analisis del nodo
        self.boundary = boundary_rect
        self.max_objects = max_objects 
        
        # Profundidad máxima del arbol
        self.max_depth = max_depth  
        # Profundidad actual de este nodo   
        self.depth = depth            

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
                # Si el subnodo contiene completamente al objeto
                if node.boundary.contains(obj_data['rect']): 
                    # El objeto se mueve a un subnodo
                    node.insert_data(obj_data)
                    moved = True
                    break 
             # Si no cabe completamente en ningun subnodo, se queda en este nodo (por ejemplo apra objetos grandes o en bordes)
            if not moved:
                objects_to_stay.append(obj_data)
        self.objects = objects_to_stay

    # recordar que obj_data es {'rect': rect, 'type': type_str, 'obj_ref': original_object}
    def insert_data(self, obj_data): 
        # Si este nodo tiene subnodos, intentar insertar en ellos
        if self.nodes:
            for node in self.nodes:
                if node.boundary.contains(obj_data['rect']):
                    # Insertado en un hijo
                    node.insert_data(obj_data)
                    return True 
            # Si no cabe en ningun hijo, se queda en este nodo 
        
        self.objects.append(obj_data)

        # Si se excede la capacidad y no se ha alcanzado la profundidad máxima, subdividir
        if len(self.objects) > self.max_objects and self.depth < self.max_depth:
             # Subdividir solo una vez
            if not self.nodes:
                self.subdivide()
        return True

    def insert(self, rect_obj, type_str, original_object_ref=None):
        # Solo insertar si el objeto está dentro de los límites de este nodo
        if not self.boundary.colliderect(rect_obj):
            # El objeto está fuera de los limites de este nodo raiz
            return False
        
        obj_data = {'rect': rect_obj, 'type': type_str, 'obj_ref': original_object_ref}
        return self.insert_data(obj_data)


    def query(self, query_rect):
        # Devuelve una lista de objetos que podrían colisionar con query_rect.
        found_objects = []

        # Si query_rect no intersecta los limites de este nodo no buscar mas 
        if not self.boundary.colliderect(query_rect):
            return found_objects

        # A;adir objetos de este nodo si intersectan
        for obj_data in self.objects:
            if query_rect.colliderect(obj_data['rect']):
                found_objects.append(obj_data)

        # Si hay subnodos, consultar recursivamente
        if self.nodes:
            for node in self.nodes:
                found_objects.extend(node.query(query_rect))
                
        return found_objects

    def clear(self):
        # Limpia el Quadtree para la siguiente actualización
        self.objects = []
        for node in self.nodes:
            node.clear()
        self.nodes = [] # resetear los nodos hijos

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0, color=(255,255,255)):
        bounds_on_screen = self.boundary.move(-camera_offset_x, -camera_offset_y)
        pygame.draw.rect(surface, color, bounds_on_screen, 1)
        if self.nodes:
            for node in self.nodes:
                # Color más oscuro para hijos
                node.draw(surface, camera_offset_x, camera_offset_y, (100,100,100)) 