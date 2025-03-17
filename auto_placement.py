from visual_classes import *

def get_gates_level_BFS(considered_gates:list[LogicClass], considered_switches:list[LogicClass]):
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
    
    visual_gates:set[VisualGate] = set()
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
        visual_gates.add(visual_child_gate)#? funzionava con .append?

    for father_gate in lista_obj:
        father_gate_child_dict:dict[int,tuple[AbstractGate,int]] = father_gate.get_child_gates_dict()
        for father_gate_output_ix in range(father_gate.number_of_outputs):
            child_gates_of_output_ix:set[tuple[AbstractGate,int]] = father_gate_child_dict[father_gate_output_ix]
            for child_gate, child_gate_input_ix in child_gates_of_output_ix:
                visual_father_gate:VisualGate = dict_logic_to_visual_gates[father_gate]
                visual_child_gate:VisualGate = dict_logic_to_visual_gates.get(child_gate, None)
                if(visual_child_gate != None):
                    start_pin:VisualPin = visual_father_gate.visual_output_pins[father_gate_output_ix]
                    end_pin:VisualPin = visual_child_gate.visual_input_pins[child_gate_input_ix]
                    new_connection:VisualConnection = VisualConnection()
                    new_connection.set_pin(start_pin)
                    new_connection.set_pin(end_pin)
        
    return visual_gates
        


def auto_placement(considered_gates=GLOBAL_ALL_BASIC_GATES_LIST, considered_switches=GLOBAL_ALL_SWITCHES_LIST):
    gates_to_BFS_levels:dict[LogicClass,int] = get_gates_level_BFS(considered_gates=considered_gates, considered_switches=GLOBAL_ALL_SWITCHES_LIST)
    #print("gates_to_BFS_levels: "+ str(gates_to_BFS_levels))
    print("ciao")
    visual_gates:list[VisualGate] = create_visual_gates(dict_gate_to_BFS_level=gates_to_BFS_levels, considered_gates = considered_gates)
    return visual_gates