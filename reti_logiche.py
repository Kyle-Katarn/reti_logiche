from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_GATES_LIST:list['AbstractGate'] = []
GLOBAL_ALL_SWITCHES_LIST:list['AbstractGate'] = []

class LogicClass:
    '''
    Nome, numero di segnali in ingresso
    '''
    def __init__(self, name: str = "LogicClass"):
        self.name: str = name
        self.number_of_inputs:int = 0
        self.number_of_outputs:int = 0

    def __str__(self):
        return "Name: "+ self.name

    def get_name(self):
        return self.name





class SwitchGate(LogicClass):
    def __init__(self, inital_value:bool =True, name: str = "SwitchGate"):
        super().__init__(name)
        self.number_of_outputs = 1
        self.output_signal: bool = False
        GLOBAL_ALL_SWITCHES_LIST.append(self)
        self.output_signal = inital_value
        self.child_gates_set: set['AbstractGate'] = set()
    
    def toggle(self):
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = True
    
    def add_child_gate(self, child_gate:'AbstractGate'):
        self.child_gates_set.add(child_gate)
    
    def get_child_gates(self):
        return self.child_gates_set

    def print_child_gates(self):
        print("Child gates of(", self, "): ")
        for c in self.child_gates_set:
            print(c)
        print("")


class AbstractGate(LogicClass):
    def __init__(self, name: str = "AbstractGate"):
        super().__init__(name)
        self.input_gates_dict = {}

    def connect_multiple_input_gates_to_input_signals(self, input_gates_param: list["AbstractGate"]):
        pass

    def connect_input_gate_to_input_signal(self, input_gate: "AbstractGate", input_signal_ix: int):
        pass

    def print_input_signal_status(self):
        pass

    def print_output_signal_status(self):
        pass

    def get_number_of_unpiloted_input_signals(self):
        pass

    def is_input_signal_piloted(self, ix:int):
        pass

    def reset_all_signals(self):
        pass

    def _get_imput_signal_status(self, ix):
        pass

    def get_all_internal_BasicGates(self):
        pass

    def get_output_gate(self, ix):
        pass


    
