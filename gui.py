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
YELLOW = (255, 255, 0)

GLOBAL_visual_gates:list["VisualGate"] = []
GLOBAL_visual_connections:list["VisualConnection"] = []

class VisualConnection:
    def __init__(self):
        self.color = YELLOW
        self.start_pin:VisualPin = None
        self.end_pin:VisualPin = None
        self.start_x =0
        self.start_y =0
        self.end_x =0
        self.end_y =0

    def set_coordinates(self, start = None, end = None):
        if(start != None):
            self.start_x, self.start_y = start
        if(end != None):
            self.end_x, self.end_y = end

    def set_pins(self, start_pin:"VisualPin" = None, end_pin:"VisualPin" = None):
        self.start_pin = start_pin
        self.end_pin = end_pin

    def set_pin(self, pin:"VisualPin"):
        if(pin.type == "in"):
            self.start_pin = pin
        else:
            self.end_pin = pin

    def auto_update_connection(self):
        if(self.start_pin == None and self.end_pin == None):
            raise Exception(f"@VISUAL ERROR: self.start_pin={self.start_pin} or self.end_pin={self.end_pin} is NONE")
        if(self.start_pin != None):
            self.start_x, self.start_y = self.start_pin.get_coordinates()
        if(self.end_pin != None):
            self.end_x, self.end_y= self.end_pin.get_coordinates()
        
        
    def draw(self, screen):
        if(self.start_pin != None and self.end_pin != None):
            self.auto_update_connection()
        if(self.start_pin):
            color = self.start_pin.color
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y), 2)


class VisualPin:
    CONST_hitbox_scaling:int = 15
    def __init__(self, visual_gate:"VisualGate", offset_x:int, offset_y:int, rad:int, type:str):
        self.type:str = type
        self.visual_gate:"VisualGate" = visual_gate
        #^^Avere una reference serve a evitare di dover riassegnare manualmente le coordinate ogni volta che sposto la VisualGate, forse era meglio avere una ref al padre? si era meglio
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.radious = rad
        self.color = BLACK

    def visual_pin_conains_point(self, px: int, py: int):
        #print((self.visual_gate.x+self.offset_x))
        Dx:int = px-(self.visual_gate.x+self.offset_x)
        Dy:int = py-(self.visual_gate.y+self.offset_y)
        #print(px-self.visual_gate.x+self.offset_x)
        #print(f"Dx {Dx} Dy {Dy}, mousex {px}, mousey: {py}| pinX: {self.visual_gate.x+self.offset_x}, pinY: {self.visual_gate.x+self.offset_y}")
        return sqrt(Dx**2 + Dy**2) <= self.radious * self.CONST_hitbox_scaling

    def draw(self, pin_color):
        pygame.draw.circle(screen, pin_color, (self.visual_gate.x+self.offset_x, self.visual_gate.y+self.offset_y), self.radious)

    def get_coordinates(self):
        return (self.visual_gate.x+self.offset_x, self.visual_gate.y+self.offset_y)



class VisualGate:
    def __init__(self, gate: BasicGate, x: int, y: int):
        self.visual_connections: list[VisualConnection] = []
        self.visual_input_pins: list[VisualPin] = []
        self.visual_output_pins: list[VisualPin] = []
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

        #* ISTANZIA CLASSI PIN / input
        if self.gate.number_of_inputs > 0:
            spacing = self.height // (self.gate.number_of_inputs + 1)
            for i in range(self.gate.number_of_inputs):
                y_offset = spacing * (i + 1)
                visual_pin:VisualPin = VisualPin(self, 0, y_offset, self.pin_radius, "in")#!maybe coo obj?
                self.visual_input_pins.append(visual_pin)
                
        #* / output
        spacing = self.height // (self.gate.number_of_outputs + 1)
        for i in range(self.gate.number_of_outputs):
            y_offset = spacing * (i + 1)
            visual_pin:VisualPin = VisualPin(self, self.width, y_offset, self.pin_radius, "out")
            self.visual_output_pins.append(visual_pin)

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
        all_pins = []
        all_pins.extend(self.visual_input_pins)
        all_pins.extend(self.visual_output_pins)
        for pin in all_pins:
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
            
        # Draw PINS
        for input_pin_ix in range(self.gate.number_of_inputs):
            pin_color = RED if self.gate.get_input_signal_value(input_pin_ix) else BLACK
            self.visual_input_pins[input_pin_ix].draw(pin_color)
        for output_pin_ix in range(self.gate.number_of_outputs):
            pin_color = RED if self.gate.get_output_signal_value(output_pin_ix) else BLACK
            self.visual_output_pins[output_pin_ix].draw(pin_color)
            
    '''  
    def add_connection(self, end_gate_tup:tuple["VisualGate",int], starting_pin_ix:int):
        connection = VisualConnection((self, starting_pin_ix), end_gate_tup)
        self.visual_connections.append(connection)
    '''

