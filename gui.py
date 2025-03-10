import pygame
import gc
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
GREEN = (0, 200, 0)

GLOBAL_visual_gates:list["VisualGate"] = []
#GLOBAL_visual_connections:list["VisualConnection"] = []

class VisualConnection:
    def __init__(self):
        self.color = YELLOW
        self.is_self_in_connections_chosen_for_action_set:bool = False#Needed to determine the color
        self.start_pin:VisualPin = None
        self.end_pin:VisualPin = None
        self.start_x =0
        self.start_y =0
        self.end_x =0
        self.end_y =0
        self.hitbox_length = 5
        self.is_connection_finalized:bool = False
        #^^distingue il caso in cui ha un pin a null perchè non hai ancora selezionato il secondo con mouse
        #dal caso in cui lo start_pin (assieme alla sua VisualGate madre) viene eliminato dall'utente -> la connection deve essere eliminata a catena 
        #is_connection_finalized = TRUE, quando viene selezionato il 2^pin
    def set_coordinates(self, start = None, end = None):
        if(start != None):
            self.start_x, self.start_y = start
        if(end != None):
            self.end_x, self.end_y = end

    def set_pin(self, pin:"VisualPin"):
        if(pin.type == "out"):#todo FIX errore uscita---->entrata
            self.start_pin = pin
            self.start_pin.pin_of_visual_connections_set.add(self)
        else:#type = in
            print(f"pin.pin_of_visual_connections_set {pin.pin_of_visual_connections_set}")
            if(pin.pin_of_visual_connections_set != set()):#todo obbligo refactoring???
                print("WARNING, rimosso una connessione per coneterne una nuova")
                old_input_pin_connection:VisualConnection = pin.pin_of_visual_connections_set.pop()
                old_input_pin_connection.remove_self()

            self.end_pin = pin
            self.end_pin.pin_of_visual_connections_set.add(self)
            self.get_end_pin_visual_gate().visual_connections.add(self)
            self.connect_logic_pins()
                

    def auto_update_connection(self):
        if(self.start_pin == None and self.end_pin == None):
            raise Exception(f"@VISUAL ERROR: self.start_pin={self.start_pin} or self.end_pin={self.end_pin} is NONE")
        if(self.start_pin != None):
            self.start_x, self.start_y = self.start_pin.get_coordinates()
        if(self.end_pin != None):
            self.end_x, self.end_y= self.end_pin.get_coordinates()
        
    def draw(self, screen):
        if(self.start_pin and self.end_pin):
            self.is_connection_finalized = True
        if(self.is_connection_finalized and (not self.start_pin.pin_of_visual_gate in GLOBAL_visual_gates)):#!MOLTO GOOFY ma non so come rimuovere la classe in altro modo
            self.remove_self()
        if(self.is_connection_finalized):
            self.auto_update_connection()
        if(self.start_pin):
            if(self.is_self_in_connections_chosen_for_action_set):
                self.color = GREEN
            elif(not self.is_connection_finalized):
                self.color = YELLOW
            else:
                self.color = self.start_pin.color
            #print(f"self.start_pin.color: {self.start_pin.color}")
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y), 2)

    def remove_self(self):
        print(f"gate: {self.get_end_pin_visual_gate().gate}")
        self.get_end_pin_visual_gate().visual_connections.remove(self)
        self.unconnect_logic_pins()

    def connect_logic_pins(self):
        print("connect_logic_pins NON FA NULLA")
        pass#boh

    def unconnect_logic_pins(self):
        print("unconnect_logic_pins NON FA NULLA")
        #!self.end_pin.unconnect_logic_pin()#rimuove l'input gate
        pass

    def get_end_pin_visual_gate(self):
        return self.end_pin.pin_of_visual_gate

    def is_visual_connection_clicked(self, px: int, py: int):
        # Calculate the distance from the point to the line segment
        line_dx = self.end_x - self.start_x
        line_dy = self.end_y - self.start_y
        length_squared = line_dx ** 2 + line_dy ** 2

        if length_squared == 0:
            # The line segment is actually a point
            distance = sqrt((px - self.start_x) ** 2 + (py - self.start_y) ** 2)
        else:
            # Project point onto the line segment and calculate the distance
            t = max(0, min(1, ((px - self.start_x) * line_dx + (py - self.start_y) * line_dy) / length_squared))
            projection_x = self.start_x + t * line_dx
            projection_y = self.start_y + t * line_dy
            distance = sqrt((px - projection_x) ** 2 + (py - projection_y) ** 2)

        return distance <= self.hitbox_length
        


