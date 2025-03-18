from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from reti_logiche import *

def run_simulation(max_iterations:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_BASIC_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):
    apply_SwitchGates_immediatly(considered_switches)

    #gates_preparing_to_switch
    gates_preparing_to_switch:set[tuple[LogicClass,int]] = set()
    gates_preparing_to_switch_countdown_dict:dict[LogicClass, int] = {}
    switching_to_value_dict:dict[LogicClass, bool] = {}
    
    for gate in considered_gates:
        gate_result:bool = gate.get_future_output_signal_value()#get result, set result a parte quando arriva a 0
        if(gate.get_output_signal_value() != gate_result):
            gates_preparing_to_switch(gate)
            if(gate_result):
                gates_preparing_to_switch_countdown_dict[gate] = gate.low_to_high_timer
                switching_to_value_dict[gate] = True
            else:
                gates_preparing_to_switch_countdown_dict[gate] = gate.high_to_low_timer
                switching_to_value_dict[gate] = False

    for _ in range(max_iterations):
        for gate in gates_preparing_to_switch:
            gates_preparing_to_switch_countdown_dict[gate] -=1
        


        #* child gates to remove after after second, 
        #* child gates to add after second
        for gate in gates_preparing_to_switch.copy():
            if(gates_preparing_to_switch_countdown_dict[gate] ==0):
                gate.set_result(switching_to_value_dict[gate])
                child_gates:set[tuple[LogicClass, int]] = gate.get_all_child_gates()#?returns also input ix?? si
                for child_gate, child_gate_input_ix in child_gates:
                    child_gate.get_all_input_signals()
                    if child_gate in gates_preparing_to_switch:
                        if(gates_preparing_to_switch_countdown_dict[gate] != 0):#gate non ha finito
                            if(child_gate.get_future_output_signal_value() != switching_to_value_dict[gate]):
                                gates_preparing_to_switch.remove(gate) #dopo il for

                        else:#gate ha appena finito
                            if(child_gate.get_future_output_signal_value() != switching_to_value_dict[gate]):
                                gates_preparing_to_switch.add(child_gate)
                                switching_to_value_dict[child_gate] = child_gate.get_future_output_signal_value()
                                if(switching_to_value_dict[child_gate] == True):
                                    gates_preparing_to_switch_countdown_dict[child_gate] = child_gate.low_to_high
                                else:
                                    gates_preparing_to_switch_countdown_dict[child_gate] = child_gate.high_to_low
        
            gates_preparing_to_switch.remove(gate)
            del gates_preparing_to_switch_countdown_dict[gate]
            del switching_to_value_dict[gate]


                            


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
                                    






