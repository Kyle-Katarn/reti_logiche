from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_GATES_LIST:list['AbstractGate'] = []
GLOBAL_ALL_SWITCHES_LIST:list['AbstractGate'] = []

class SIGNAL():
    def __init__(self, val:bool = False):
        self.val = val

class LogicClass:
    '''
    Nome, numero di segnali in ingresso
    '''
    def __init__(self, number_of_inputs, number_of_outputs, name: str = "LogicClass"):
        self.name: str = name
        self.number_of_inputs:int = number_of_inputs
        self.number_of_outputs:int = number_of_outputs

    def __str__(self):
        return "Name: "+ str(self.name)

    def get_name(self):
        return self.name





class SwitchGate(LogicClass):
    def __init__(self, inital_value:bool =True, name: str = "SwitchGate"):
        super().__init__(0, 1, name)
        self.number_of_outputs = 1
        self.output_signal: bool = False
        GLOBAL_ALL_SWITCHES_LIST.append(self)
        self.output_signal = inital_value
        self.child_gates_set: set[tuple['AbstractGate', int]] = set()
    
    def toggle(self):
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = True
    
    def add_child_gate(self, child_gate_tup:tuple['AbstractGate', int]):
            self.child_gates_set.add((child_gate_tup))
    
    def get_output_signal_value(self, ix=0):
        return self.output_signal

    def print_child_gates(self):
        print("Child gates of(", self, "): ")
        for c in self.child_gates_set:
            print(c)
        print("")


class AbstractGate(LogicClass):
    def __init__(self, number_of_inputs, number_of_outputs, name: str = "AbstractGate"):
        super().__init__(number_of_inputs, number_of_outputs, name)
        GLOBAL_ALL_GATES_LIST.append(self)
        self.input_gates_dict:dict[int, tuple['AbstractGate', int]] = {} #*input_gate e l'ix del segnale di output di input_gate
        self.child_gates_dict:dict[int, set[tuple['AbstractGate', int]]] = {} #*child_gate e l'ix del segnale di input di child_gate
        for i in range(self.number_of_outputs):
            self.child_gates_dict[i] = set()

    def connect_input_gate_to_input_signal(self, param: tuple["AbstractGate", int], input_signal_ix:int):
        if input_signal_ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(input_signal_ix) + " last index: " + str((self.number_of_inputs)-1))
        self.input_gates_dict[input_signal_ix] = param
        input_gate, input_gate_signal_ix = param
        input_gate.add_child_gate((self, input_signal_ix))

    def connect_multiple_input_gates_to_input_signals(self, param:list[tuple["AbstractGate",int]], first_ix:int =0):
        if first_ix + len(param) > self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your last index index: " + str(first_ix + len(param) - 1) + " last available index: " + str((self.number_of_inputs)-1))

        for tup in param:
            self.connect_input_gate_to_input_signal(tup, first_ix)
            first_ix += 1

    def input_gates_results_set_input_signals(self, input_signal_ix): 
        pass
    
    def _update_internal_gates_affected_by_last_level_signal_changes(self, input_signal_ix):
        pass #I need this method here to end the recursion when I reach a BasicGate


    