class VisualPin:
    CONST_hitbox_scaling:int = 2
    def __init__(self, pin_of_visual_gate:"VisualGate", logic_gate_index:int, offset_x:int, offset_y:int, rad:int, type:str):
        self.type:str = type
        self.pin_of_visual_connections_set:set[VisualConnection] = set()
        self.logic_gate_index:int = logic_gate_index
        self.pin_of_visual_gate:"VisualGate" = pin_of_visual_gate
        #^^Avere una reference serve a evitare di dover riassegnare manualmente le coordinate ogni volta che sposto la VisualGate, forse era meglio avere una ref al padre? si era meglio
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.radious = rad
        self.color = BLACK

    def visual_pin_conains_point(self, px: int, py: int):
        Dx:int = px-(self.pin_of_visual_gate.x+self.offset_x)
        Dy:int = py-(self.pin_of_visual_gate.y+self.offset_y)
        return sqrt(Dx**2 + Dy**2) <= self.radious * self.CONST_hitbox_scaling

    def draw(self):
        if(self.type == "in"):
            self.color = RED if self.pin_of_visual_gate.gate.get_input_signal_value(self.logic_gate_index) else BLACK
        else:
            self.color = RED if self.pin_of_visual_gate.gate.get_output_signal_value(self.logic_gate_index) else BLACK
        pygame.draw.circle(screen, self.color, (self.pin_of_visual_gate.x+self.offset_x, self.pin_of_visual_gate.y+self.offset_y), self.radious)

    def get_coordinates(self):
        return (self.pin_of_visual_gate.x+self.offset_x, self.pin_of_visual_gate.y+self.offset_y)
    



class VisualGate:
    def __init__(self, gate: BasicGate, x: int, y: int):
        self.visual_connections: set[VisualConnection] = set()#! FIX, NON USATO, VISUAL CONNECTIONS GLOBALE NON VA BENE X LA COPIATURA
        self.visual_input_pins: list[VisualPin] = []
        self.visual_output_pins: list[VisualPin] = []
        self.gate = gate
        self.x = x 
        self.y = y
        self.color = LIGHTBLUE
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
                visual_pin:VisualPin = VisualPin(self, i, 0, y_offset, self.pin_radius, "in")#!maybe coo obj? no just pass the reference of father_class
                self.visual_input_pins.append(visual_pin)
                
        #* / output
        spacing = self.height // (self.gate.number_of_outputs + 1)
        for i in range(self.gate.number_of_outputs):
            y_offset = spacing * (i + 1)
            visual_pin:VisualPin = VisualPin(self, i, self.width, y_offset, self.pin_radius, "out")
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

    #*Gestione SELEZIONE PIN (PIN)
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
    
    #*Gestione SELEZIONE CONNESSIONE (CONNESSIONE)
    def check_if_a_visual_connection_is_cicked(self, x: int, y: int):
        selected_connection:VisualConnection = None
        for connection in self.visual_connections:
            if(connection.is_visual_connection_clicked(x,y)):
                selected_connection = connection
                break
        return selected_connection
    
    #*ELIMINAZIONE
    def delete_internal_logic_gate(self):
        print("DOES NOTHING, THIS SHOULD REMOVE LOGIC GATE FROM SIM")

    def draw(self, screen):
        # Draw gate body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw gate name
        font = pygame.font.Font(None, 24)
        text = font.render(self.gate.name, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, text_rect)
            
        #* Draw PINS
        for input_pin_ix in range(self.gate.number_of_inputs):
            self.visual_input_pins[input_pin_ix].draw()
        for output_pin_ix in range(self.gate.number_of_outputs):
            self.visual_output_pins[output_pin_ix].draw()

        #* Draw Connections
        for vc in self.visual_connections:
            vc.draw(screen)
            

