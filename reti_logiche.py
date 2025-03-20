from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_BASIC_GATES_LIST:list['AbstractGate'] = []
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
        self.input_gates_dict:dict[int, tuple['AbstractGate', int]] = {} #*input pin ix -> input_gate e l'ix del segnale di output di input_gate
        self.number_of_outputs:int = number_of_outputs
        self.child_gates_dict:dict[int, set[tuple['AbstractGate', int]]] = {} #*output pin ix -> child_gate e l'ix del segnale di input di child_gate
        for ix in range(number_of_outputs):
            self.child_gates_dict[ix] = set()

        self.input_signals_name:dict[int, str] = {} #!!!
        for ix in range(number_of_inputs):
            self.input_signals_name[ix] = "/"

        self.output_signals_name:dict[int, str] = {}
        for ix in range(self.number_of_outputs):
            self.output_signals_name[ix] = "/"

    def __str__(self):
        return "Name: "+ str(self.name)

    def get_name(self):
        return self.name
    
    def get_child_gates_by_output_signal_index(self, ix:int):
        if(ix >= self.number_of_outputs):
            raise Exception(f"ix: {ix} > last_output_signal_ix: {self.number_of_outputs-1}")
        return self.child_gates_dict.get(ix)
    
    def get_all_child_gates(self):
        ris:set[tuple[AbstractGate,int]] = set()
        for ix in range(self.number_of_outputs):
            ris.update(self.get_child_gates_by_output_signal_index(ix))
        return ris
    
    def get_child_gates_dict(self):
        return self.child_gates_dict
    
    def get_input_gate_by_input_signal_index(self, ix:int):
        if(ix >= self.number_of_inputs):
            raise Exception(f"ix: {ix} > last_input_signal_ix: {self.number_of_inputs-1}")
        return self.input_gates_dict.get(ix)

    def get_all_input_gates(self):
        ris:set[tuple[AbstractGate,int]] = set()
        for ix in range(self.number_of_inputs):
            gi = self.get_input_gate_by_input_signal_index(ix)
            if(gi):
                ris.add(gi)
        return ris
    
    def connect_input_gate_to_input_signal(self, input_gate_tup: tuple["LogicClass", int], input_signal_ix:int):
        if not isinstance(input_gate_tup, tuple):
            raise Exception(f"@@@INTERNAL ERROR: connect_input_gate_to_input_signal() WANTS a TUPLE")
        if input_signal_ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(input_signal_ix) + " last index: " + str((self.number_of_inputs)-1))
        input_gate, input_gate_output_signal = input_gate_tup
        if(self.input_gates_dict.get(input_signal_ix) != None):#!UNTESTED 
            self.unconnect_input_gate_from_input_signal(input_signal_ix)
        input_gate.add_child_gate(input_gate_output_signal,(self, input_signal_ix))
        self.input_gates_dict[input_signal_ix] = input_gate_tup
        print(f"Connected input signal {input_signal_ix} of gate '{self.name}' to output signal {input_gate_output_signal} of gate '{input_gate.name}'")

    def connect_multiple_input_gates_to_input_signals(self, input_gate_tup_list:list[tuple["AbstractGate",int]], first_ix:int =0):
        if not isinstance(input_gate_tup_list, list):
            raise Exception(f"@@@INTERNAL ERROR: connect_multiple_input_gates_to_input_signals() WANTS a LIST")
        if first_ix + len(input_gate_tup_list) > self.number_of_inputs:
            raise Exception("ERRORE: Input signal index out of range, your last index index: " + str(first_ix + len(input_gate_tup_list) - 1) + " last available index: " + str((self.number_of_inputs)-1))

        for tup in input_gate_tup_list:
            self.connect_input_gate_to_input_signal(tup, first_ix)
            first_ix += 1
    
    def unconnect_input_gate_from_input_signal(self, input_index:int):#!UNTESTED
        gate_tup:tuple[LogicClass,int] = self.input_gates_dict.pop(input_index, None)
        if(gate_tup):
            input_gate, output_signal_ix = gate_tup
            input_gate.remove_child_gate(output_signal_ix, (self, input_index))
            print(f"UNconnected input signal {input_index} of gate '{self.name}' from output signal {output_signal_ix} of gate '{input_gate.name}'")

    def add_child_gate(self, index:int, gate_tup:tuple["LogicClass",int]):
        print(f"name: {self.name} self.child_gates_dict: {self.child_gates_dict}")
        self.child_gates_dict[index].add(gate_tup)
    
    def remove_child_gate(self, index:int, gate_tup:tuple["LogicClass",int]):
        self.child_gates_dict[index].remove(gate_tup)

    def set_child_gates_input_signals(self):
        pass

    




