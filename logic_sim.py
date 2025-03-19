from reti_logiche import *

def apply_SwitchGates_immediatly(considered_switches):
    for switch in considered_switches:
        switch.set_child_gates_input_signals()
        for gate, gate_input_ix in switch.get_all_child_gates():
            print(f"Gate: {gate.name} input: {gate_input_ix} > set to {switch.get_output_signal_value()}")
        

#todo NON GLOBAL_ALL_BASIC_GATES_LIST ma GLOBAL_ALL_GATES_LIST
def run_simulation(simulation_time:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):
    print("\nSIMULATION:")
    apply_SwitchGates_immediatly(considered_switches)
    print()
    gates_preparing_to_switch:set[LogicClass] = set()
    gates_timer:dict[LogicClass, int] = {}
    
    all_basic_gates:set[BasicGate] = set()
    for gate in considered_gates:
        all_basic_gates.update(gate._get_all_internal_basic_gates())

    for gate in all_basic_gates:
        gate_result:bool = gate.get_future_output_signal_value()#get result, set result a parte quando arriva a 0
        if(gate.get_output_signal_value() != gate_result):
            gates_preparing_to_switch.add(gate)
            if(gate_result):
                gates_timer[gate] = gate.low_to_high_timer
            else:
                gates_timer[gate] = gate.high_to_low_timer

    for second in range(simulation_time):
        print(f"current second: {second}")
        for gate in gates_preparing_to_switch:
            gates_timer[gate] -=1

        gates_to_add:set[LogicClass] = set()
        gates_to_remove:set[LogicClass] = set()
        for gate in gates_preparing_to_switch:
            if(gates_timer[gate] == 0):#* TIMER == 0
                gate.set_output_signal(not gate.get_output_signal_value())
                gate.set_child_gates_input_signals()#sia ModuleGate che BasicGate
                print(f"GATE SWITCHED: {gate}")
                if(gate.get_output_signal_value() == gate.get_future_output_signal_value()):
                    gates_to_remove.add(gate)
                else:
                    #se A -> B e entrambi switchano al secondo 0, B switcha comunque(perchè ha finito il countdown)
                    #ma ricomincia il countdown per ri switchare dato il cambiamento di input
                    if(gate.get_future_output_signal_value()):
                        gates_timer[gate] = gate.low_to_high_timer
                        print(f"ADDED GATE == 0: {child_gate.name}, timer: {child_gate.low_to_high_timer}, switching to: 1")
                    else:
                        gates_timer[gate] = gate.high_to_low_timer
                        print(f"ADDED GATE == 0: {child_gate.name}, timer: {child_gate.high_to_low_timer}, switching to: 0")
                
                child_basic_gates:set[BasicGate] = set()
                for child_gate, child_gate_input_ix in gate.get_all_child_gates():
                    child_basic_gates.update(child_gate.get_all_basic_gates_connected_to_input_signal(child_gate_input_ix))

                for child_gate in child_basic_gates:#* ITERA SU TUTTI I FIGLI DEL GATE CHE è APPENA COMMUATO
                    if(child_gate not in gates_preparing_to_switch or  gates_timer[gate] >0):#* AGGIUNGE UN NUOVO GATE CHE DOVRA' COMMUTARE
                        #print(f"child_gate {child_gate}, future signal: {child_gate.get_future_output_signal_value()}")
                        #print(f"not2: {not2.get_output_signal_value()}, {switch1.get_output_signal_value()}")#?????? T T
                        if child_gate.get_output_signal_value() == child_gate.get_future_output_signal_value():
                            if(child_gate in gates_to_add) : gates_to_add.remove(child_gate)
                        else:
                            gates_to_add.add(child_gate)
                            if(child_gate.get_future_output_signal_value()):
                                gates_timer[child_gate] = child_gate.low_to_high_timer
                                print(f"ADDED NEW GATE: {child_gate.name}, timer: {child_gate.low_to_high_timer}, switching to: 1")
                            else:
                                gates_timer[child_gate] = child_gate.high_to_low_timer
                                print(f"ADDED NEW GATE: {child_gate.name}, timer: {child_gate.high_to_low_timer}, switching to: 0")

                    else:#* RIMUOVE UN GATE CHE è INTERROTTO
                        if(not gates_timer[child_gate] == 0 and child_gate.get_output_signal_value() == child_gate.get_future_output_signal_value()):
                            gates_to_remove.add(child_gate)
                            
        gates_preparing_to_switch.difference_update(gates_to_remove)
        #l'ordine importa, può togliere e riaggiungere subito un gate che ha appena switchato
        gates_preparing_to_switch.update(gates_to_add)
        gates_to_remove.clear()
        gates_to_add.clear()

not1 = NOT(name="not1", high_to_low_timer=2, low_to_high_timer=2)
not2 = NOT((not1,0), name="not2", high_to_low_timer=15, low_to_high_timer=2)
and1 = AND([(switch1, 0), (not2, 0)], name="and1")


run_simulation(simulation_time=30, considered_gates=[not1,not2,and1])

                                    