class ModuleGate(AbstractGate):
    def __init__(self, internal_gates:list[AbstractGate] = [], number_of_inputs:int =0, number_of_outputs:int =0, name = "AbstractGate"):
        super().__init__(number_of_inputs=number_of_inputs, number_of_outputs=number_of_outputs, name=name)
        self.internal_gates:list[AbstractGate] = internal_gates
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs

        self.input_signals_list:list[list[SIGNAL]] = []
        self.input_signals_name:dict[int, str] = {}
        for ix in range(number_of_inputs):
            self.input_signals_list.append([])
            self.input_signals_name[ix] = "/"
        
        self.internal_gates_affected_by_input_signal_ix:dict[int, set[("AbstractGate",int)]] = {} #* input_signal_ix -> [(first_layer_gate,flg_input_signal_ix)]
        for i in range(self.number_of_inputs):
            self.internal_gates_affected_by_input_signal_ix[i] = set()

        self.internal_gates_affected_by_last_level_signal_changes:set[(AbstractGate,int)] = set() #you aways have to .clear() it
        
        
        self.output_signals_list:list[SIGNAL] = []
        for i in range(self.number_of_outputs):
            self.output_signals_list.append(None)
        self.output_signals_name:dict[int, str] = {}
        self.internal_gates_that_pilots_output_signal_ix:dict[int, (AbstractGate,int)] = {}#* output_signal_ix -> (last_layer_gate,flg_output_signal_ix)
        for ix in range(self.number_of_outputs):
            self.output_signals_name[ix] = "/"


    def _get_input_signal(self, input_ix): #portebbero essere più signal interni = [SIGNAL, SIGNAL] pilotati dallo stesso signal ix
        return self.input_signals_list[input_ix]

    def set_module_gate_input_signal_to_internal_gate_input_signal(self, first_layer_gate_tup:tuple[AbstractGate,int], self_input_signal_ix:int, name:str = '/'):
        first_layer_gate, flg_input_signal_ix = first_layer_gate_tup
        self.input_signals_list[self_input_signal_ix].extend(first_layer_gate._get_input_signal(flg_input_signal_ix))#!___ok
        self.internal_gates_affected_by_input_signal_ix[self_input_signal_ix].add((first_layer_gate,flg_input_signal_ix))
        self.input_signals_name[self_input_signal_ix] = name

    def input_gates_results_set_input_signals(self, input_signal_ix):
        #*se cambia l'input_signal X, solo le internal_gates dipendenti da X devono ricalolare, qundi tutte le X in GatesAffectedByInputSignalChange
        #*quando viene chiamato compute_result (nel livello successivo) si ricalcolano tutti i gate interessati e poi si resetta il set
        input_gate, input_gate_output_ix = self.input_gates_dict[input_signal_ix]
        input_gate_res:bool = input_gate.get_output_signal_value(input_gate_output_ix)
        for s in self.input_signals_list[input_signal_ix]:
            s.val = input_gate_res

        #self.internal_gates_affected_by_last_level_signal_changes.update(self.internal_gates_affected_by_input_signal_ix.get(input_signal_ix))#!__chiama ricorsivamente fino a basic gate
        self._update_internal_gates_affected_by_last_level_signal_changes(input_signal_ix)
        #*modifichi SIGNAL dell'internal gate

    def _update_internal_gates_affected_by_last_level_signal_changes(self, input_signal_ix):
        self.internal_gates_affected_by_last_level_signal_changes.update(self.internal_gates_affected_by_input_signal_ix.get(input_signal_ix))
        for internal_gate, internal_gate_input_signal_ix in self.internal_gates_affected_by_last_level_signal_changes:
            internal_gate._update_internal_gates_affected_by_last_level_signal_changes(internal_gate_input_signal_ix)

    #aneurysm = useless optimization: not all internal_gates_affected_by_input_signal_ix gates but only the affected by input ones
    def compute_result_and_returns_gates_affeted_by_the_result(self, compute_all__internal_gates_affected_by_module_input_signals:bool=False):
        if(compute_all__internal_gates_affected_by_module_input_signals):
            for ix in range(self.number_of_inputs):
                self.internal_gates_affected_by_last_level_signal_changes.update(self.internal_gates_affected_by_input_signal_ix.get(ix))
        gates_affected_by_the_result:set[AbstractGate] = set()
        for ig, ig_input_signal_ix in self.internal_gates_affected_by_last_level_signal_changes:
            print("ig: "+str(ig))
            gates_affected_by_the_result.update(ig.compute_result_and_returns_gates_affeted_by_the_result())
        self.internal_gates_affected_by_last_level_signal_changes.clear()
        #^^^ LVL1[compute_result, set_signals<-also sets internal_gates_affected_by_last_level_signal_changes] -> LVL2[compute_result<-right now, set_signals]
        
        return gates_affected_by_the_result

    def _get_output_signal(self, output_ix):
        return self.output_signals_list[output_ix]

    def set_module_gate_output_signal_to_internal_gate_output_signal(self, last_layer_gate_tup:tuple[AbstractGate,int], self_output_signal_ix:int, name:str = '/'):
        last_layer_gate, llg_output_signal_ix = last_layer_gate_tup
        self.output_signals_list[self_output_signal_ix] = last_layer_gate._get_output_signal(llg_output_signal_ix)
        self.output_signals_name[self_output_signal_ix] = name
        self.internal_gates_that_pilots_output_signal_ix[self_output_signal_ix] = (last_layer_gate, llg_output_signal_ix)

    def add_child_gate(self, child_gate_tup:tuple[AbstractGate, int], output_signal_ix:int =0):
        self.child_gates_dict[output_signal_ix].add(child_gate_tup)
        last_layer_gate, flg_output_signal_ix = self.internal_gates_that_pilots_output_signal_ix.get(output_signal_ix)
        last_layer_gate.add_child_gate(child_gate_tup, flg_output_signal_ix)
    
    def reset_all_signals(self):
        self.internal_gates_affected_by_last_level_signal_changes.clear()
        for g in self.internal_gates:
            g.reset_all_signals()
    
    def get_input_signal_value(self,input_signal_ix:int):
        return self.input_signals_list[input_signal_ix][0].val
    
    def get_output_signal_value(self, ix=0):
        return self.output_signals_list[ix].val