class SwitchGate(LogicClass):
    def __init__(self, inital_value:bool =True, name: str = "SwitchGate"):
        super().__init__(0, 1, name)
        GLOBAL_ALL_SWITCHES_LIST.append(self)
        self.output_signal = inital_value
    
    def toggle(self):
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = True
    
    def get_output_signal_value(self, ix=0):
        return self.output_signal
    
    def set_child_gates_input_signals(self):
        for child_gate, child_gate_input_ix in self.child_gates_dict[0]:
            child_gate.set_input_signal_value(child_gate_input_ix, self.output_signal)

    def print_child_gates(self):
        print("Child gates of(", self, "): ")
        for c in self.child_gates_dict.get(0):
            print(c)
        print("")


class AbstractGate(LogicClass):
    def __init__(self, number_of_inputs, number_of_outputs, name: str = "AbstractGate"):
        super().__init__(number_of_inputs, number_of_outputs, name)

    def input_gates_results_set_input_signals(self, input_signal_ix): 
        pass #Both classes have this method
    
    def _update_internal_gates_affected_by_last_level_signal_changes(self, input_signal_ix):
        pass #I need this method to end the recursion when I reach a BasicGate

    def _get_all_internal_basic_gates(self):
        pass #I need this method to end the recursion when I reach a BasicGate

    def get_input_signal_value(self, ix):
        pass #Both classes have this method
    
    def get_output_signal_value(self, ix):
        pass #Both classes have this method

    def reset_all_signals(self):
        pass #Both classes have this method

    def compute_result_and_returns_gates_affeted_by_the_result(self):
        pass #Both classes have this method

    def get_all_basic_gates_connected_to_input_signal(self, input_signal_ix):
        pass #I need this method to end the recursion when I reach a BasicGate
    
    
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
        
        self.internal_gates_connected_to_input_signal_ix:dict[int, set[("AbstractGate",int)]] = {} #* input_signal_ix -> [(first_layer_gate,flg_input_signal_ix)]
        for i in range(self.number_of_inputs):
            self.internal_gates_connected_to_input_signal_ix[i] = set()
        
        self.output_signals_list:list[SIGNAL] = []
        for i in range(self.number_of_outputs):
            self.output_signals_list.append(None)
        self.internal_gates_that_pilots_output_signal_ix:dict[int, (AbstractGate,int)] = {}#* output_signal_ix -> (last_layer_gate,flg_output_signal_ix)
        


    def _get_input_signal(self, input_ix): #portebbero essere più signal interni = [SIGNAL, SIGNAL] pilotati dallo stesso signal ix
        return self.input_signals_list[input_ix]

    def set_module_gate_input_signal_to_internal_gate_input_signal(self, first_layer_gate_tup:tuple[AbstractGate,int], self_input_signal_ix:int, name:str = '/'):
        first_layer_gate, flg_input_signal_ix = first_layer_gate_tup
        self.input_signals_list[self_input_signal_ix].extend(first_layer_gate._get_input_signal(flg_input_signal_ix))#!___ok
        self.internal_gates_connected_to_input_signal_ix[self_input_signal_ix].add((first_layer_gate,flg_input_signal_ix))
        self.input_signals_name[self_input_signal_ix] = name

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
    
    def _get_all_internal_basic_gates(self):
        ris:set[tuple[BasicGate,int]] = set()
        for ig in self.internal_gates:
            ris.update(ig._get_all_internal_basic_gates())
        return ris
    
    def get_all_basic_gates_connected_to_input_signal(self, input_signal_ix):
        result:set[BasicGate] = set()
        for gate in self.internal_gates_connected_to_input_signal_ix[input_signal_ix]:
            result.update(gate.get_all_basic_gates_connected_to_input_signal())
        return result



class BasicGate(AbstractGate):
    def __init__(self, input_gates_list:list['BasicGate'], number_of_inputs:int = 2, name:str = "BasicGate", low_to_high_timer:float =10, high_to_low_timer:float =10):
        super().__init__(number_of_inputs=number_of_inputs, number_of_outputs=1, name=name)
        GLOBAL_ALL_BASIC_GATES_LIST.append(self)
        self.input_signals_list:list[SIGNAL] = []
        self.number_of_outputs:int = 1
        self.output_signal:SIGNAL = SIGNAL()
        self.low_to_high_timer:float = low_to_high_timer
        self.high_to_low_timer:float = high_to_low_timer

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

    def compute_result(self, considered_signals:list[bool]):#!!!
        pass#esiste nei gate basilari

    def set_output_signal(self, res:bool):
        self.output_signal.val = res

    def set_child_gates_input_signals(self):
        for child_gate, child_gate_input_ix in self.child_gates_dict[0]:
            child_gate.set_input_signal_value(child_gate_input_ix, self.get_output_signal_value(0))

    def __str__(self):
        return super().__str__() + " -> " + str(self.output_signal.val)

    def reset_all_signals(self):
        for ix in range(len(self.input_signals_list)):
            self.input_signals_list[ix] = SIGNAL()
        self.output_signal = SIGNAL()
        self.has_oputput_signal_changed = False

    def get_input_signal_value(self,ix):
        return self.input_signals_list[ix].val
    
    def get_input_signals_value_list(self):
        ris:list[bool] = []
        for ix in range(self.number_of_inputs):
            ris.append(self.get_input_signal_value(ix))
        return ris
    
    def set_input_signal_value(self, ix, val):
        self.input_signals_list[ix].val = val
    
    def get_output_signal_value(self, ix=0):
        return self.output_signal.val
    
    def _get_input_signal(self, input_ix): 
        return [self.input_signals_list[input_ix]]
    
    def _get_output_signal(self, input_ix=0): 
        return self.output_signal
    
    def _get_all_internal_basic_gates(self):
        return [self]
    
    def get_all_basic_gates_connected_to_input_signal(self, input_signal_ix):
        return {self}





