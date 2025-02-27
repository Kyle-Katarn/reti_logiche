import pygame
from reti_logiche import *
from math import sqrt

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Logic Gates Visualizer")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTBLUE = (173, 216, 230)
WHITE = (255, 255, 255)

GLOBAL_visual_gates:list["VisualGate"] = []
GLOBAL_visual_connections:list["VisualConnection"] = []

class VisualConnection:
    def __init__(self, start_gate_tup: tuple["VisualGate",int]=None, end_gate_tup: tuple["VisualGate",int]=None):
        self.start_gate_tup:tuple["VisualGate",int] = start_gate_tup
        self.end_gate_tup:tuple["VisualGate",int] = end_gate_tup
        self.start_x =0
        self.start_y =0
        self.end_x =0
        self.end_y =0
        self.update_connection()

    def set_end_coo(self, end_x, end_y):
        self.end_x = end_x
        self.end_y = end_y

    def update_connection(self):
        self.start_gate:VisualGate = self.start_gate_tup[0]
        self.start_gate_ix:int = self.start_gate_tup[1]
        self.end_gate: VisualGate = self.end_gate_tup[0]
        self.end_gate_ix:int = self.end_gate_tup[1]
        #start_gate output pin coo
        self.start_x = self.start_gate.x + self.start_gate.width
        start_y_segment:int = self.start_gate.height//(self.start_gate.gate.number_of_outputs+1)
        self.start_y = self.start_gate.y + start_y_segment*(self.start_gate_ix+1)
        #end_gate input pin coo
        if(self.end_gate_tup == None):
            self.end_x = self.end_gate.x
            end_y_segment:int = self.end_gate.height//(self.end_gate.gate.number_of_inputs+1)
            self.end_y = self.end_gate.y + end_y_segment*(self.end_gate_ix+1)
        
    def draw(self, screen):
        self.update_connection()
        color = BLACK
        if(self.start_gate.gate.get_output_signal_value(self.start_gate_ix)):
            color = RED
        pygame.draw.line(screen, color, (self.start_x, self.start_y), (self.end_x, self.end_y), 2)


class VisualPin:
    CONST_hitbox_scaling:int = 2
    def __init__(self, x:int, y:int, rad:int, type:str):
        self.type:str = type
        self.center_x = x
        self.center_y = y
        self.radious = rad

    def visual_pin_conains_point(self, px: int, py: int):
        Dx:int = px-self.center_x
        Dy:int = py-self.center_y
        return sqrt(Dx**2 + Dy**2) <= self.radious * self.CONST_hitbox_scaling

    def draw(self, pin_color):
        pygame.draw.circle(screen, pin_color, (self.center_x, self.center_y), self.radious)

class VisualGate:
    def __init__(self, gate: BasicGate, x: int, y: int):
        self.visual_connections: list[VisualConnection] = []
        self.visual_pins: list[VisualPin] = []
        self.gate = gate
        self.x = x
        self.y = y
        self.width = 100
        # Height based on max between inputs and outputs
        max_pins = max(gate.number_of_inputs, gate.number_of_outputs)
        self.height = max(60, max_pins * 30)
        self.pin_radius = 5
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    #*Gestione SPOSTAMENTO RETTANGOLO
    def visual_gate_contains_point(self, x: int, y: int) -> bool:
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)

    def visual_gate_start_drag(self, mouse_x: int, mouse_y: int):
        self.is_dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y

    def visual_gate_end_drag(self):
        self.is_dragging = False

    def visual_gate_update_position(self, mouse_x: int, mouse_y: int):
        if self.is_dragging:
            self.x = mouse_x - self.drag_offset_x
            self.y = mouse_y - self.drag_offset_y

    #*Gestione CREAZIONE COLLEGAMENTI
    def check_if_a_visual_pin_is_cicked(self, x: int, y: int):
        selected_pin:VisualPin = None
        for pin in self.visual_pins:
            if pin.visual_pin_conains_point(x,y):
                selected_pin = pin
                break
        return selected_pin
        

    def draw(self, screen):
        # Draw gate body
        pygame.draw.rect(screen, LIGHTBLUE, (self.x, self.y, self.width, self.height))
        
        # Draw gate name
        font = pygame.font.Font(None, 24)
        text = font.render(self.gate.name, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, text_rect)

        #* Draw input pins
        if self.gate.number_of_inputs > 0:
            spacing = self.height // (self.gate.number_of_inputs + 1)
            for i in range(self.gate.number_of_inputs):
                pin_color = RED if self.gate.get_input_signal_value(i) else BLACK
                y_pos = self.y + spacing * (i + 1)
                visual_pin:VisualPin = VisualPin(self.x, y_pos, self.pin_radius, "in")
                self.visual_pins.append(visual_pin)
                visual_pin.draw(pin_color)

        #* Draw output pins
        spacing = self.height // (self.gate.number_of_outputs + 1)
        for i in range(self.gate.number_of_outputs):
            pin_color = RED if self.gate.get_output_signal_value(i) else BLACK
            y_pos = self.y + spacing * (i + 1)
            visual_pin:VisualPin = VisualPin(self.x + self.width, y_pos, self.pin_radius, "out")
            self.visual_pins.append(visual_pin)
            visual_pin.draw(pin_color)
            
        # Draw connections
        for connection in self.visual_connections:
            connection.draw(screen)
            
        
    def add_connection(self, end_gate_tup:tuple["VisualGate",int], starting_pin_ix:int):
        connection = VisualConnection((self, starting_pin_ix), end_gate_tup)
        self.visual_connections.append(connection)


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
GLOBAL_visual_gates = auto_placement(considered_gates=considered_gates)

# Main game loop
running:bool = True
selected_gate:VisualGate = None
selected_pin:VisualPin = None
current_connetion:VisualConnection = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for gate in GLOBAL_visual_gates:
                selected_pin = gate.check_if_a_visual_pin_is_cicked(mouse_x, mouse_y)#il check sui pin ha la precedenza
                if(selected_pin):
                    break
                if gate.visual_gate_contains_point(mouse_x, mouse_y):
                    gate.visual_gate_start_drag(mouse_x, mouse_y)
                    selected_gate = gate
                    break

            '''
            start_coo, end_coo
            '''
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_pin:
                pass
            if selected_gate:
                selected_gate.visual_gate_end_drag()
                selected_gate = None

        elif event.type == pygame.MOUSEMOTION:
            if selected_pin:
                pass
            if selected_gate:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_gate.visual_gate_update_position(mouse_x, mouse_y)
    
    screen.fill(WHITE)
    
    # Draw all gates
    for visual_gate in GLOBAL_visual_gates:
        visual_gate.draw(screen)

    for connection in GLOBAL_visual_connections:
        connection.draw(screen) 
    
    pygame.display.flip()

pygame.quit()

