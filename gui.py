import pygame
from reti_logiche import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Logic Gates Visualizer")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTBLUE = "#97dff7"
WHITE = (255, 255, 255)
GREEN = "#219e02"

class VisualConnection:
    def __init__(self, start_port: "VisualPort", end_port: "VisualPort", pin_index: int = 1):
        self.start_port:"VisualPort" = start_port
        self.end_port:"VisualPort" = end_port
        self.pin_index = pin_index
    
    def draw(self, screen):
        self.start_x = self.start_port.x + self.start_port.width
        self.start_y = self.start_port.y + self.start_port.height//2
        
        self.end_x = self.end_port.x
        space_in_between_height = self.end_port.height // (self.end_port.port.get_number_of_inputs()+1)
        self.end_y = self.end_port.y + space_in_between_height * self.pin_index
        color = BLACK
        if(self.start_port.get_result()):
            color = RED
            
        pygame.draw.line(screen, color, (self.start_x, self.start_y), (self.end_x, self.end_y), 2)


class VisualPort:
    def __init__(self, port: BasicPort, x: int, y: int):
        self.visual_connections:list[VisualConnection] = []
        self.port = port
        self.x = x
        self.y = y
        self.width = 100
        self.height = max(60, self.port.get_number_of_inputs() * 30)  # Changed to use number_of_inputs
        self.pin_radius = 5
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
    
    def get_result(self):
        return self.port.result
    
    def get_logic_port(self):
        return self.port

    def draw(self, screen):
        # Draw port body
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        
        # Draw port name
        font = pygame.font.Font(None, 24)
        text = font.render(self.port.name, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, text_rect)

        # Draw output pin
        pin_color = RED if self.port.result else BLACK
        pygame.draw.circle(screen, pin_color, 
                         (self.x + self.width, self.y + self.height//2), 
                         self.pin_radius)

        # Draw input pins
        num_inputs = self.port.get_number_of_inputs()  # Changed to use number_of_inputs
        if num_inputs > 0:
            spacing = self.height // (num_inputs + 1)
            for i in range(num_inputs):  # Changed to use range(num_inputs)
                pin_color = RED if self.port.input_signals_list[i] else BLACK
                y_pos = self.y + spacing * (i + 1)
                pygame.draw.circle(screen, pin_color, 
                                 (self.x, y_pos), 
                                 self.pin_radius)
            
        # Draw connections
        for connection in self.visual_connections:
            connection.draw(screen)
        
    def add_connection(self, end_port: "VisualPort", pin_index: int = 1):
        connection = VisualConnection(self, end_port, pin_index)
        self.visual_connections.append(connection)

    def contains_point(self, x: int, y: int) -> bool:
        """Check if point (x,y) is inside the port rectangle"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)

    def start_drag(self, mouse_x: int, mouse_y: int):
        """Start dragging, calculate offset from port top-left corner"""
        self.dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y

    def end_drag(self):
        """Stop dragging"""
        self.dragging = False

    def update_position(self, mouse_x: int, mouse_y: int):
        """Update position while dragging"""
        if self.dragging:
            self.x = mouse_x - self.drag_offset_x
            self.y = mouse_y - self.drag_offset_y


#*ordinmento topologico
def ordinamento_topologico_helper(port: BasicPort, stack: list[BasicPort], visited: set[BasicPort]):
    visited.add(port)
    for child_port in port.child_ports_list:
        if child_port not in visited:
            ordinamento_topologico_helper(child_port, stack, visited)
    stack.append(port)

def ordinamento_topologico(lista_porte: list[BasicPort]):
    stack:list[BasicPort] = []
    visited:set[BasicPort] = set()

    for port in lista_porte:
        if port not in visited:
            ordinamento_topologico_helper(port, stack, visited)
    return stack


#*PORT TO BFS LEVEL
def get_ports_level_BFS(lista_porte: list[BasicPort]):
    dict_port_to_BFS_level: Dict[BasicPort, int] = {}
    start_ports = [GlOBAL_TRUE, GlOBAL_FALSE]
    get_ports_level_BFS_helper(lista_porte, start_ports, dict_port_to_BFS_level)

    unconnected_ports:list[BasicPort] = []
    for port in lista_porte:
        if port not in dict_port_to_BFS_level:
            unconnected_ports.append(port)
    get_ports_level_BFS_helper(lista_porte, unconnected_ports, dict_port_to_BFS_level)
    return dict_port_to_BFS_level


def get_ports_level_BFS_helper(lista_porte: list[BasicPort], start_ports: list[BasicPort], dict_port_to_BFS_level: dict[BasicPort, int]):
    current_level_ports = set()
    next_level_ports = set()
    current_level_ports.update(start_ports)
    level = 0
    
    # Initialize first level
    for port in current_level_ports:
        dict_port_to_BFS_level[port] = level

    while len(current_level_ports) > 0:
        current_port:"BasicPort" = current_level_ports.pop()
        current_port_adjacent_ports = current_port.get_child_ports_list()
        for port in current_port_adjacent_ports:
            if port in lista_porte:
                next_level_ports.add(port)

        if len(current_level_ports) == 0:
            level += 1
            # Set level for all ports in next_level
            for port in next_level_ports:
                dict_port_to_BFS_level[port] = level
            current_level_ports = next_level_ports.copy()
            next_level_ports.clear()
    



def create_visual_ports(lista_porte: list[BasicPort], dict_port_to_BFS_level: dict[BasicPort, int]):
    lista_porte_ordinata = ordinamento_topologico(lista_porte)
    lista_porte_ordinata.reverse()
    visual_ports = []
    x, y = -100, 50
    dict_y_per_level = {}
    dict_logic_to_visual_ports = {}

    for child_port in lista_porte_ordinata:
        #print(child_port)
        level = dict_port_to_BFS_level[child_port]
        if level in dict_y_per_level:
            y = dict_y_per_level[level] + 100
        else:
            y = 50
            x += 150
        
        dict_y_per_level[level] = y
        visual_child_Port = VisualPort(child_port, x, y)
        dict_logic_to_visual_ports[child_port] = visual_child_Port
        visual_ports.append(visual_child_Port)

        # Create connections for all input ports
        if not isinstance(child_port, (PortTrue, PortFalse)):
            for i, input_port in enumerate(child_port.input_ports_list):
                visual_input_port:VisualPort = dict_logic_to_visual_ports[input_port]
                visual_input_port.add_connection(visual_child_Port, i + 1)

    return visual_ports
        



dict_port_to_BFS_level:dict[BasicPort, int] = get_ports_level_BFS(GLOBAL_ALL_PORTS_LIST)
lista_ordinata:list[BasicPort] = ordinamento_topologico(GLOBAL_ALL_PORTS_LIST)
visual_ports:list[VisualPort] = create_visual_ports(lista_ordinata, dict_port_to_BFS_level)

# Main game loop
running = True
selected_port = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for port in visual_ports:
                if port.contains_point(mouse_x, mouse_y):
                    port.start_drag(mouse_x, mouse_y)
                    selected_port = port
                    break
        
        # Handle mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_port:
                selected_port.end_drag()
                selected_port = None
        
        # Handle mouse motion
        elif event.type == pygame.MOUSEMOTION:
            if selected_port:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_port.update_position(mouse_x, mouse_y)
    
    screen.fill(LIGHTBLUE)
    
    # Draw all ports
    for visual_port in visual_ports:
        visual_port.draw(screen)
    
    pygame.display.flip()

pygame.quit()
