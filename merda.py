def add_input_ports(self, input_ports_param:list[AbstractPort]):
        #!se ci sono più porte di input che input_signals, aggiunge input_signals
        #len_input_ports_dict:int = len(self.input_ports_dict)#indcice del primo input_signal non pilotato
        number_of_unconnected_input_signals:int = self.number_of_inputs - self.number_of_piloted_input_signals
        number_of_extra_input_ports:int = len(input_ports_param) - number_of_unconnected_input_signals
        self.number_of_inputs += max(0, number_of_extra_input_ports)#se passi meno porte di input di quelle necessarie

        
        for input_port in input_ports_param:
            input_port.add_child_port(self)
            self.input_ports_dict[number_of_unconnected_input_signals] = input_port
            number_of_unconnected_input_signals += 1

    def connect_multiple_input_signals_to_input_ports(self, input_ports_param: list[AbstractPort]):
        #!connette le input ports SOLO alle porte già presenti

        #first unpiloated input_signal index
        if(self.number_of_piloted_input_signals + len(input_ports_param) > self.number_of_inputs):
            raise ValueError("ERRORE: porte di input in eccesso, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        if(self.number_of_piloted_input_signals + len(input_ports_param) < self.number_of_inputs):
            print("WARNING: porte di input insufficienti, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        
        param_ix:int =0
        input_signal_ix:int =0
        while(param_ix < len(input_ports_param) and input_signal_ix < self.get_number_of_inputs()):
            if self.input_ports_dict.get(input_signal_ix) == None:
                self.input_ports_dict[input_signal_ix] = input_ports_param[param_ix]
                param_ix +=1
            input_signal_ix +=1


    def connect_input_signal_to_input_port(self, input_port: AbstractPort, input_signal_ix: int):
        if input_signal_ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(input_signal_ix) + " last index: " + (str(self.number_of_inputs)-1))
        self.input_ports_dict[input_signal_ix] = input_port
        input_port.add_child_port(self)



    def connect_multiple_input_signals_to_input_ports(self, input_ports_param: list[AbstractPort]):
        #!connette le input ports SOLO alle porte già presenti
        #first unpiloated input_signal index
        if(self.number_of_piloted_input_signals + len(input_ports_param) > self.number_of_inputs):
            raise ValueError("ERRORE: porte di input in eccesso, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        if(self.number_of_piloted_input_signals + len(input_ports_param) < self.number_of_inputs):
            print("WARNING: porte di input insufficienti, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        
        for p in input_ports_param:
            self.input_ports_dict[self.number_of_piloted_input_signals] = p
            self.number_of_piloted_input_signals +=1


////////////////////////////////

and1 = AND([switch1, switch1], 2, "and1")
not1 = NOT(and1)
or1 = OR([], 2, "OR1")
#esegui_rete_logica()

print("/////////////////////////////////7")

'''#*and1 non ha più input gate libera
or2 = OR([], 2, "OR1")
and1.connect_input_signal_to_input_gate(or2, 1)
'''
mod:ModuleGate = ModuleGate([and1,not1,or1])
#*and1 non ha più input gate libera
or2 = OR([], 2, "OR1")
mod.connect_input_signal_to_input_gate(or2, 0)

mod1:ModuleGate = ModuleGate([mod, or2])

print(mod.input_gates_dict)
print("get_number_of_unpiloted_input_signals: " + str(mod.get_number_of_unpiloted_input_signals()))
print("number_of_inputs: " + str(mod.number_of_inputs))
print(mod1.input_gates_dict)
print("get_number_of_unpiloted_input_signals: " + str(mod1.get_number_of_unpiloted_input_signals()))
print("number_of_inputs: " + str(mod1.number_of_inputs))

mod1.print_input_signal_status()

print(mod1.get_all_internal_BasicGates())

#!////////////////////////////////////

#!funziona solo con BASIC GATE
def run_simulation(max_iterations:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):#se non passo la rete logica, eseguo tutte le gates
    apply_SwitchGates_immediatly(considered_switches)

    current_level_gates:set[AbstractGate] = set()
    next_level_gates:set[AbstractGate] = set()
    current_level_gates.update(considered_gates)
    #print(considered_gates)

    current_level_gates_copy = current_level_gates.copy()#!ERRATO lista di funzioni per i pin che devono essere cambiati a fine turno
    #^^^Copy needed because first he computes results for all current level gates 
    #then it sets the input signals to the children of current level gates
    level:int = 0
    iterations:int = 0  
    print("LEVEL: ", level)

    while len(current_level_gates) >0 and iterations < max_iterations:
        iterations += 1
        current_gate:BasicGate = current_level_gates.pop()
        current_gate.compute_result()
        if(current_gate.has_output_signal_changed):
            next_level_gates.update(current_gate.child_gates_set)
            #! add (A,0) set input signal di A,0
        print(current_gate)

        if len(current_level_gates) == 0:
            level += 1
            if(len(next_level_gates) > 0):
                print("LEVEL: ", level)
            current_level_gates = next_level_gates.copy()
            next_level_gates.clear()
            while len(current_level_gates_copy) > 0:
                current_gate = current_level_gates_copy.pop()
                current_gate.input_gates_results_set_input_signals()

switch1 = SwitchGate()
switch2 = SwitchGate()

and1:AND = AND()
xor1:XOR = XOR()
print("and1.number_of_inputs: " + str(and1.number_of_inputs))
half_adder:ModuleGate = ModuleGate([xor1, and1], name="halfadder", number_of_inputs=2, number_of_outputs=2)
half_adder.set_input_signal_to_flg_input_signal(0, and1, 0)
half_adder.set_input_signal_to_flg_input_signal(0, xor1, 0)
half_adder.set_input_signal_to_flg_input_signal(1, and1, 1)
half_adder.set_input_signal_to_flg_input_signal(1, xor1, 1)

half_adder.set_output_signal_to_llg_output_signal(0, and1, 0)
half_adder.set_output_signal_to_llg_output_signal(1, xor1, 0)

half_adder.connect_multiple_input_gates_to_input_signals([switch1, switch2])
half_adder.print_all_input_signals_status()
half_adder.print_all_output_signals_status()

or1 = OR(input_gates_list=[half_adder.get_output_gate(0), half_adder.get_output_gate(1)])
sim_gates= []
sim_gates.extend(half_adder.get_all_internal_BasicGates())
sim_gates.extend(or1.get_all_internal_BasicGates())
print(sim_gates)

run_simulation(considered_gates=sim_gates)
