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
        self.child_gates_set: set[tuple['AbstractGate', int]] = set()
    
    def toggle(self):
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = True
    
    def add_child_gate(self, child_gate:'AbstractGate'):
        self.child_gates_set.add(child_gate)
    
    def get_output_signal(self, ix=0):
        return self.output_signal

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

    def get_all_internal_BasicGates(self):
        pass

    def get_output_gate(self, ix):
        pass

    def get_input_signal_status(self,ix):
        pass

    def get_output_signal_status(self,ix=0):
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
        for flg in first_layer_gates:
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

    def get_input_signal_status(self,ix):
        internal_gate, internal_ix = self.input_gates_dict.get(ix)[0] #sono tutti piloati dalla stesso BasicGate
        return internal_gate.get_input_signal_status(internal_ix)

    def set_output_signal_to_llg_output_signal(self, self_ix:int, last_layer_gate:AbstractGate, flg_ix:int=0, name:str = '/'):
        self.output_gates_names_dict[self_ix] = name
        self.output_gates_dict[self_ix] = (last_layer_gate, flg_ix)
        print(self.output_gates_dict.get(self_ix))

    def get_number_of_children(self):
        tot:int = 0
        for ig in self.internal_gates:
            sum += ig.get_number_of_children()

    def set_output_signals_automatically(self):
        last_layer_gates:list[AbstractGate] = []  # gates with no child gates
        for ip in self.internal_gates:
            if(ip.get_number_of_children() == 0):
                last_layer_gates.append(ip)
        # Set output signals based on last layer gates
        self.number_of_outputs = 0  # automatically calculated
        self.output_gates_dict.clear()  # automatically calculated
        for llg in last_layer_gates:
            for llg_output_ix in range(llg.number_of_outputs):
                self.set_output_signal_to_llg_output_signal(self.number_of_outputs, llg, llg_output_ix)
                self.number_of_outputs += 1

    def get_output_gate(self, ix):
        if(ix > self.number_of_outputs):
            raise IndexError("ERRORE: Output gate of range, your index: " + str(ix) + " last index: " + str(self.number_of_inputs)-1)
        output_gate, output_gate_ix = self.output_gates_dict.get(ix)
        return output_gate.get_output_gate(output_gate_ix)
    
    def get_all_child_gates(self):
        tot:set[BasicGate] = set()
        for ig in self.internal_gates:
            for cg in ig.get_all_child_gates():
                if(not cg in self.internal_gates):
                    tot.add(cg)
        return tot

    def get_output_signal_status(self, ix):
        internal_gate, internal_ix = self.output_gates_dict.get(ix)[0] #sono tutti piloati dalla stesso BasicGate
        return internal_gate.get_output_signal_status(internal_ix)

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

    def print_output_signal_status(self, output_signal_ix:int, lvl:int):
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
        

class SIGNAL():
    def __init__(self, val:bool = False):
        self.val = val

