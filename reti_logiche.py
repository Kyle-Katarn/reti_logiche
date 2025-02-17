from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_PORTS_LIST:list['AbstractPort'] = []
GLOBAL_ALL_SWITCHES_LIST:list['AbstractPort'] = []

class AbstractPort:
    def __init__(self, name: str = "AbstractPort"):
        self.name: str = name

        self.output_signal: bool = False
        self.has_oputput_signal_changed: bool = False
        self.child_ports_set: set['AbstractPort'] = set()

        self.number_of_inputs:int = 0

    def add_child_port(self, child_port:'AbstractPort'):
        self.child_ports_set.add(child_port)
    
    def compute_result(self):
        pass

    def __str__(self):
        return "Name: "+ self.name + " -> " + str(self.output_signal)

    def get_child_ports_list(self):
        return self.child_ports_set
    
    def get_number_of_inputs(self):
        return self.number_of_inputs
    
    def get_output_signal(self):
        return self.output_signal


class SwitchPort(AbstractPort):
    def __init__(self, inital_value:bool =True, name: str = "SwitchPort"):
        super().__init__(name)

        GLOBAL_ALL_SWITCHES_LIST.append(self)
        self.output_signal = inital_value
    
    def toggle(self):
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = True

    



class PortWithInputs(AbstractPort):
    def __init__(self, number_of_inputs:int = 0, name:str = "PortWithInput"):
        super().__init__(name)
        GLOBAL_ALL_PORTS_LIST.append(self)
        self.input_ports_dict:dict[int, AbstractPort] = {} #la porta e l'indice del imput_signal che pilota
        self.input_signals_list:list[bool] = []

        for _ in range(number_of_inputs): #inizializza la lista degli input_signals
            self.input_signals_list.append(False)
        self.number_of_inputs:int = number_of_inputs

    def connect_multiple_input_signals_to_input_ports(self, input_ports_param: list[AbstractPort]):
        ix:int = len(self.input_ports_dict)#first unpiloated input_signal index
        if(ix + len(input_ports_param) > self.number_of_inputs):
            raise ValueError("ERRORE: porte di input in eccesso, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        if(ix + len(input_ports_param) < self.number_of_inputs):
            print("WARNING: porte di input insufficienti, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        
        for input_port in input_ports_param:
            self.connect_input_signal_to_input_port(input_port, ix)
            ix+=1

    def connect_input_signal_to_input_port(self, input_port: AbstractPort, input_signal_ix: int):
        if input_signal_ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(input_signal_ix) + " last index: " + (str(self.number_of_inputs)-1))
        self.input_ports_dict[input_signal_ix] = input_port
        input_port.add_child_port(self)
 
    def get_input_ports_dict(self):
        return self.input_ports_dict
    
    def print_input_signal_status(self):
        for ix in range(len(self.input_signals_list)):
            pilot_port:AbstractPort = self.input_ports_dict.get(ix)
            pilot_port_info:str
            if(pilot_port == None):
                pilot_port_info = "NONE"
            else:
                pilot_port_info = pilot_port.__str__()
            print("SIGNAL IX: ", ix, " |PILOT PORT: ", pilot_port_info, " |SIGNAL STATUS: ", self.input_signals_list[ix])


class ModulePort(AbstractPort):
    def __init__(self, internal_ports_list:list[PortWithInputs], input_ports_list:list[AbstractPort], name = "ModulePort"):
        super().__init__(name)
        self.internal_ports_list = internal_ports_list
        self.input_ports_list = input_ports_list
        self.link_internal_ports_and_input_ports()

        self.input_internal_ports_list = [] #porte interne che ricevono il segnale dall'esterno
        for port in self.internal_ports_list:
            if port.get_input_ports_list() == []:
                self.input_internal_ports_list.append(port)

        self.output_internal_ports_list = [] #porte interne che mandano il segnale all'esterno
        for port in self.internal_ports_list:
            if port.get_child_ports_list() == []:
                self.output_internal_ports_list.append(port)
        

    def print_first_level_internal_ports(self):
        print("First level internal ports:")
        for ix, port in enumerate(self.internal_ports_list):
            if port.get_input_ports_list() == []:
                print(f"Index: {ix}, Port: {port}")
    
    def print_last_level_internal_ports(self):
        print("Last level internal ports:")
        for ix, port in enumerate(self.internal_ports_list):
            if port.get_child_ports_list() == []:
                print(f"Index: {ix}, Port: {port}")

    def link_internal_ports_and_input_ports(self):
        input_ports_ix:int = 0
        for port in self.input_internal_ports_list:
            for j in range(port.get_number_of_inputs()):
                input_ports_ix += 1
                if(input_ports_ix >= len(self.input_ports_list)):
                    raise ValueError("Errore: porte di input insufficienti, porte di input: " + str(len(self.input_ports_list)) + " porte di input necessarie: " + str(input_ports_ix))
                port.add_input_ports(self.input_ports_list[input_ports_ix])
                self.input_ports_list[input_ports_ix].add_child_port(port)
        
        if(input_ports_ix < len(self.input_ports_list)):
            raise ValueError("Errore: porte di input in eccesso, porte di input: " + str(len(self.input_ports_list)) + " porte di input necessarie: " + str(input_ports_ix))

    def select_output_internal_ports(self, output_internal_ports_list:list[PortWithInputs]):
        self.output_internal_ports_list_copy.extend(output_internal_ports_list)

    def select_input_internal_ports(self, input_internal_ports_list:list[PortWithInputs]):
        self.input_internal_ports_list_copy.extend(input_internal_ports_list)

    def out(self, ix:int):
        return self.output_internal_ports_list_copy[ix]


class BasicPort(PortWithInputs):
    def __init__(self, input_ports_list:list['AbstractPort'], n_input_signals:int = 2, name: str = "BasicPort"):
        super().__init__(n_input_signals, name)
        self.add_input_ports(input_ports_list)

    def add_input_ports(self, input_ports_param:list[AbstractPort]):#!solo Basic port 
        #connette gli input_signals gia presenti con le porte di input
        #!*se ci sono più porte di input che input_signals, aggiunge input_signals
        len_input_ports_dict:int = len(self.input_ports_dict)#indcice del primo input_signal non pilotato
        number_of_unconnected_input_signals:int = self.number_of_inputs - len_input_ports_dict
        number_of_extra_input_ports:int = len(input_ports_param) - number_of_unconnected_input_signals
        self.number_of_inputs += max(0, number_of_extra_input_ports)#se passi meno porte di input di quelle necessarie

        ix:int = len_input_ports_dict
        for input_port in input_ports_param:
            input_port.add_child_port(self)
            self.input_ports_dict[ix] = input_port
            ix += 1

    def input_ports_results_set_input_signals(self):
        for ix in range(self.number_of_inputs):
            pilot_port:AbstractPort = self.input_ports_dict.get(ix)
            if(pilot_port != None):
                self.input_signals_list[ix] = pilot_port.get_output_signal()

    
    def has_output_signal_changed(self):#da chiamare dopo compute_result
        return self.has_oputput_signal_changed
    


class AND(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort] = [], n_input_signals:int = 2, name: str = "AND"):
        super().__init__(input_ports_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        print("old_output_signal: "+ str(old_output_signal))
        self.output_signal = True
        for value in self.input_signals_list:
            self.output_signal = self.output_signal and value
        self.has_oputput_signal_changed = old_output_signal != self.output_signal


class OR(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort] = [], n_input_signals:int = 2, name: str = "OR"):
        super().__init__(input_ports_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = False
        for value in self.input_signals_list:
            self.output_signal = self.output_signal or value
        self.has_oputput_signal_changed = old_output_signal != self.output_signal


class NAND(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort] = [], n_input_signals:int = 2, name: str = "NAND"):
        super().__init__(input_ports_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = True
        for value in self.input_signals_list:
            self.output_signal = self.output_signal and value
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = old_output_signal != self.output_signal

class NOR(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort] = [], n_input_signals:int = 2, name: str = "NOR"):
        super().__init__(input_ports_list, n_input_signals, name)
        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = False
        for value in self.input_signals_list:
            self.output_signal = self.output_signal or value
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = old_output_signal != self.output_signal