def get_gates_level_BFS(considered_gates:list[LogicClass] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[LogicClass] = GLOBAL_ALL_SWITCHES_LIST):
    dict_gate_to_BFS_level:dict[LogicClass,int] = dict()

    visited_gates_set:set[LogicClass] = set() #x cicli
    starting_gates:list[LogicClass] = []
    starting_gates.extend(considered_switches)
    for g in considered_gates:
        #print("gate: "+ str(g) + str(g.get_all_input_gates()))
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
        father_gate_child_dict:dict[int,tuple[AbstractGate,int]] = father_gate.get_child_gates_dict()
        for father_gate_output_ix in range(father_gate.number_of_outputs):
            child_gates_of_output_ix:set[tuple[AbstractGate,int]] = father_gate_child_dict[father_gate_output_ix]
            for child_gate, child_gate_input_ix in child_gates_of_output_ix:
                visual_father_gate:VisualGate = dict_logic_to_visual_gates[father_gate]
                visual_child_gate:VisualGate = dict_logic_to_visual_gates[child_gate]
                #visual_father_gate.add_connection((visual_child_gate,child_gate_input_ix), father_gate_output_ix)
                #print(f"father gate childer: {father_gate.get_all_child_gates()}")
                #print(f"visual_father_gate.visual_output_pins: {visual_father_gate.visual_output_pins}")#!non creai i pin
                start_pin:VisualPin = visual_father_gate.visual_output_pins[father_gate_output_ix]
                end_pin:VisualPin = visual_child_gate.visual_input_pins[child_gate_input_ix]
                new_connection:VisualConnection = VisualConnection()
                new_connection.set_pins(start_pin,end_pin)
                GLOBAL_visual_connections.append(new_connection)
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
is_first_pin_already_selected = False
first_pin_type = None
was_mouse_button_up:bool = True#*or it will keep selecting the same pin while the mouse button is down
current_connetion:VisualConnection = None


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for gate in GLOBAL_visual_gates: #*GESTIONE CONNESSIONE (hai premuto su un pin)
                selected_pin:VisualPin = gate.check_if_a_visual_pin_is_cicked(mouse_x, mouse_y)#il check sui pin ha la precedenza
                if(selected_pin and was_mouse_button_up == True):
                    if(not is_first_pin_already_selected):#* nessun pin già selezionato
                        print("nessun pin gia' selezionato")
                        current_connetion:VisualConnection = VisualConnection()
                        first_pin_type = selected_pin.type
                        current_connetion.set_pin(selected_pin)
                        is_first_pin_already_selected = True

                    else:#* 1^pin è già stato selezionato
                        if(selected_pin.type == first_pin_type):
                            print("WARNING, you can't connect 2 inputs or 2 outputs")
                        else:
                            print("secondo pin selezionato con successo")
                            current_connetion.set_pin(selected_pin)
                            GLOBAL_visual_connections.append(current_connetion)
                            current_connetion = None #reset
                            is_first_pin_already_selected = False #reset
                            first_pin_type = None #reset
                        
                    #print(f"start_pin: {selected_pin} of {gate.gate.name}" )
                    #print(f"current_connetion.start_pin: {current_connetion.start_pin}")

                else: #*(hai premuto sul vuoto o su un gate)
                    pass

                if selected_pin == None and gate.visual_gate_contains_point(mouse_x, mouse_y): #*GESTIONE SPOSTAMENTO GATES
                    gate.visual_gate_start_drag(mouse_x, mouse_y)
                    selected_gate = gate
                    break

            was_mouse_button_up = False #*in ogni caso, fuori dal for

            if(not selected_pin):
                if(was_mouse_button_up):
                        print("hai premuto sul vuoto o su un gate")
                        current_connetion = None #reset
                        is_first_pin_already_selected = False #reset
                        first_pin_type = None #reset

            if(was_mouse_button_up):
                print("STATUS:")
                print(f"selected_pin: {selected_pin}")
                print(f"is_first_pin_already_selected: {is_first_pin_already_selected}")
                print(f"first_pin_type: {first_pin_type}")
                print(f"was_mouse_button_up: {was_mouse_button_up}")
                print(f"current_connetion: {current_connetion}")
                print("")
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_gate:#*GESTIONE SPOSTAMENTO GATES
                selected_gate.visual_gate_end_drag()
                selected_gate = None

            was_mouse_button_up = True

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if(current_connetion != None): #*GESTIONE CONNESSIONE
                current_connetion.auto_update_connection()
                if(first_pin_type == "in"):
                    current_connetion.set_coordinates(end=(mouse_x,mouse_y))
                else:
                    current_connetion.set_coordinates(start=(mouse_x,mouse_y))
            
            if selected_gate:#*GESTIONE SPOSTAMENTO GATES
                selected_gate.visual_gate_update_position(mouse_x, mouse_y)
    
    screen.fill(WHITE)
    
    # Draw all gates
    for visual_gate in GLOBAL_visual_gates:
        visual_gate.draw(screen)

    for connection in GLOBAL_visual_connections:
        connection.draw(screen) 

    if(current_connetion != None):
        current_connetion.draw(screen=screen)
    
    pygame.display.flip()

pygame.quit()

