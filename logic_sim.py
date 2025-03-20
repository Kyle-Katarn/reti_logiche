from reti_logiche import *

def apply_SwitchGates_immediatly(considered_switches):
    for switch in considered_switches:
        switch.set_child_gates_input_signals()
        for gate, gate_input_ix in switch.get_all_child_gates():
            print(f"Gate: {gate.name} input: {gate_input_ix} > set to {switch.get_output_signal_value()}")
        
#! no devi controllare che gli input che averbbero determinato l'input rimangano stabili per tutti e 10 i secondi, l'intersezione degli input porta ancora ad un riultato positivo
class SimGate():
    def __init__(self, gate = None, inputs = None, timer = None):
        self.gate:BasicGate = gate
        self.timer:int = timer
        self.original_inputs:list[bool] = inputs

    def __str__(self):
        return f"{self.gate.name} | timer: {self.timer} | og inputs: {self.original_inputs}"

gate_to_SimGate_dict:dict[AbstractGate, SimGate] = {}

#todo NON GLOBAL_ALL_BASIC_GATES_LIST ma GLOBAL_ALL_GATES_LIST
def run_simulation(simulation_time:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):
    print("\nSIMULATION:")
    apply_SwitchGates_immediatly(considered_switches)
    print()
    gates_preparing_to_switch:set[SimGate] = set()
    
    
    all_basic_gates:set[BasicGate] = set()
    for logic_gate in considered_gates:
        all_basic_gates.update(logic_gate._get_all_internal_basic_gates())

    for logic_gate in all_basic_gates:
        sim_gate = SimGate(logic_gate)
        gate_to_SimGate_dict[logic_gate] = sim_gate #*all basic gates -> SimGate

        logic_gate_result:bool = logic_gate.compute_result(logic_gate.get_input_signals_value_list())#get result, set result a parte quando arriva a 0
        if(logic_gate.get_output_signal_value() != logic_gate_result):
            gates_preparing_to_switch.add(sim_gate)
            sim_gate.original_inputs = logic_gate.get_input_signals_value_list()
            if(logic_gate_result):
                sim_gate.timer = logic_gate.low_to_high_timer
            else:
                sim_gate.timer = logic_gate.high_to_low_timer

    for second in range(simulation_time):
        print(f"current second: {second}")
        for sim_gate in gates_preparing_to_switch:
            sim_gate.timer -= 1

        sim_gates_to_add:set[SimGate] = set()
        sim_gates_to_remove:set[SimGate] = set()

        for sim_gate in gates_preparing_to_switch:
            if(sim_gate.timer == 0):#* TIMER == 0
                sim_gate.gate.set_output_signal(not sim_gate.gate.get_output_signal_value())
                sim_gate.gate.set_child_gates_input_signals()#sia ModuleGate che BasicGate
                print(f"GATE SWITCHED: {sim_gate.gate}")
                sim_gates_to_remove.add(sim_gate)
                
                child_basic_gates:set[BasicGate] = set()
                for child_gate, child_gate_input_ix in sim_gate.gate.get_all_child_gates():
                    if(child_gate in considered_gates):#se un gate NON incluso è figlio di un gate incluso
                        child_basic_gates.update(child_gate.get_all_basic_gates_connected_to_input_signal(child_gate_input_ix))

                for child_logic_gate in child_basic_gates:#* ITERA SU TUTTI I FIGLI DEL GATE CHE è APPENA COMMUATO
                    child_sim_gate = gate_to_SimGate_dict[child_logic_gate]

                    if child_sim_gate in gates_preparing_to_switch:
                        stable_input_signals_AND:list[bool] = []
                        stable_input_signals_OR:list[bool] = []
                        for ix in range(len(child_sim_gate.original_inputs)):
                            stable_input_signals_AND.append(child_sim_gate.original_inputs[ix] and child_sim_gate.gate.get_input_signal_value(ix))
                            stable_input_signals_OR.append(child_sim_gate.original_inputs[ix] or child_sim_gate.gate.get_input_signal_value(ix))
                        old_output_value:bool = child_sim_gate.gate.get_output_signal_value() 
                        if child_sim_gate.timer >0 and (child_sim_gate.gate.compute_result(stable_input_signals_AND) == old_output_value or child_sim_gate.gate.compute_result(stable_input_signals_OR) == old_output_value):
                            sim_gates_to_remove.add(child_sim_gate)
                    
                    child_logic_gate_result:bool = child_logic_gate.compute_result(child_logic_gate.get_input_signals_value_list())
                    if(child_logic_gate.get_output_signal_value() != child_logic_gate_result):
                        if(child_logic_gate_result):
                            child_sim_gate.timer = child_logic_gate.low_to_high_timer
                        else:
                            child_sim_gate.timer = child_logic_gate.high_to_low_timer
                        #print(f"child_sim_gate: {child_sim_gate}")
                        child_sim_gate.original_inputs = child_logic_gate.get_input_signals_value_list()
                        sim_gates_to_add.add(child_sim_gate)
                    else:
                        if(child_sim_gate in sim_gates_to_add):
                            sim_gates_to_add.remove(child_sim_gate)


        
        for sim_gate in sim_gates_to_remove:
            if(sim_gate.timer == 0):
                print(f"FINISHED, REMOVED: {sim_gate}")
            else:
                print(f"INTERRUPTED, REMOVED: {sim_gate}")    

        gates_preparing_to_switch.difference_update(sim_gates_to_remove)
        #l'ordine importa, può togliere e riaggiungere subito un gate che ha appena switchato
        for sim_gate in sim_gates_to_add:
            if(sim_gate not in gates_preparing_to_switch):
                gates_preparing_to_switch.add(sim_gate)
                print(f"ADDED: {sim_gate}")

        sim_gates_to_remove.clear()
        sim_gates_to_add.clear()

not1 = NOT(name="not1", high_to_low_timer=2, low_to_high_timer=2)
not2 = NOT((not1,0), name="not2", high_to_low_timer=15, low_to_high_timer=4)
#prova:ModuleGate = ModuleGate([not1,not2], 1, 1)
#prova.set_module_gate_input_signal_to_internal_gate_input_signal((not1,0),0)
#prova.set_module_gate_output_signal_to_internal_gate_output_signal((not2,0),0)
#prova.connect_multiple_input_gates_to_input_signals([(switch1,0),(switch2,0)])

and1 = AND([(switch1, 0), (not2, 0)], name="and1")

#run_simulation(simulation_time=30, considered_gates=[prova])
run_simulation(simulation_time=30, considered_gates=[not1, not2])

                                    