def get_gates_level_BFS(considered_gates:list[LogicClass] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[LogicClass] = GLOBAL_ALL_SWITCHES_LIST):
    dict_gate_to_BFS_level:dict[LogicClass,int] = dict()

    visited_gates_set:set[LogicClass] = set() #x cicli
    starting_gates:list[LogicClass] = []
    starting_gates.extend(considered_switches)
    #print(considered_gates)
    for g in considered_gates:
        #print("gate: "+ str(g) + str(g.get_all_input_gates()))
        if(len(g.get_all_input_gates()) == 0):
            starting_gates.append(g)
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


dict_logic_to_visual_gates:dict[LogicClass, VisualGate] = {}#useful for debug
def create_visual_gates(dict_gate_to_BFS_level:dict[LogicClass, int], considered_gates: list[LogicClass] = GLOBAL_ALL_BASIC_GATES_LIST, considered_swiches = GLOBAL_ALL_SWITCHES_LIST):
    #todo 1 -> tutti i gate puntati da 1 -> 2. ->
    
    visual_gates:set[VisualGate] = []
    x, y = -100, 50
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
                new_connection.set_pin(start_pin)
                new_connection.set_pin(end_pin)
                visual_child_gate.visual_connections.add(new_connection)
                #GLOBAL_visual_connections.append(new_connection) #! CHANGE
    return visual_gates
        


def auto_placement(considered_gates=GLOBAL_ALL_BASIC_GATES_LIST, considered_switches=GLOBAL_ALL_SWITCHES_LIST):
    gates_to_BFS_levels:dict[LogicClass,int] = get_gates_level_BFS(considered_gates=considered_gates, considered_switches=GLOBAL_ALL_SWITCHES_LIST)
    #print("gates_to_BFS_levels: "+ str(gates_to_BFS_levels))
    print("ciao")
    visual_gates:list[VisualGate] = create_visual_gates(dict_gate_to_BFS_level=gates_to_BFS_levels, considered_gates = considered_gates)
    return visual_gates



considered_gates=[not1,not2]
GLOBAL_visual_gates = auto_placement(considered_gates=considered_gates)




# Main game loop
running:bool = True
#gestione spostamento gate
selected_gate:VisualGate = None
#gestione pin e crezione connessioni
first_pin:VisualPin = None
second_pin:VisualPin = None
selected_pin:VisualPin = None
is_first_pin_already_selected = False
first_pin_type = None
connection_being_created:VisualConnection = None
#gestione azioni (cancellazione, copia, incolla) su oggetto
#selected_gate
selected_connection:VisualConnection = None
gates_chosen_for_action_set:set[VisualGate] = set()
are_gates_chosen_for_action_being_dragged:bool = False
connections_chosen_for_action_set:set[VisualConnection] = set()