class BasicGate(AbstractGate):
    def __init__(self, input_gates_list:list['BasicGate'], number_of_inputs:int = 2, name:str = "GateWithInput"):
        super().__init__(number_of_inputs=number_of_inputs, number_of_outputs=1, name=name)
        self.input_signals_list:list[SIGNAL] = []
        self.number_of_outputs:int = 1
        self.output_signal:SIGNAL = SIGNAL()
        self.has_oputput_signal_changed: bool = False

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
            
        for tup in param:
            self.connect_input_gate_to_input_signal(tup, first_ix)
            first_ix +=1

    def is_input_signal_piloted(self, ix:int):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        return self.input_gates_dict.get(ix) != None

    def add_child_gate(self, child_gate_tup:tuple[AbstractGate, int], output_signal_ix:int =0):
        if output_signal_ix not in self.child_gates_dict:
            self.child_gates_dict[output_signal_ix] = []
        self.child_gates_dict[output_signal_ix].add(child_gate_tup)

    def compute_result_and_returns_gates_affeted_by_the_result(self):
        print(self)
        if(self.has_oputput_signal_changed):
            return self.child_gates_dict.get(0) #*0 BasicGate ha solo un output
        return set()

    def input_gates_results_set_input_signals(self, input_signal_ix): 
        input_gate, input_gate_output_signal_ix = self.input_gates_dict[input_signal_ix]
        self.input_signals_list[input_signal_ix].val = input_gate.get_output_signal_value(input_gate_output_signal_ix)

    def __str__(self):
        return super().__str__() + " -> " + str(self.output_signal.val)

    def reset_all_signals(self):
        for ix in range(len(self.input_signals_list)):
            self.input_signals_list[ix] = SIGNAL()
        self.output_signal = SIGNAL()
        self.has_oputput_signal_changed = False

    def get_input_signal_value(self,ix):
        return self.input_signals_list[ix].val
    
    def get_output_signal_value(self, ix=0):
        return self.output_signal.val
    
    def _get_input_signal(self, input_ix): 
        return [self.input_signals_list[input_ix]]
    
    def _get_output_signal(self, input_ix=0): 
        return self.output_signal




class AND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "AND"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result_and_returns_gates_affeted_by_the_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = True
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val and s.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val
        #print("and: "+str(self.output_signal.val))
        return super().compute_result_and_returns_gates_affeted_by_the_result()


class OR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "OR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result_and_returns_gates_affeted_by_the_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = False
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val or s.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val
        return super().compute_result_and_returns_gates_affeted_by_the_result()


class NAND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NAND"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result_and_returns_gates_affeted_by_the_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = True
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val and s.val
        self.output_signal.val = not self.output_signal.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val
        return super().compute_result_and_returns_gates_affeted_by_the_result()

class NOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NOR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result_and_returns_gates_affeted_by_the_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = False
        for s in self.input_signals_list:
            self.output_signal.val = self.output_signal.val or s.val
        self.output_signal.val = not self.output_signal.val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val
        return super().compute_result_and_returns_gates_affeted_by_the_result()

class NOT(BasicGate):
    def __init__(self, input_gate:tuple[AbstractGate, int] = None, name: str = "NOT"):
        super().__init__([], 1, name)
        if(input_gate != None):
            self.add_input_gate(input_gate)

    def add_input_gate(self, input_gate:tuple[AbstractGate, int]):
        if(self.input_gates_dict.get(0) == None):
            self.input_gates_dict[0] = input_gate  #(input_gate, input_gate_output_signal_ix)
            input_gate[0].add_child_gate((self, 0))  # (self, self_input_signal_ix)
        else:
            print("WARNING: La gate NOT accetta SOLO 1 segnale in input - Operazione annullata")

    def compute_result_and_returns_gates_affeted_by_the_result(self):
        old_output_signal_val = self.output_signal.val
        self.output_signal.val = not self.input_signals_list[0].val
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val
        return super().compute_result_and_returns_gates_affeted_by_the_result()

class XOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "XOR"):
        super().__init__(input_gates_list, n_input_signals, name)
        
    def compute_result_and_returns_gates_affeted_by_the_result(self):
        old_output_signal_val = self.output_signal.val
        number_of_true_inputs = sum(1 for signal in self.input_signals_list if signal.val)
        self.output_signal.val = (number_of_true_inputs % 2) == 1  # XOR is true when odd number of inputs are true
        self.has_oputput_signal_changed = old_output_signal_val != self.output_signal.val
        return super().compute_result_and_returns_gates_affeted_by_the_result()

#setti la gate in input ad un pin di B, A contiene B nella lista delle gates di output

def apply_SwitchGates_immediatly(considered_switches:list[SwitchGate]):
    for p in considered_switches:
        for child_gate, child_gate_input_signal_ix in p.child_gates_set:
            #print("ciao: "+ str(child_gate), str(child_gate_input_signal_ix))
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

    while len(current_level_gates) > 0 and iterations < max_iterations:
        #print("current_level_gates: "+str(current_level_gates))
        iterations += 1
        current_gate:AbstractGate = current_level_gates.pop()
        current_gate_children_tup = current_gate.compute_result_and_returns_gates_affeted_by_the_result()
        if current_gate_children_tup:
            for child_gate, _ in current_gate_children_tup:
                next_level_gates.add(child_gate)
            next_level_gates_signals_to_update.update(current_gate_children_tup)

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
'''
or_internal_1 = OR(name="or_internal_1", n_input_signals=1)
or1 = OR([(switch1,0)], n_input_signals=1, name="or1")  # Changed from NOT to OR with 1 input
or2 = OR(n_input_signals=1, name="or2")  # Set n_input_signals=1
prova_int:ModuleGate = ModuleGate([or_internal_1],1,1,name="prova_int")
prova_int.set_module_gate_input_signal_to_internal_gate_input_signal((or_internal_1,0),0)
prova_int.set_module_gate_output_signal_to_internal_gate_output_signal((or_internal_1,0),0)

prova_ext:ModuleGate = ModuleGate([prova_int],1,1,name="prova_ext")

prova_ext.connect_input_gate_to_input_signal((or1,0),0)
prova_ext.set_module_gate_input_signal_to_internal_gate_input_signal((prova_int,0),0)
prova_ext.set_module_gate_output_signal_to_internal_gate_output_signal((prova_int,0),0)

or1.connect_input_gate_to_input_signal((switch1,0),0)
print(prova_ext.internal_gates_that_pilots_output_signal_ix)
or2.connect_input_gate_to_input_signal((prova_ext,0),0)
'''

'''
not1 = NOT(name="not1")
not2 = NOT(name="not2", input_gate=(not1,0))
not1.connect_input_gate_to_input_signal((not2,0),0)
'''
not1 = NOT(name="not1")
not1.connect_input_gate_to_input_signal((not1,0),0)
run_simulation()#you should pass in a list




