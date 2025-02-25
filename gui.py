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
                pin_color = RED if self.gate.get_input_signal_value(i) else BLACK
                y_pos = self.y + spacing * (i + 1)
                pygame.draw.circle(screen, pin_color, (self.x, y_pos), self.pin_radius)

        # Draw output pins
        spacing = self.height // (self.gate.number_of_outputs + 1)
        for i in range(self.gate.number_of_outputs):
            pin_color = RED if self.gate.get_output_signal_value(i) else BLACK
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




def ordinamento_topologico_helper(gate: LogicClass, stack: list[LogicClass], visited: set[LogicClass]):
    visited.add(gate)
    for child_gate, child_gate_input_ix in gate.get_all_child_gates():
        if child_gate not in visited:
            ordinamento_topologico_helper(child_gate, stack, visited)
    stack.append(gate)

def ordinamento_topologico(lista_gate: list[LogicClass]):
    stack:list[LogicClass] = []
    visited:set[LogicClass] = set()

    for gate, gate_input_ix in lista_gate:
        if gate not in visited:
            ordinamento_topologico_helper(gate, stack, visited)
    return stack

def get_gates_level_BFS(considered_gates:list[LogicClass] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[LogicClass] = GLOBAL_ALL_SWITCHES_LIST):
    dict_gate_to_BFS_level:dict[LogicClass,int] = dict()

    visited_gates_set:set[LogicClass] = set() #x cicli
    starting_gates:list[LogicClass] = []
    starting_gates.extend(considered_switches)
    for g in considered_gates:
        if(len(g.get_all_input_gates()) == 0):
            considered_gates.append(g)
    get_gates_level_BFS_helper(starting_gates,considered_gates,visited_gates_set, dict_gate_to_BFS_level)#se non ci sono cicli basta questo
    starting_gates.clear()

    for gate in considered_gates: #*necessario per A -> B e B -> A
        if gate not in visited_gates_set:
            get_gates_level_BFS_helper([gate],considered_switches,visited_gates_set, dict_gate_to_BFS_level)

    return dict_gate_to_BFS_level

def get_gates_level_BFS_helper(starting_gates:list[LogicClass], considered_gates:list[LogicClass], visited_gates_set:set[LogicClass], dict_gate_to_BFS_level:dict[LogicClass,int]):
    gates_to_execute:list[LogicClass] = []
    gates_to_execute.extend(starting_gates)

    number_of_gates_in_level:int = len(gates_to_execute)
    level:int = 0

    while(not len(gates_to_execute) == 0):
        current_gate:LogicClass = gates_to_execute.pop(0)
        print("@@@@@@current_gate: "+str(current_gate))
        for gate, ix in current_gate.get_all_child_gates():
            print("ponted gate: " +str(gate))
            if (gate not in visited_gates_set) and (gate in considered_gates):
                gates_to_execute.append(gate)
                visited_gates_set.add(gate)
                print("---gates_to_execute: "+str(gates_to_execute))
        dict_gate_to_BFS_level[current_gate] = level
        number_of_gates_in_level -= 1

        if number_of_gates_in_level == 0:
            level += 1
    return dict_gate_to_BFS_level


def create_visual_gates(dict_gate_to_BFS_level:dict[LogicClass, int], lista_gate: list[LogicClass] = GLOBAL_ALL_BASIC_GATES_LIST, lista_switch = GLOBAL_ALL_SWITCHES_LIST):
    #todo 1 -> tutti i gate puntati da 1 -> 2. ->
    
    visual_gates:set[VisualGate] = []
    x, y = -100, 50
    dict_logic_to_visual_gates:dict[LogicClass, VisualGate] = {}
    dict_BFS_level_to_next_y_coo:dict[int, int] = {}

    lista_obj:list[LogicClass] = []
    lista_obj.extend(lista_gate)
    lista_obj.extend(lista_switch)
    for gate in lista_obj:
        child_gate_level:int = dict_gate_to_BFS_level.get(gate)
        #print("gate: "+str(gate)+" |level: "+str(child_gate_level))
        if dict_BFS_level_to_next_y_coo.get(child_gate_level) == None:
            dict_BFS_level_to_next_y_coo[child_gate_level] = 50 #y+=100 y=50 inizio
        # x+=150
        y:int = dict_BFS_level_to_next_y_coo[child_gate_level]
        dict_BFS_level_to_next_y_coo[child_gate_level] += 100
        x:int = child_gate_level*150 +50
            
        #print("gate: ", gate, " level: ", dict_gate_to_BFS_level[gate])
        visual_child_gate = VisualGate(gate, x, y)
        dict_logic_to_visual_gates[gate] = visual_child_gate
        visual_gates.append(visual_child_gate)

        #altro

    return visual_gates
        



gates_to_BFS_levels:dict[LogicClass,int] = get_gates_level_BFS()
print("gates_to_BFS_levels: "+ str(gates_to_BFS_levels))
visual_gates:list[VisualGate] = create_visual_gates(dict_gate_to_BFS_level=gates_to_BFS_levels)

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