class BasicGate(AbstractGate):
    def __init__(self, input_gates_list:list['BasicGate'], number_of_inputs:int = 2, name:str = "GateWithInput"):
        super().__init__(name)
        GLOBAL_ALL_GATES_LIST.append(self)
        self.input_gates_dict:dict[int, tuple['BasicGate', int]] = {} #input gate e l'ix del segnale di output di input gate
        self.input_signals_list:list[SIGNAL] = []

        self.output_signal: SIGNAL = SIGNAL()  # Initialize as SIGNAL instance
        self.number_of_outputs:int = 1
        self.has_oputput_signal_changed: bool = False
        self.child_gates_set: set[tuple['BasicGate',int]] = set() #child gate e l'ix del segnale di input di child gate

        for _ in range(number_of_inputs): #inizializza la lista degli input_signals
            self.input_signals_list.append(SIGNAL())
        self.number_of_inputs:int = number_of_inputs

        self.connect_multiple_input_gates_to_input_signals(input_gates_list)

    def connect_multiple_input_gates_to_input_signals(self, param:list[tuple["AbstractGate",int]], first_ix:int =0):
        #!se ci sono più gates di input che input_signals, aggiunge input_signals
        n:int =0#numbers of signals to add
        if(first_ix+len(param) > self.number_of_inputs):
            n= first_ix+len(param) - self.number_of_inputs
            print("WARNING: added "+ str(n) + " input gates")
            self.number_of_inputs += n

        for j in range(n):#adds more signals if needed
            self.input_signals_list.append(SIGNAL())
            
        for input_gate, input_gate_signal_ix in param:
            input_gate.add_child_gate((self,first_ix)) #child gate = self, ix signal di input di childgate
            self.input_gates_dict[first_ix] = (input_gate,input_gate_signal_ix)
            first_ix +=1

    def connect_input_gate_to_input_signal(self, param: tuple[AbstractGate, int], ix:int):
        if ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        self.input_gates_dict[ix] = param
        input_gate, input_gate_signal_ix = param
        input_gate.add_child_gate(tuple[self,ix])

    def get_number_of_unpiloted_input_signals(self):
        return self.number_of_inputs - len(self.input_gates_dict)

    def is_input_signal_piloted(self, ix:int):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        return self.input_gates_dict.get(ix) != None
    
    def get_input_signal_status(self,ix):
        return self.input_signals_list[ix].val
    
    def get_output_signal_status(self, ix=0):
        return self.output_signal.val

    def add_child_gate(self, child_gate:'BasicGate'):
        self.child_gates_set.add(child_gate)

    '''#!FIX?
    def get_all_child_gates(self):
        return self.child_gates_set
    '''

    def compute_result(self):
        pass

    def has_output_signal_changed(self):#da chiamare dopo compute_result
        return self.has_oputput_signal_changed
    
    def get_output_signal(self, ix=0):
        return self.output_signal.val

    def input_gates_results_set_input_signals(self, input_signal_ix): 
        input_gate, input_gate_output_signal_ix = self.input_gates_dict[input_signal_ix]
        self.input_signals_list[input_signal_ix].val = input_gate.get_output_signal(input_gate_output_signal_ix)

    def __str__(self):
        return super().__str__() + " -> " + str(self.output_signal.val)

    def reset_all_signals(self):
        for ix in range(len(self.input_signals_list)):
            self.input_signals_list[ix] = SIGNAL()
        self.output_signal = SIGNAL()
        self.has_oputput_signal_changed = False
    
    def print_input_signal_status(self, input_signal_ix:int, lvl:int =0): 
        pilot_gate, pilot_gate_output_signal_ix = self.input_gates_dict.get(input_signal_ix)
        pilot_gate_info:str = "/"
        if(pilot_gate != None):
            pilot_gate_info = pilot_gate.name
        before:str = ""
        for i in range(lvl):
            before += " >"
        if(lvl == 0):
            before += "O"
        print(before+ " Signal IX: "+str(input_signal_ix)+" of "+self.name+" |PILOT_GATE: " +str(pilot_gate_info) + "PILOT_GATE_OUTPUT_SIGNAL_IX: "+ str(pilot_gate_output_signal_ix) +" |----------------| STATUS: "+ str(self.input_signals_list[input_signal_ix]))

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
            print("PILOTS CHILD GATES: ")
            for cg, cg_is_ix in self.child_gates_set:
                print(" -> ("+ str(cg) +") on INPUT_SIGNAL_IX: "+ str(cg_is_ix))

    def print_all_output_signals_status(self): 
        print("@ OUTPUT SIGNALS - Traccia di tutti i segnali interni collegati, l'ultimo e' di una BasicPort:")
        for input_signal_ix in range(self.number_of_inputs):
            self.print_output_signal_status(input_signal_ix, 0)
            print("----------------")

    def get_all_internal_BasicGates(self):
        return [self]
    
    def get_number_of_piloted_signals(self): #!NOT get_number_of_children
        return len(self.child_gates_set)