class ModuleGate(AbstractGate):
    def __init__(self, internal_gates:list[AbstractGate] = [], number_of_inputs:int =0, number_of_outputs:int =0, name = "AbstractGate"):
        super().__init__(name)
        self.input_gates_dict: Dict[int, list[tuple[AbstractGate, int]]] = {}
        self.input_gates_names_dict:dict[int, str] = {}
        self.internal_gates:list[AbstractGate] = internal_gates
        self.number_of_inputs = number_of_inputs

        self.number_of_outputs = number_of_outputs
        self.output_gates_dict: Dict[int, tuple[AbstractGate, int]] = {}
        self.output_gates_names_dict:dict[int, str] = {}
        
    def set_input_signal_to_flg_input_signal(self, self_ix:int, first_layer_gate:AbstractGate, flg_ix:int, name:str = '/'):
        self.input_gates_names_dict[self_ix] = name
        if(self.input_gates_dict.get(self_ix) == None):
            self.input_gates_dict[self_ix] = []
        self.input_gates_dict[self_ix].append((first_layer_gate, flg_ix))

    def set_input_signals_automatically(self):
        first_layer_gates:list[AbstractGate] = []#gates with 1 or more unpiloted input signals #!spostalo
        for ip in self.internal_gates:
            print(ip.name + "  "+ str(ip.get_number_of_unpiloted_input_signals()))
            if(ip.get_number_of_unpiloted_input_signals() != 0):
                first_layer_gates.append(ip)
        #i segnali di input di module gate = Unione di tutti i segnali di input di first layer gate
        self.number_of_inputs =0 #viene calcolato in automatico
        self.input_gates_dict.clear() #viene calcolato in automatico
        for flg in self.first_layer_gates:
            for flg_input_gate_ix in range(flg.number_of_inputs):  # Fixed iteration
                if(not flg.is_input_signal_piloted(flg_input_gate_ix)):
                    self.set_input_signal_to_flg_input_signal(self.number_of_inputs, flg, flg_input_gate_ix)
                    self.number_of_inputs += 1

    def connect_input_gate_to_input_signal(self, gate_param:AbstractGate, ix:int =0):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs-1)))
        for tup in self.input_gates_dict.get(ix):
            flg, internal_ix = tup
            flg.connect_input_gate_to_input_signal(gate_param, internal_ix)
      
    def connect_multiple_input_gates_to_input_signals(self, gates_param:list[AbstractGate], first_ix:int =0):
        if(first_ix+len(gates_param) > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your last index: " + str(first_ix+len(gates_param)) + " last index: " + (str(self.number_of_inputs-1)))
        for ip in gates_param:
            self.connect_input_gate_to_input_signal(ip, first_ix)
            first_ix +=1

    def set_output_signal_to_llg_output_signal(self, self_ix:int, last_layer_gate:AbstractGate, flg_ix:int, name:str = '/'):
        self.output_gates_names_dict[self_ix] = name
        self.output_gates_dict[self_ix] = (last_layer_gate, flg_ix)
        print(self.output_gates_dict.get(self_ix))

    def set_output_signals_automatically(self):
        pass

    def get_output_gate(self, ix):
        if(ix > self.number_of_outputs):
            raise IndexError("ERRORE: Output gate of range, your index: " + str(ix) + " last index: " + str(self.number_of_inputs)-1)
        output_gate, output_gate_ix = self.output_gates_dict.get(ix)
        return output_gate.get_output_gate(output_gate_ix)

    def get_number_of_unpiloted_input_signals(self):
        sum:int =0
        for flg in self.internal_gates:
            sum+= flg.get_number_of_unpiloted_input_signals() #get_number_of_unpiloted_input_signals ha senso solo su BasicGate
        return sum

    def is_input_signal_piloted(self, ix:int):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        #is_input_signal_piloted ha senso solo su BasicGate
        internal_gate, internal_ix = self.input_gates_dict.get(ix)[0] #se il primo è pilotato
        return internal_gate.is_input_signal_piloted(internal_ix)
    
    def reset_all_signals(self):
        for g in self.internal_gates:
            g.reset_all_signals()
    
    def print_input_signal_status(self, input_signal_ix:int, lvl:int): 
        nome_segnale: str = self.input_gates_names_dict.get(input_signal_ix)
        if nome_segnale is None:
            nome_segnale = "/"
        before:str=""
        for i in range(lvl):
            before += " >"
        if(lvl == 0):
            before += "O"
        print(before+" Signal name: " + nome_segnale + " |IX: " + str(input_signal_ix) + " of " + self.name)
        for internal_gate, internal_ix in self.input_gates_dict.get(input_signal_ix):
            internal_gate.print_input_signal_status(internal_ix, lvl+1)

    def print_all_input_signals_status(self): 
        print("@ INPUT SIGNALS - Traccia di tutti i segnali interni collegati, l'ultimo e' di una BasicPort:")
        for input_signal_ix in range(self.number_of_inputs):
            self.print_input_signal_status(input_signal_ix, 0)
            print("----------------")

    def print_output_signal_status(self, output_signal_ix:int, lvl:int): #!fixa 
        nome_segnale: str = self.input_gates_names_dict.get(output_signal_ix)
        if nome_segnale is None:
            nome_segnale = "/"
        before:str=""
        for i in range(lvl):
            before += " >"
        if(lvl == 0):
            before += "O"
        print(before+ " Signal name: " + nome_segnale + " |IX: " + str(output_signal_ix) + " of " + self.name)
        internal_gate, internal_ix = self.output_gates_dict.get(output_signal_ix)
        internal_gate.print_output_signal_status(internal_ix, lvl+1)

    def print_all_output_signals_status(self): 
        print("@ OUTPUT SIGNALS - Traccia di tutti i segnali interni collegati, l'ultimo e' di una BasicPort:")
        for output_signal_ix in range(self.number_of_inputs):
            self.print_output_signal_status(output_signal_ix, 0)
            print("----------------")

    def get_all_internal_BasicGates(self):
        ris:list[BasicGate] = []
        for ig in self.internal_gates:
            ris.extend(ig.get_all_internal_BasicGates())
        return ris
        



class BasicGate(AbstractGate):
    def __init__(self, input_gates_list:list['AbstractGate'], number_of_inputs:int = 2, name:str = "GateWithInput"):
        super().__init__(name)
        GLOBAL_ALL_GATES_LIST.append(self)
        self.input_gates_dict:dict[int, AbstractGate] = {} #la gate e l'indice del imput_signal che pilota
        self.input_signals_list:list[bool] = []

        self.output_signal: bool = False
        self.has_oputput_signal_changed: bool = False
        self.child_gates_set: set['AbstractGate'] = set()

        for _ in range(number_of_inputs): #inizializza la lista degli input_signals
            self.input_signals_list.append(False)
        self.number_of_inputs:int = number_of_inputs

        self.connect_multiple_input_gates_to_input_signals(input_gates_list)

    def connect_multiple_input_gates_to_input_signals(self, input_gates_param:list[AbstractGate], first_ix:int =0):
        #!se ci sono più gates di input che input_signals, aggiunge input_signals
        if(first_ix+len(input_gates_param) > self.number_of_inputs):
            n:int = first_ix+len(input_gates_param) - self.number_of_inputs
            print("WARNING: added "+ str(n) + " input gates")
            self.number_of_inputs += n
            
        for input_gate in input_gates_param:
            input_gate.add_child_gate(self)
            self.input_gates_dict[first_ix] = input_gate
            self.input_signals_list.append(False)
            first_ix +=1

    def connect_input_gate_to_input_signal(self, input_gate: AbstractGate, ix:int):
        if ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        self.input_gates_dict[ix] = input_gate
        input_gate.add_child_gate(self)

    def get_number_of_unpiloted_input_signals(self):
        return self.number_of_inputs - len(self.input_gates_dict)

    def is_input_signal_piloted(self, ix:int):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        return self.input_gates_dict.get(ix) != None

    def add_child_gate(self, child_gate:AbstractGate):
        self.child_gates_set.add(child_gate)

    def compute_result(self):
        pass

    def input_gates_results_set_input_signals(self):
        for ix in range(self.number_of_inputs):
            pilot_gate:AbstractGate = self.input_gates_dict.get(ix)
            if(pilot_gate != None):
                self.input_signals_list[ix] = pilot_gate.output_signal

    def has_output_signal_changed(self):#da chiamare dopo compute_result
        return self.has_oputput_signal_changed

    def __str__(self):
        return super().__str__() + " -> " + str(self.output_signal)
 
    def get_input_gates_dict(self):
        return self.input_gates_dict

    def get_child_gates_set(self):
        return self.child_gates_set

    def reset_all_signals(self):
        for ix in range(len(self.input_signals_list)):
            self.input_signals_list[ix] = False
        self.output_signal = False
        self.has_oputput_signal_changed = False
    
    def print_input_signal_status(self, input_signal_ix:int, lvl:int): 
        pilot_gate:AbstractGate = self.input_gates_dict.get(input_signal_ix)
        pilot_gate_info:str = "/"
        if(pilot_gate != None):
            pilot_gate_info = pilot_gate.name
        before:str = ""
        for i in range(lvl):
            before += " >"
        if(lvl == 0):
            before += "O"
        print(before+ " Signal IX: "+str(input_signal_ix)+" of "+self.name+" |PILOT_GATE: " +str(pilot_gate_info)  +" |----------------| STATUS: "+ str(self.input_signals_list[input_signal_ix]))

    def print_all_input_signals_status(self): 
        print("@ Traccia di tutti i segnali interni collegati, l'ultimo e' di una BasicPort:")
        for input_signal_ix in range(self.number_of_inputs):
            self.print_input_signal_status(input_signal_ix, 0)
            print("----------------")

    def print_output_signal_status(self, output_signal_ix:int, lvl:int): 
        before:str=""
        for i in range(lvl):
            before += " >"
        if(lvl == 0):
            before += "O"
        print(before+ " Signal IX: "+str(output_signal_ix)+" of "+self.name + " |----------------| STATUS: "+ str(self.input_signals_list[output_signal_ix]))
        if(len(self.child_gates_set) >0):
            print("CHILD GATES: ")
            for g in self.child_gates_set:
                print(" -> "+ str(g))

    def print_all_output_signals_status(self): 
        print("@ OUTPUT SIGNALS - Traccia di tutti i segnali interni collegati, l'ultimo e' di una BasicPort:")
        for input_signal_ix in range(self.number_of_inputs):
            self.print_output_signal_status(input_signal_ix, 0)
            print("----------------")

    def get_all_internal_BasicGates(self):
        return [self]
    
    def get_output_gate(self, ix):
        return self



class AND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "AND"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        print("old_output_signal: "+ str(old_output_signal))
        self.output_signal = True
        for value in self.input_signals_list:
            self.output_signal = self.output_signal and value
        self.has_oputput_signal_changed = old_output_signal != self.output_signal


class OR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "OR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = False
        for value in self.input_signals_list:
            self.output_signal = self.output_signal or value
        self.has_oputput_signal_changed = old_output_signal != self.output_signal


class NAND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NAND"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = True
        for value in self.input_signals_list:
            self.output_signal = self.output_signal and value
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = old_output_signal != self.output_signal

class NOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NOR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = False
        for value in self.input_signals_list:
            self.output_signal = self.output_signal or value
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = old_output_signal != self.output_signal

class NOT(BasicGate):
    def __init__(self, input_gate:AbstractGate = None, name: str = "NOT"):
        super().__init__([], 1, name)
        self.add_input_gate(input_gate)

    def add_input_gate(self, input_gate_param:AbstractGate):
        if(self.get_input_gates_dict().get(0) == None):
            self.get_input_gates_dict()[0] = input_gate_param
            input_gate_param.add_child_gate(self)
        else:
            print("WARNING: La gate NOT accetta SOLO 1 segnale in input - Operazione annullata")

        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = not self.input_signals_list[0]
        self.has_oputput_signal_changed = old_output_signal != self.output_signal

class XOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "XOR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = False
        number_of_true_inputs = sum(1 for value in self.input_signals_list if value)
        self.output_signal = (number_of_true_inputs % 2) == 1  # XOR is true when odd number of inputs are true
        self.has_oputput_signal_changed = old_output_signal != self.output_signal

#setti la gate in input ad un pin di B, A contiene B nella lista delle gates di output

def apply_SwitchGates_immediatly(considered_switches:list[AbstractGate]):
    for p in considered_switches:
        for f in p.child_gates_set:
            f.input_gates_results_set_input_signals()
                #applica prende i risultati di tutte le gates in input
                #*NON è un problema se il metodo è chiamato a fine turno ossia dopo aver chiamato set_input_signals su tutte currnet_level_gates. (è un problema altrimenti)


#!funziona solo con BASIC GATE
def run_simulation(max_iterations:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):#se non passo la rete logica, eseguo tutte le gates
    apply_SwitchGates_immediatly(considered_switches)

    current_level_gates:set[AbstractGate] = set()
    next_level_gates:set[AbstractGate] = set()
    current_level_gates.update(considered_gates)
    print(considered_gates)

    current_level_gates_copy = current_level_gates.copy()
    level:int = 0
    iterations:int = 0  
    print("LEVEL: ", level)

    while len(current_level_gates) >0 and iterations < max_iterations:
        iterations += 1
        current_gate:BasicGate = current_level_gates.pop()
        current_gate.compute_result()
        if(current_gate.has_output_signal_changed):
            next_level_gates.update(current_gate.get_child_gates_set())
        print(current_gate)

        if len(current_level_gates) == 0:
            level += 1
            if(len(next_level_gates) > 0):
                print("LEVEL: ", level)
            current_level_gates = next_level_gates.copy()
            next_level_gates.clear()
            while len(current_level_gates_copy) > 0:
                current_gate = current_level_gates_copy.pop()
                current_gate.input_gates_results_set_input_signals()  # Updated method call

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



