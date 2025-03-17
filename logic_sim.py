from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from reti_logiche import *

def run_simulation(max_iterations:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):
    apply_SwitchGates_immediatly(considered_switches)

    #gates_preparing_to_switch
    gates_preparing_to_execute:set[tuple[LogicClass,int]] = set()
    gates_preparing_to_execute_countdown_dict:dict[LogicClass, int] = {}
    
    for gate in considered_gates:
        gate_result:bool = gate.compute_result()#get result, set result a parte quando arriva a 0
        if(gate.output_signal != gate_result):
            gates_preparing_to_execute.add(gate)
            if(gate_result):
                gates_preparing_to_execute_countdown_dict[gate] = gate.PLH_delay
            else:
                gates_preparing_to_execute_countdown_dict[gate] = gate.PHL_delay

    for _ in range(max_iterations):
        for gate in gates_preparing_to_execute:
            gates_preparing_to_execute_countdown_dict[gate] -=1
        
        for gate in gates_preparing_to_execute:
            if(gates_preparing_to_execute_countdown_dict[gate] ==0):
                child_gates:set[tuple[LogicClass, int]] = gate.get_child_gates()#?returns also input ix?? dovrebbe
                for child_gate, child_gate_input_ix in child_gates:
                    #child_gate.prendi_input_signal()
                    if(child_gate in gates_preparing_to_execute time!=0 and compute_result != result):#cambierebbe con child_gate? se si #se è in preparing to excute e cambia un altra volta torna al valore precedente
                        # è già a 0? -> propaghi
                        # è diverso da 0 -> elimini
                        remove child_gate from gates_preaparing_to_execute


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
                                    






