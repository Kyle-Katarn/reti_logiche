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
    def __init__(self, start_gate_tup: tuple["VisualGate",int], end_gate_tip: tuple["VisualGate",int]):
        self.start_gate:VisualGate = start_gate_tup[0]
        self.start_gate_ix:int = start_gate_tup[1]
        self.end_gate: VisualGate = end_gate_tip[0]
        self.end_gate_ix:int = end_gate_tip[1]
        #start_gate output pin coo
        self.start_x = self.start_gate.x + self.start_gate.width
        start_y_segment:int = self.start_gate.height//(self.start_gate.gate.number_of_outputs+1)
        self.start_y = self.start_gate.y + start_y_segment*(self.start_gate_ix+1)
        #end_gate input pin coo
        self.end_x = self.end_gate.x
        end_y_segment:int = self.end_gate.height//(self.end_gate.gate.number_of_inputs+1)
        self.end_y = self.end_gate.y + end_y_segment*(self.end_gate_ix+1)
    
    def draw(self, screen):
        color = BLACK
        if(self.start_gate.gate.get_output_signal_value(self.start_gate_ix)):
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
            
        
    def add_connection(self, end_gate_tup:tuple["VisualGate",int], starting_pin_ix:int):
        connection = VisualConnection((self, starting_pin_ix), end_gate_tup)
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
        print("gate: "+ str(g) + str(g.get_all_input_gates()))
        if(len(g.get_all_input_gates()) == 0):
            considered_gates.append(g)
    get_gates_level_BFS_helper(starting_gates,considered_gates,visited_gates_set, dict_gate_to_BFS_level)#se non ci sono cicli basta questo
    starting_gates.clear()

    for gate in considered_gates: #*necessario per A -> B e B -> A
        if gate not in visited_gates_set:
            visited_gates_set.add(gate)
            get_gates_level_BFS_helper([gate],considered_gates,visited_gates_set, dict_gate_to_BFS_level)

    return dict_gate_to_BFS_level

def get_gates_level_BFS_helper(starting_gates:list[LogicClass], considered_gates:list[LogicClass], visited_gates_set:set[LogicClass], dict_gate_to_BFS_level:dict[LogicClass,int]):
    gates_to_execute:list[LogicClass] = []
    gates_to_execute.extend(starting_gates)

    number_of_gates_in_level:int = len(gates_to_execute)
    level:int = 0

    while(not len(gates_to_execute) == 0):
        current_gate:LogicClass = gates_to_execute.pop(0)
        #print("@@current_gate: " +str(current_gate))
        for gate, ix in current_gate.get_all_child_gates():
            #print("----near_gate: " +str(current_gate))
            #print("--(near_gate not in visited_gates_set): "+str((gate not in visited_gates_set)))
            #print("--(near_gate in considered_gates): "+str((gate in considered_gates)))
            if (gate not in visited_gates_set) and (gate in considered_gates):
                gates_to_execute.append(gate)
                visited_gates_set.add(gate)
        dict_gate_to_BFS_level[current_gate] = level
        number_of_gates_in_level -= 1

        if number_of_gates_in_level == 0:
            level += 1
    return dict_gate_to_BFS_level


def create_visual_gates(dict_gate_to_BFS_level:dict[LogicClass, int], considered_gates: list[LogicClass] = GLOBAL_ALL_BASIC_GATES_LIST, considered_swiches = GLOBAL_ALL_SWITCHES_LIST):
    #todo 1 -> tutti i gate puntati da 1 -> 2. ->
    
    visual_gates:set[VisualGate] = []
    x, y = -100, 50
    dict_logic_to_visual_gates:dict[LogicClass, VisualGate] = {}
    dict_BFS_level_to_next_y_coo:dict[int, int] = {}

    lista_obj:list[LogicClass] = []
    lista_obj.extend(considered_gates)
    lista_obj.extend(considered_swiches)
    for gate in lista_obj:
        child_gate_level:int = dict_gate_to_BFS_level.get(gate)
        #print("gate: "+str(gate)+" |level: "+str(child_gate_level))
        if dict_BFS_level_to_next_y_coo.get(child_gate_level) == None:
            dict_BFS_level_to_next_y_coo[child_gate_level] = 50 #y+=100 y=50 inizio
        # x+=150
        y:int = dict_BFS_level_to_next_y_coo[child_gate_level]
        dict_BFS_level_to_next_y_coo[child_gate_level] += 100
        x:int = child_gate_level*150 +50
            
        visual_child_gate = VisualGate(gate, x, y)
        dict_logic_to_visual_gates[gate] = visual_child_gate
        visual_gates.append(visual_child_gate)

    for father_gate in lista_obj:
        for father_gate_output_ix in range(father_gate.number_of_outputs):
            child_gates_of_output_ix:set[tuple[AbstractGate,int]] = father_gate.get_child_gates_dict()[father_gate_output_ix]
            for child_gate, child_gate_input_ix in child_gates_of_output_ix:
                visual_father_gate:VisualGate = dict_logic_to_visual_gates[father_gate]
                visual_child_gate:VisualGate = dict_logic_to_visual_gates[child_gate]
                visual_father_gate.add_connection((visual_child_gate,child_gate_input_ix), father_gate_output_ix)
    return visual_gates
        


def auto_placement(considered_gates=GLOBAL_ALL_BASIC_GATES_LIST, considered_switches=GLOBAL_ALL_SWITCHES_LIST):
    gates_to_BFS_levels:dict[LogicClass,int] = get_gates_level_BFS(considered_gates=considered_gates, considered_switches=GLOBAL_ALL_SWITCHES_LIST)
    #print("gates_to_BFS_levels: "+ str(gates_to_BFS_levels))
    visual_gates:list[VisualGate] = create_visual_gates(dict_gate_to_BFS_level=gates_to_BFS_levels, considered_gates = considered_gates)
    return visual_gates

considered_gates=[not1,not2]
visual_gates = auto_placement(considered_gates=considered_gates)

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

