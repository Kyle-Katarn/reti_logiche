from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from reti_logiche import *

def run_simulation(max_iterations:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):
    apply_SwitchGates_immediatly(considered_switches)

    #gates_preparing_to_switch
    gates_preparing_to_switch:set[LogicClass] = set()
    gates_timer:dict[LogicClass, int] = {}
    
    for gate in considered_gates:
        gate_result:bool = gate.get_future_output_signal_value()#get result, set result a parte quando arriva a 0
        if(gate.get_output_signal_value() != gate_result):
            gates_preparing_to_switch(gate)
            if(gate_result):
                gates_timer[gate] = gate.low_to_high_timer
            else:
                gates_timer[gate] = gate.high_to_low_timer

    for _ in range(max_iterations):
        for gate in gates_preparing_to_switch:
            gates_timer[gate] -=1

        gates_to_add:set[LogicClass] = set()
        gates_to_remove:set[LogicClass] = set()
        for gate in gates_preparing_to_switch:
            if(gates_timer(gate) == 0):
                gate.set_output_signal(not gate.get_output_signal_value())
                gate.set_child_gates_input_signals()
                if(gate.get_output_signal_value() == child_gate.get_future_output_signal_value()):
                    gates_to_remove.add(gate)
                else:
                    #se A -> B e entrambi switchano al secondo 0, B switcha comunque(perchè ha finito il countdown)
                    #ma ricomincia il countdown per ri switchare dato il cambiamento di input
                    if(gate.get_output_signal_value()):
                        gates_timer[gate] = gate.low_to_high_timer
                    else:
                        gates_timer[gate] = gate.high_to_low_timer
                
                for child_gate, child_gate_input_ix in gate.get_all_child_gates():
                    if(child_gate not in gates_preparing_to_switch):
                        if child_gate.get_output_signal_value() == child_gate.get_future_output_signal_value():
                            if(child_gate in gates_to_add) : gates_to_add.remove(child_gate)
                        else:
                            gates_to_add.add(child_gate)
                            if(child_gate.get_output_signal_value()):
                                gates_timer[child_gate] = child_gate.low_to_high_timer
                            else:
                                gates_timer[child_gate] = child_gate.high_to_low_timer

                    else:# child_gate in gates_preparing_to_switch
                        if(not gates_timer(child_gate) == 0 and child_gate.get_output_signal_value() == child_gate.get_future_output_signal_value()):
                            gates_to_remove.add(child_gate)
                            
        gates_preparing_to_switch.difference_update(gates_to_remove)
        gates_preparing_to_switch.update(gates_to_add)
        gates_to_remove.clear()
        gates_to_add.clear()


                            


                        # switch_dict{} Gate-> value to switch to

                        #gate.set_result(switch_dict{gate}) #! * B cambierebbe valore, errore: mi serve di ricordarmmi per che valore sono entrati?
                        #child_gate.get_input_signals() 
                        #if child gate in gates_preapring_to_switch:
                            #if(child_gate.timer != 0):
                                #(child_gate.compute_result() != switch_dict{child_gate}):
                                    #gates_preparing_to_switch.remove(child_gate)
                            #else:
                                #if(child_gate.compute_result() != switch_dict{child_gate}):#es: 0 -> 1 -> 0 #! *
                                    #gate_preparing_to_switch.add(child_gate)
                                    #switch_dict[child_gate] = child_gate.compute_result #*non posso vare la stessa key, mi serve un nuovo dict
                                    #if(switch_dict[child_gate] == 0):
                                        #timer_dict[child_gate] = ..... #*non posso vare la stessa key, mi serve un nuovo dict
                                    #else:
                                        ##timer_dict[child_gate] = ..... #*non posso vare la stessa key, mi serve un nuovo dict
                                #else:
                                    #niente il valore è stabile
                                    






