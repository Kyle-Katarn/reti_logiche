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
    def __init__(self, start_gate: "VisualGate", end_gate: "VisualGate", pin_index: int = 1):
        self.start_gate: "VisualGate" = start_gate
        self.end_gate: "VisualGate" = end_gate
        #start_gate only output pin
        self.start_x = start_gate.x + start_gate.width
        self.start_y = start_gate.y + start_gate.height//2
        
        self.end_x = end_gate.x
        if isinstance(end_gate.gate, (AND, OR, NAND, NOR)):
            self.end_y = end_gate.y + end_gate.height//3 if pin_index == 1 else end_gate.y + 2*end_gate.height//3
        else:
            self.end_y = end_gate.y + end_gate.height//2
    
    def draw(self, screen):
        color = BLACK
        if(self.start_gate.gate.get_output_signal_status()):
            color = RED
            
        pygame.draw.line(screen, color, (self.start_x, self.start_y), (self.end_x, self.end_y), 2)


class VisualGate:
    def __init__(self, gate: BasicGate, x: int, y: int):
        self.visual_connections: list[VisualConnection] = []
        self.gate = gate
        self.x = x
        self.y = y
        self.width = 100
        # Height based on max between inputs and outputs
        max_pins = max(gate.number_of_inputs, gate.number_of_outputs)
        self.height = max(60, max_pins * 30)
        self.pin_radius = 5

    def draw(self, screen):
        # Draw gate body
        pygame.draw.rect(screen, LIGHTBLUE, (self.x, self.y, self.width, self.height))
        
        # Draw gate name
        font = pygame.font.Font(None, 24)
        text = font.render(self.gate.name, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, text_rect)

        # Draw input pins
        if self.gate.number_of_inputs > 0:
            spacing = self.height // (self.gate.number_of_inputs + 1)
            for i in range(self.gate.number_of_inputs):
                pin_color = RED if self.gate.get_input_signal_status(i) else BLACK
                y_pos = self.y + spacing * (i + 1)
                pygame.draw.circle(screen, pin_color, (self.x, y_pos), self.pin_radius)

        # Draw output pins
        spacing = self.height // (self.gate.number_of_outputs + 1)
        for i in range(self.gate.number_of_outputs):
            pin_color = RED if self.gate.get_output_signal_status(i) else BLACK
            y_pos = self.y + spacing * (i + 1)
            pygame.draw.circle(screen, pin_color, 
                    (self.x + self.width, y_pos), 
                    self.pin_radius)
            
        # Draw connections
        for connection in self.visual_connections:
            connection.draw(screen)
            
        
    def add_connection(self, end_gate: "VisualGate", pin_index: int = 1):
        connection = VisualConnection(self, end_gate, pin_index)
        self.visual_connections.append(connection)




def ordinamento_topologico_helper(gate: AbstractGate, stack: list[AbstractGate], visited: set[AbstractGate]):
    visited.add(gate)
    for child_gate in gate.output_to_gates:
        if child_gate not in visited:
            ordinamento_topologico_helper(child_gate, stack, visited)
    stack.append(gate)

def ordinamento_topologico(lista_gate: list[Gate]):
    stack:list[Gate] = []
    visited:set[Gate] = set()

    for gate in lista_gate:
        if gate not in visited:
            ordinamento_topologico_helper(gate, stack, visited)
    return stack


def get_gates_level_BFS():
    gates_to_execute:list[Gate] = []
    gates_to_execute.append(GLOBAL_TRUE)
    gates_to_execute.append(GLOBAL_FALSE)
    number_of_gates_in_level:int = len(gates_to_execute)
    level:int = 0

    while(not len(gates_to_execute) == 0):
        current_gate:Gate = gates_to_execute.pop(0)
        dict_gate_to_BFS_level[current_gate] = level
        number_of_gates_in_level -= 1

        if number_of_gates_in_level == 0:
            level += 1


def create_visual_gates(lista_gate: list[Gate]):
    lista_gate_ordinata:list[Gate] = ordinamento_topologico(lista_gate)
    lista_gate_ordinata.reverse()
    #print("lista_gate_ordinata: ", lista_gate_ordinata)
    visual_gates = []
    x, y = -100, 50
    dict_logic_to_visual_gates:dict[Gate, VisualGate] = {}

    previous_gate_level:int = -1
    for child_gate in lista_gate_ordinata:
        if dict_gate_to_BFS_level[child_gate] == previous_gate_level:
            print(child_gate, previous_gate_level)
            y += 100
        else:
            y = 50
            x += 150
            previous_gate_level = dict_gate_to_BFS_level[child_gate]
            
        #print("child_gate: ", child_gate, " level: ", dict_gate_to_BFS_level[child_gate])
        visual_child_gate = VisualGate(child_gate, x, y)
        dict_logic_to_visual_gates[child_gate] = visual_child_gate
        visual_gates.append(visual_child_gate)

        if not isinstance(child_gate, (PortTrue, PortFalse)):
            pin_1_Port = child_gate.pin_1_Port
            visual_pin_1_Port = dict_logic_to_visual_gates.get(pin_1_Port)
            visual_pin_1_Port.add_connection(visual_child_gate, 1)

            if isinstance(child_gate, (AND, OR, NAND, NOR)):
                pin_2_Port = child_gate.pin_2_Port
                visual_pin_2_Port = dict_logic_to_visual_gates.get(pin_2_Port)
                visual_pin_2_Port.add_connection(visual_child_gate, 2)

    return visual_gates
        




visual_gates:list[VisualGate] = create_visual_gates(all_gates_list)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)
    
    # Draw all gates
    for visual_gate in visual_gates:
        visual_gate.draw(screen)
    
    pygame.display.flip()

pygame.quit()