class AND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "AND", low_to_high_timer:float =10, high_to_low_timer:float =10):
        super().__init__(input_gates_list, n_input_signals, name, low_to_high_timer, high_to_low_timer)
    
    def compute_result(self, considered_signals):
        res = True
        for s in considered_signals:
            res = res and s
        return res
        

class OR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "OR", low_to_high_timer:float =10, high_to_low_timer:float =10):
        super().__init__(input_gates_list, n_input_signals, name, low_to_high_timer, high_to_low_timer)
    
    def compute_result(self, considered_signals):
        res = False
        for s in considered_signals:
            res = res or s
        return res


class NAND(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NAND", low_to_high_timer:float =10, high_to_low_timer:float =10):
        super().__init__(input_gates_list, n_input_signals, name, low_to_high_timer, high_to_low_timer)
    
    def compute_result(self, considered_signals):
        res = True
        for s in considered_signals:
            res = res and s
        res = not res
        return res

class NOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "NOR", low_to_high_timer:float =10, high_to_low_timer:float =10):
        super().__init__(input_gates_list, n_input_signals, name, low_to_high_timer, high_to_low_timer)
    
    def compute_result(self, considered_signals):
        res = False
        for s in considered_signals:
            res = res or s
        res = not res
        return res

class NOT(BasicGate):
    def __init__(self, input_gate:tuple[AbstractGate, int] = None, name: str = "NOT", low_to_high_timer:float =10, high_to_low_timer:float =10):
        super().__init__([], 1, name, low_to_high_timer, high_to_low_timer)
        if(input_gate != None):
            self.add_input_gate(input_gate)

    def add_input_gate(self, input_gate_tup:tuple[AbstractGate, int]):
        if(self.input_gates_dict.get(0) == None):
            self.input_gates_dict[0] = input_gate_tup  #(input_gate, input_gate_output_signal_ix)
            input_gate, input_gate_output_signal = input_gate_tup
            input_gate.add_child_gate(input_gate_output_signal, (self, 0))  # (self, self_input_signal_ix) #!!!
        else:
            print("WARNING: La gate NOT accetta SOLO 1 segnale in input - Operazione annullata")
    
    def compute_result(self, considered_signals):
        res = not considered_signals[0]
        return res

class XOR(BasicGate):
    def __init__(self, input_gates_list:list[AbstractGate] = [], n_input_signals:int = 2, name: str = "XOR", low_to_high_timer:float =10, high_to_low_timer:float =10):
        super().__init__(input_gates_list, n_input_signals, name, low_to_high_timer, high_to_low_timer)
    
    def compute_result(self, considered_signals):
        number_of_true_inputs = sum(1 for signal in considered_signals if signal.val)
        return (number_of_true_inputs % 2) == 1  # XOR is true when odd number of inputs are true
    



#? SITAX: list[(Gate0, Gate0_output_signal_ix), (Gate1, Gate1_output_signal_ix)]; Gate0 input_gates_dict[ix=0], Gate1 input_gates_dict[ix=1];


switch1 = SwitchGate(name="switch1")
switch2 = SwitchGate(name="switch2")
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
#ciclo
not1 = NOT(name="not1")
not2 = NOT(name="not2", input_gate=(not1,0))
#not1.connect_input_gate_to_input_signal((not2,0),0)
'''


'''
not1 = NOT(name="not1")
not2 = NOT(name="not2", input_gate=(not1,0))
not1.connect_input_gate_to_input_signal((not2,0),0)
prova:ModuleGate = ModuleGate([not1,not2], 2, 2)
prova.set_module_gate_input_signal_to_internal_gate_input_signal((not1,0),0)
prova.set_module_gate_input_signal_to_internal_gate_input_signal((not2,0),1)
prova.set_module_gate_output_signal_to_internal_gate_output_signal((not1,0),0)
prova.set_module_gate_output_signal_to_internal_gate_output_signal((not2,0),1)
prova.connect_multiple_input_gates_to_input_signals([(switch1,0),(switch2,0)])'
'''

#print(prova.get_all_input_gates())
#run_simulation()#you should pass in a list