class NOT(BasicPort):
    def __init__(self, input_port:AbstractPort = None, name: str = "NOT"):
        super().__init__([], 1, name)
        self.add_input_port(input_port)

    def add_input_port(self, input_port_param:AbstractPort):
        if(self.get_input_ports_dict().get(0) == None):
            self.get_input_ports_dict()[0] = input_port_param
            input_port_param.add_child_port(self)
        else:
            print("WARNING: La porta NOT accetta SOLO 1 segnale in input - Operazione annullata")

        
    def compute_result(self):
        old_output_signal = self.output_signal
        self.output_signal = not self.input_signals_list[0]
        self.has_oputput_signal_changed = old_output_signal != self.output_signal

#setti la porta in input ad un pin di B, A contiene B nella lista delle porte di output

def apply_SwitchPorts_immediatly(considered_switches:list[AbstractPort]):
    for p in considered_switches:
        for f in p.child_ports_set:
            f.input_ports_results_set_input_signals()
                #applica prende i risultati di tutte le porte in input
                #*NON è un problema se il metodo è chiamato a fine turno ossia dopo aver chiamato set_input_signals su tutte currnet_level_ports. (è un problema altrimenti)


def esegui_rete_logica(max_iterations:int = 10, considered_ports:list[AbstractPort] = GLOBAL_ALL_PORTS_LIST, considered_switches:list[AbstractPort] = GLOBAL_ALL_SWITCHES_LIST):#se non passo la rete logica, eseguo tutte le porte
    apply_SwitchPorts_immediatly(considered_switches)

    current_level_ports:set[AbstractPort] = set()
    next_level_ports:set[AbstractPort] = set()
    current_level_ports.update(considered_ports)
    print(considered_ports)

    current_level_ports_copy = current_level_ports.copy()
    level:int = 0
    iterations:int = 0  
    print("LEVEL: ", level)

    while len(current_level_ports) >0 and iterations < max_iterations:
        iterations += 1
        current_port = current_level_ports.pop()
        current_port.compute_result()
        if(current_port.has_oputput_signal_changed):
            next_level_ports.update(current_port.get_child_ports_list())
        print(current_port)

        if len(current_level_ports) == 0:
            level += 1
            if(len(next_level_ports) > 0):
                print("LEVEL: ", level)
            current_level_ports = next_level_ports.copy()
            next_level_ports.clear()
            while len(current_level_ports_copy) > 0:
                current_port = current_level_ports_copy.pop()
                current_port.input_ports_results_set_input_signals()  # Updated method call

switch1 = SwitchPort()

and1 = AND([switch1, switch1], 2, "and1")
not1 = NOT(and1)
or1 = OR([], 2, "OR1")


esegui_rete_logica()




