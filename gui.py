import pygame
import gc
from reti_logiche import *
from ui_elements import *
from ui_elements import InputField
import GLOBAL_VARIABLES as GV
from math import sqrt
from visual_classes import *


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GV.SCREEN_WIDTH, GV.SCREEN_HEIGHT))
pygame.display.set_caption("Logic Gates Visualizer")




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
                #visual_child_gate.visual_connections.add(new_connection)#!!!
    return visual_gates
        


def auto_placement(considered_gates=GLOBAL_ALL_BASIC_GATES_LIST, considered_switches=GLOBAL_ALL_SWITCHES_LIST):
    gates_to_BFS_levels:dict[LogicClass,int] = get_gates_level_BFS(considered_gates=considered_gates, considered_switches=GLOBAL_ALL_SWITCHES_LIST)
    #print("gates_to_BFS_levels: "+ str(gates_to_BFS_levels))
    print("ciao")
    visual_gates:list[VisualGate] = create_visual_gates(dict_gate_to_BFS_level=gates_to_BFS_levels, considered_gates = considered_gates)
    return visual_gates



considered_gates=[not1,not2]
GV.GLOBAL_visual_gates = auto_placement(considered_gates=considered_gates)


UI_ELEMENTS_SET:set[ButtonClass] = set()
next_frame_button = NextFrameButton()
previous_frame_button = PreviousFrameButton()
play_simulation_button = PlaySimulationButton()
input_field = InputField()
UI_ELEMENTS_SET.add(next_frame_button)
UI_ELEMENTS_SET.add(previous_frame_button)
UI_ELEMENTS_SET.add(play_simulation_button)
UI_ELEMENTS_SET.add(input_field)


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

debug_prints:bool = True

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
            for gate in GV.GLOBAL_visual_gates: 
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
                        if debug_prints:
                            print("PRIMO pin selezionato con successo")
                        connection_being_created:VisualConnection = VisualConnection()
                        first_pin_type = selected_pin.type
                        connection_being_created.set_pin(selected_pin)
                        is_first_pin_already_selected = True

                    else:#* 1^pin è già stato selezionato; SELEZIONE 2^PIN
                        if(selected_pin.type == first_pin_type):
                            if debug_prints:
                                print("WARNING, you can't connect 2 inputs or 2 outputs")
                        else:
                            if debug_prints:
                                print("secondo pin selezionato con successo")
                            connection_being_created.set_pin(selected_pin)#todo setta collegamento logico se entrambi i pin sono != NULL
                            #connection_being_created.get_end_pin_visual_gate().visual_connections.add(connection_being_created)#todo non necessaria
                            connection_being_created.is_connection_finalized = True
                            connection_being_created = None #reset
                            is_first_pin_already_selected = False #reset
                            first_pin_type = None #reset

                else:#hai premuto sul vuoto o su un gate
                    if debug_prints:
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
                    if debug_prints:
                        print("CTRL click su una connessione")
                    if(not selected_connection in connections_chosen_for_action_set):
                        connections_chosen_for_action_set.add(selected_connection)
                        selected_connection.is_self_in_connections_chosen_for_action_set = True
                    else:
                        connections_chosen_for_action_set.remove(selected_connection)
                        selected_connection.is_self_in_connections_chosen_for_action_set = False
                elif(selected_gate):
                    if debug_prints:
                        print("CTRL click su un gate")
                    if(not selected_gate in gates_chosen_for_action_set):
                        gates_chosen_for_action_set.add(selected_gate)
                        selected_gate.color = GV.GREEN
                    else:
                        gates_chosen_for_action_set.remove(selected_gate)
                        selected_gate.color = GV.LIGHTBLUE
                else:
                    if debug_prints:
                        print("CTRL click sul vuoto")
                    for vg in gates_chosen_for_action_set:
                        vg.color = GV.LIGHTBLUE
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
            if debug_prints:
                print("mouse button up")
            if selected_gate:#*END SPOSTAMENTO 1 GATE
                selected_gate.visual_gate_end_drag()
                selected_gate = None

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:  # *START/END SPOSTAMENTO N GATES in gates_chosen_for_action_set
            if debug_prints:
                print("K_m")
            are_gates_chosen_for_action_being_dragged = not are_gates_chosen_for_action_being_dragged 
            for vg in gates_chosen_for_action_set.copy():
                if(are_gates_chosen_for_action_being_dragged):
                    vg.visual_gate_start_drag(mouse_x,mouse_y)
                else:
                    vg.visual_gate_end_drag()
                    for vg in gates_chosen_for_action_set:#reset
                        vg.color = GV.LIGHTBLUE
                    gates_chosen_for_action_set.clear()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:  #* CANCELLAZIONE GATES, CONNESSIONI
            for vg in gates_chosen_for_action_set:
                GV.GLOBAL_visual_gates.remove(vg)
                vg.delete_internal_logic_gate()

            for vc in connections_chosen_for_action_set:
                vc.remove_self()
                vc.unconnect_logic_pins()
                pass
            gates_chosen_for_action_set.clear()
            connections_chosen_for_action_set.clear()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            if debug_prints:
                print("K_c")
            import copy
            copied_gates:set[VisualGate] = copy.deepcopy(gates_chosen_for_action_set)
            for vc in gates_chosen_for_action_set:
                vc.color = GV.LIGHTBLUE
            gates_chosen_for_action_set.clear()
            gates_chosen_for_action_set.update(copied_gates)
            for vc in gates_chosen_for_action_set:
                vc.x+=30
                vc.y+=30
            GV.GLOBAL_visual_gates.extend(copied_gates)

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

        for button in UI_ELEMENTS_SET:
            button.handle_event(event)

    
    screen.fill(GV.WHITE)
    
    # Draw all gates
    for visual_gate in GV.GLOBAL_visual_gates.copy():
        visual_gate.draw(screen)

    # draw all buttons
    for button in UI_ELEMENTS_SET:
        button.draw(screen)

        #!button.handle_event(event) WHY DOES IT EXIST OUTSIDE THE LOOP??
        #!print(event)


    '''#!old
    for connection in GLOBAL_visual_connections:
        connection.draw(screen)
    ''' 

    if(connection_being_created != None):
        connection_being_created.draw(screen=screen)

    
    
    pygame.display.flip()

pygame.quit()
