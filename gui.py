import pygame
from reti_logiche import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Logic Gates Visualizer")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTBLUE = (173, 216, 230)
WHITE = (255, 255, 255)

class VisualConnection:
    def __init__(self, start_port: "VisualPort", end_port: "VisualPort", pin_index: int = 1):
        self.start_port:"VisualPort" = start_port
        self.end_port:"VisualPort" = end_port
        #start_port only output pin
        self.start_x = start_port.x + start_port.width
        self.start_y = start_port.y + start_port.height//2
        
        self.end_x = end_port.x
        if isinstance(end_port.port, (AND, OR, NAND, NOR)):
            self.end_y = end_port.y + end_port.height//3 if pin_index == 1 else end_port.y + 2*end_port.height//3
        else:
            self.end_y = end_port.y + end_port.height//2
    
    def draw(self, screen):
        color = BLACK
        if(self.start_port.get_result()):
            color = RED
            
        pygame.draw.line(screen, color, (self.start_x, self.start_y), (self.end_x, self.end_y), 2)


class VisualPort:
    def __init__(self, port: Port, x: int, y: int):
        self.visual_connections:list[VisualConnection] = []
        self.port = port
        self.x = x
        self.y = y
        self.width = 100
        self.height = 60
        self.pin_radius = 5
    
    def get_result(self):
        return self.port.result

    def draw(self, screen):
        # Draw port body
        pygame.draw.rect(screen, LIGHTBLUE, (self.x, self.y, self.width, self.height))
        
        # Draw port name
        font = pygame.font.Font(None, 24)
        text = font.render(self.port.__class__.__name__, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, text_rect)

        # Draw output pin
        pin_color = RED if self.port.result else BLACK
        pygame.draw.circle(screen, pin_color, 
                         (self.x + self.width, self.y + self.height//2), 
                         self.pin_radius)

        # Draw input pins
        if isinstance(self.port, (AND, OR, NAND, NOR)):
            pin1_color = RED if self.port.pin_1 else BLACK
            pin2_color = RED if self.port.pin_2 else BLACK
            
            # Input pin 1
            pygame.draw.circle(screen, pin1_color, 
                             (self.x, self.y + self.height//3), 
                             self.pin_radius)
            # Input pin 2
            pygame.draw.circle(screen, pin2_color, 
                             (self.x, self.y + 2*self.height//3), 
                             self.pin_radius)
        
        elif isinstance(self.port, NOT):
            pin_color = RED if self.port.pin else BLACK
            pygame.draw.circle(screen, pin_color, 
                             (self.x, self.y + self.height//2), 
                             self.pin_radius)
            
        # Draw connections
        for connection in self.visual_connections:
            connection.draw(screen)
            
        
    def add_connection(self, end_port: "VisualPort", pin_index: int = 1):
        connection = VisualConnection(self, end_port, pin_index)
        self.visual_connections.append(connection)



'''
PROB NON SERVE A NIENTE
parti dall'ultimo nodo dello stack, crei la sua classe visual
crei la classe visual per le porte padre e le connetti
riparti dal padre e ripeti
'''
def ordinamento_topologico_helper(port: Port, stack: list[Port], visited: set[Port]):
    visited.add(port)
    for child_port in port.output_to_ports:
        if child_port not in visited:
            ordinamento_topologico_helper(child_port, stack, visited)
    stack.append(port)

def ordinamento_topologico(lista_porte: list[Port]):
    stack:list[Port] = []
    visited:set[Port] = set()

    for port in lista_porte:
        if port not in visited:
            ordinamento_topologico_helper(port, stack, visited)
    return stack



def create_visual_ports(lista_porte: list[Port]):
    lista_porte_ordinata:list[Port] = ordinamento_topologico(lista_porte)
    lista_porte_ordinata.reverse()
    #print("lista_porte_ordinata: ", lista_porte_ordinata)
    visual_ports = []
    x, y = -100, 50
    dict_logic_to_visual_ports:dict[Port, VisualPort] = {}

    previus_port_level:int = -1
    for child_port in lista_porte_ordinata:
        if dict_port_to_BFS_level[child_port] == previus_port_level:
            print(child_port, previus_port_level)
            y += 100
        else:
            y = 50
            x += 150
            previus_port_level = dict_port_to_BFS_level[child_port]
            
        #print("child_port: ", child_port, " level: ", dict_port_to_BFS_level[child_port])
        visual_child_Port = VisualPort(child_port, x, y)
        dict_logic_to_visual_ports[child_port] = visual_child_Port
        visual_ports.append(visual_child_Port)

        if not isinstance(child_port, (PortTrue, PortFalse)):
            pin_1_Port = child_port.pin_1_Port
            visual_pin_1_Port = dict_logic_to_visual_ports.get(pin_1_Port)
            visual_pin_1_Port.add_connection(visual_child_Port, 1)

            if isinstance(child_port, (AND, OR, NAND, NOR)):
                pin_2_Port = child_port.pin_2_Port
                visual_pin_2_Port = dict_logic_to_visual_ports.get(pin_2_Port)
                visual_pin_2_Port.add_connection(visual_child_Port, 2)

    return visual_ports
        


visual_ports:list[VisualPort] = create_visual_ports(all_ports_list)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)
    
    # Draw all ports
    for visual_port in visual_ports:
        visual_port.draw(screen)
    
    pygame.display.flip()

pygame.quit()