class AND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "AND"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = True
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val and s.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val


class OR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "OR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = False
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val or s.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val


class NAND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NAND"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = True
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val and s.val
        self.output_signal.val = not self.output_signal.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val

class NOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NOR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = False
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val or s.val
        self.output_signal.val = not self.output_signal.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val

class NOT(BasicGate):
    def __init__(self, input_gate:tuple[AbstractGate, int] = (None, 0), name: str = "NOT"):
        super().__init__([], 1, name)
        self.add_input_gate(input_gate)

    def add_input_gate(self, input_gate:tuple[AbstractGate, int]):
        if(self.input_gates_dict.get(0) == None):
            self.input_gates_dict[0] = input_gate  #(input_gate, input_gate_output_signal_ix)
            input_gate[0].add_child_gate((self, 0))  # (self, self_input_signal_ix)
        else:
            print("WARNING: La gate NOT accetta SOLO 1 segnale in input - Operazione annullata")

    def compute_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = not self.input_signals_list[0].val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val

class XOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "XOR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal_val = self.output_signal.val
        number_of_true_inputs = sum(1 for signal in self.input_signals_list if signal.val)
        self.output_signal.val = (number_of_true_inputs % 2) == 1  # XOR is true when odd number of inputs are true
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val

#setti la gate in input ad un pin di B, A contiene B nella lista delle gates di output

def apply_SwitchGates_immediatly(considered_switches:list[AbstractGate]):
    for p in considered_switches:
        for child_gate, child_gate_input_signal_ix in p.child_gates_set:
            child_gate.input_gates_results_set_input_signals(child_gate_input_signal_ix)
                

#!funziona solo con BASIC GATE
def run_simulation(max_iterations:int = 10, considered_gates:list[BasicGate] = GLOBAL_ALL_GATES_LIST, considered_switches:list[SwitchGate] = GLOBAL_ALL_SWITCHES_LIST):#se non passo la rete logica, eseguo tutte le gates
    apply_SwitchGates_immediatly(considered_switches)

    current_level_gates:set[AbstractGate] = set()
    next_level_gates:set[AbstractGate] = set()
    current_level_gates.update(considered_gates)
    #current_level_gates_copy = current_level_gates.copy()#!ERRATO lista di funzioni per i pin che devono essere cambiati a fine turno
    next_level_gates_signals_to_update:set[AbstractGate, int] = set()#next_level_gate, signal_ix to update
    level:int = 0
    iterations:int = 0  
    print("LEVEL: ", level)

    while len(current_level_gates) >0 and iterations < max_iterations:
        iterations += 1
        current_gate:AbstractGate = current_level_gates.pop()
        current_gate.compute_result()
        if(current_gate.has_output_signal_changed):
            for tup in current_gate.child_gates_set:
                next_level_gates_signals_to_update.add(tup) #(child_gate, child_gate_input_signal_ix)
                next_level_gates.add(tup[0])
            #! add (A,0) set input signal di A,0
        print(current_gate)

        if len(current_level_gates) == 0:
            level += 1
            if(len(next_level_gates) > 0):
                print("LEVEL: ", level)
            while len(next_level_gates_signals_to_update) > 0:
                tup = next_level_gates_signals_to_update.pop()
                child_gate, child_gate_input_signal_ix = tup
                child_gate.input_gates_results_set_input_signals(child_gate_input_signal_ix)
            current_level_gates = next_level_gates.copy()
            next_level_gates.clear()


#? SITAX: list[(Gate0, Gate0_output_signal_ix), (Gate1, Gate1_output_signal_ix)]; Gate0 input_gates_dict[ix=0], Gate1 input_gates_dict[ix=1];

switch1 = SwitchGate()
switch2 = SwitchGate()
and1 = AND([(switch1,0), (switch2,0)], name="and1")
and2 = AND([(and1,0), (switch1,0)], name="and2")
not1 = NOT((and2,0))
run_simulation()