while running:
    keys_pressed = pygame.key.get_pressed()#premute in un dato frame, dura N frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #L'evento pygame.MOUSEBUTTONDOWN si attiva solo per un singolo frame quindi il for è chiamato 1 sola volta per pressione
            selected_pin = None
            selected_gate = None
            for gate in GLOBAL_visual_gates: 
                selected_connection = gate.check_if_a_visual_connection_is_cicked(mouse_x, mouse_y)#*HAI PREMUTO SU UNA CONNESSIONE
                if((keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and selected_connection):
                    break

                selected_pin = gate.check_if_a_visual_pin_is_cicked(mouse_x, mouse_y)#*HAI PREMUTO SU UN PIN
                if(selected_pin):
                    break#check dei pin ha la precedenza

                if not selected_gate and gate.visual_gate_contains_point(mouse_x, mouse_y):#*HAI PREMUTO SU UN GATE
                    selected_gate = gate
                    break


            if not keys_pressed[pygame.K_LCTRL] and not keys_pressed[pygame.K_RCTRL]: #*CTRL non sta vendendo Premuto
                if(selected_pin): #was_mouse_button_up non è necessario, perchè BUTTONDOWN è attivo per un solo frame
                    if(not is_first_pin_already_selected):#* SELEZIONE 1^PIN
                        print("PRIMO pin selezionato con successo")
                        connection_being_created:VisualConnection = VisualConnection()
                        first_pin_type = selected_pin.type
                        connection_being_created.set_pin(selected_pin)
                        is_first_pin_already_selected = True

                    else:#* 1^pin è già stato selezionato; SELEZIONE 2^PIN
                        if(selected_pin.type == first_pin_type):
                            print("WARNING, you can't connect 2 inputs or 2 outputs")
                        else:
                            print("secondo pin selezionato con successo")
                            connection_being_created.set_pin(selected_pin)#todo setta collegamento logico se entrambi i pin sono != NULL
                            #connection_being_created.get_end_pin_visual_gate().visual_connections.add(connection_being_created)#todo non necessaria
                            connection_being_created.is_connection_finalized = True
                            connection_being_created = None #reset
                            is_first_pin_already_selected = False #reset
                            first_pin_type = None #reset

                else:#hai premuto sul vuoto o su un gate
                    print("hai premuto sul vuoto o su un gate")
                    connection_being_created = None #reset
                    is_first_pin_already_selected = False #reset
                    first_pin_type = None #reset
                
                if(selected_gate):#*START SPOSTAMENTO 1 GATE
                    #print(f"{mouse_x}, {mouse_y}")
                    selected_gate.visual_gate_start_drag(mouse_x, mouse_y)

            else:#* SELEZIONE E DESELEZIONE DI GATES E CONNESSIONI
                #print("CTRL STA VENENDO PREMUTO")
                connection_being_created = None #reset
                is_first_pin_already_selected = False #reset
                first_pin_type = None #reset
                if(selected_connection):
                    print("CTRL click su una connessione")
                    if(not selected_connection in connections_chosen_for_action_set):
                        connections_chosen_for_action_set.add(selected_connection)
                        selected_connection.is_self_in_connections_chosen_for_action_set = True
                    else:
                        connections_chosen_for_action_set.remove(selected_connection)
                        selected_connection.is_self_in_connections_chosen_for_action_set = False
                elif(selected_gate):
                    print("CTRL click su un gate")
                    if(not selected_gate in gates_chosen_for_action_set):
                        gates_chosen_for_action_set.add(selected_gate)
                        selected_gate.color = GREEN
                    else:
                        gates_chosen_for_action_set.remove(selected_gate)
                        selected_gate.color = LIGHTBLUE
                else:
                    print("CTRL click sul vuoto")
                    for vg in gates_chosen_for_action_set:
                        vg.color = LIGHTBLUE
                    gates_chosen_for_action_set.clear()
                    for vc in connections_chosen_for_action_set:
                        vc.is_self_in_connections_chosen_for_action_set = False
                    connections_chosen_for_action_set.clear()


            if(False):
                print("STATUS:")
                print(f"selected_pin: {selected_pin}")
                print(f"is_first_pin_already_selected: {is_first_pin_already_selected}")
                print(f"first_pin_type: {first_pin_type}")
                print(f"connection_being_created: {connection_being_created}")
                print("")
            
        elif event.type == pygame.MOUSEBUTTONUP:
            print("mouse button up")
            if selected_gate:#*END SPOSTAMENTO 1 GATE
                selected_gate.visual_gate_end_drag()
                selected_gate = None

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:  # *START/END SPOSTAMENTO N GATES in gates_chosen_for_action_set
            print("K_m")
            are_gates_chosen_for_action_being_dragged = not are_gates_chosen_for_action_being_dragged 
            for vg in gates_chosen_for_action_set.copy():
                if(are_gates_chosen_for_action_being_dragged):
                    vg.visual_gate_start_drag(mouse_x,mouse_y)
                else:
                    vg.visual_gate_end_drag()
                    for vg in gates_chosen_for_action_set:#reset
                        vg.color = LIGHTBLUE
                    gates_chosen_for_action_set.clear()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:  #* CANCELLAZIONE GATES, CONNESSIONI
            for vg in gates_chosen_for_action_set:
                GLOBAL_visual_gates.remove(vg)
                vg.delete_internal_logic_gate()

            for vc in connections_chosen_for_action_set:
                vc.remove_self()
                vc.unconnect_logic_pins()
                pass
            gates_chosen_for_action_set.clear()
            connections_chosen_for_action_set.clear()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            print("K_c")
            import copy
            copied_gates:set[VisualGate] = copy.deepcopy(gates_chosen_for_action_set)
            for vc in gates_chosen_for_action_set:
                vc.color = LIGHTBLUE
            gates_chosen_for_action_set.clear()
            gates_chosen_for_action_set.update(copied_gates)
            for vc in gates_chosen_for_action_set:
                vc.x+=30
                vc.y+=30
            GLOBAL_visual_gates.extend(copied_gates)

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if(connection_being_created != None): #*SPOSTAMENTO MOUSE connection_being_created
                connection_being_created.auto_update_connection()
                if(first_pin_type == "out"):#spostalo interno a classe pin?
                    connection_being_created.set_coordinates(end=(mouse_x,mouse_y))
                else:
                    connection_being_created.set_coordinates(start=(mouse_x,mouse_y))
            
            if selected_gate:#* SPOSTAMENTO MOUSE 1 GATE
                selected_gate.visual_gate_update_position(mouse_x, mouse_y)
            if are_gates_chosen_for_action_being_dragged:#*SPOSTAMENTO MOUSE N GATES
                for vg in gates_chosen_for_action_set:
                    vg.visual_gate_update_position(mouse_x,mouse_y)

    
    screen.fill(WHITE)
    
    # Draw all gates
    for visual_gate in GLOBAL_visual_gates.copy():
        visual_gate.draw(screen)


    '''#!old
    for connection in GLOBAL_visual_connections:
        connection.draw(screen)
    ''' 

    if(connection_being_created != None):
        connection_being_created.draw(screen=screen)
    
    pygame.display.flip()

pygame.quit()

def connection_debugger(logic_gate:LogicClass):
    print("")
    input_visual_gate:VisualGate = dict_logic_to_visual_gates[logic_gate]
    visual_connections_set:set[VisualConnection] = input_visual_gate.visual_connections

    if(len(visual_gate.visual_input_pins) != 0):
        print(f"Input pins of {visual_gate.gate.name}")
        for ivp in visual_gate.visual_input_pins:
            print(f"input pin {ivp}")

    if(len(visual_connections_set) == 0):
        print(f"NO connections point to {logic_gate.name}")
    for vc in visual_connections_set:
        print(f"#@visual connection: {vc}")
        start_pin:VisualPin = vc.start_pin
        end_pin:VisualPin = vc.end_pin
        print(f"start_pin: {start_pin}")
        print(f"    start_pin father: {start_pin.pin_of_visual_gate.gate.name} | start_pin_type: {start_pin.type} | start_pin_ix: {start_pin.logic_gate_index} | start_pin_color: {start_pin.color}")
        print(f"end_pin: {end_pin}")
        print(f"    end_pin father: {end_pin.pin_of_visual_gate.gate.name} | end_pin_type: {end_pin.type} | end_pin_ix: {end_pin.logic_gate_index} | end_pin_color: {end_pin.color}")
        print("")

    


connection_debugger(not2)#todo errore!!
#!metti apposto la documentazione!!!