from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_PORTS_LIST:list['AbstractPort'] = []
GLOBAL_ALL_SWITCHES_LIST:list['AbstractPort'] = []

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





class SwitchPort(LogicClass):
    def __init__(self, inital_value:bool =True, name: str = "SwitchPort"):
        super().__init__(name)
        self.number_of_outputs = 1
        self.output_signal: bool = False
        GLOBAL_ALL_SWITCHES_LIST.append(self)
        self.output_signal = inital_value
        self.child_ports_set: set['AbstractPort'] = set()
    
    def toggle(self):
        self.output_signal = not self.output_signal
        self.has_oputput_signal_changed = True
    
    def add_child_port(self, child_port:'AbstractPort'):
        self.child_ports_set.add(child_port)
    
    def get_child_ports_list(self):
        return self.child_ports_set

    def print_child_ports_list(self):
        print("Child ports of(", self, "): ")
        for c in self.child_ports_set:
            print(c)
        print("")


class AbstractPort(LogicClass):
    def __init__(self, name: str = "AbstractPort"):
        super().__init__(name)
        self.input_ports_dict = {}

    def connect_multiple_input_signals_to_input_ports(self, input_ports_param: list["AbstractPort"]):
        pass

    def connect_input_signal_to_input_port(self, input_port: "AbstractPort", input_signal_ix: int):
        pass

    def print_input_signal_status(self):
        pass

    def print_output_signal_status(self):
        pass

    def get_number_of_unpiloted_input_signals(self):
        pass

    def is_input_signal_piloted(self, ix:int):
        pass


    
class ModulePort(AbstractPort):
    def __init__(self, internal_ports:list[AbstractPort] = [], last_layer_ports:list[AbstractPort] = [], name = "AbstractPort"):
        super().__init__(name)
        self.input_ports_dict:dict[int, (AbstractPort, int)] = {}
        self.first_layer_ports:list[AbstractPort] = []#ports with 1 or more unpiloted input signals
        self.last_layer_ports:list[AbstractPort] = last_layer_ports#ports with no child ports + ports manually added by the user
        self.internal_ports:list[AbstractPort] = internal_ports


        for ip in internal_ports:
            print(ip.name + "  "+ str(ip.get_number_of_unpiloted_input_signals()))
            if(ip.get_number_of_unpiloted_input_signals() != 0):#!funziona solo per BasicPort, PROBLEMA
                self.first_layer_ports.append(ip)

        for flp in self.first_layer_ports:
            #print("flp.number_of_inputs: "+ str(flp.number_of_inputs))
            for flp_input_port_ix in range(flp.number_of_inputs):  # Fixed iteration
                #print("FLP: "+ str(flp.name)+ " ix: "+ str(flp_input_port_ix)+ " -is piloted- "+ str(flp.is_input_signal_piloted(flp_input_port_ix)))
                if(not flp.is_input_signal_piloted(flp_input_port_ix)):
                    self.input_ports_dict[self.number_of_inputs] = (flp, flp_input_port_ix)
                    self.number_of_inputs += 1
      
    def connect_multiple_input_signals_to_input_ports(self, ports_param:list[AbstractPort], first_ix:int =0):
        if(first_ix+len(ports_param) > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your last index: " + str(first_ix+len(ports_param)) + " last index: " + (str(self.number_of_inputs)-1))
        for ip in ports_param:
            self.connect_input_signal_to_input_port(ip, first_ix)
            first_ix +=1
    
    def connect_input_signal_to_input_port(self, port_param:AbstractPort, ix:int =0):
        tup = self.input_ports_dict.get(ix)
        flp, internal_ix = tup
        flp.connect_input_signal_to_input_port(port_param, internal_ix)

    def get_number_of_unpiloted_input_signals(self):
        sum:int =0
        for flp in self.first_layer_ports:
            sum+= flp.get_number_of_unpiloted_input_signals()#get_number_of_unpiloted_input_signals ha senso solo su BasicPort
        return sum

    def is_input_signal_piloted(self, ix:int):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        #is_input_signal_piloted ha senso solo su BasicPort
        #print("esplodi: "+str(self.input_ports_dict.get(ix)[0]))
        internal_port, internal_ix = self.input_ports_dict.get(ix)
        return internal_port.is_input_signal_piloted(internal_ix)
    
    def out(self, ix):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Output port of range, your last index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        return self.last_layer_ports[ix]
        


class BasicPort(AbstractPort):
    def __init__(self, input_ports_list:list['AbstractPort'], number_of_inputs:int = 2, name:str = "PortWithInput"):
        super().__init__(name)
        GLOBAL_ALL_PORTS_LIST.append(self)
        self.input_ports_dict:dict[int, AbstractPort] = {} #la porta e l'indice del imput_signal che pilota
        self.input_signals_list:list[bool] = []

        self.output_signal: bool = False
        self.has_oputput_signal_changed: bool = False
        self.child_ports_set: set['AbstractPort'] = set()

        for _ in range(number_of_inputs): #inizializza la lista degli input_signals
            self.input_signals_list.append(False)
        self.number_of_inputs:int = number_of_inputs

        self.connect_multiple_input_signals_to_input_ports(input_ports_list)

    def connect_multiple_input_signals_to_input_ports(self, input_ports_param:list[AbstractPort], first_ix:int =0):
        #!se ci sono più porte di input che input_signals, aggiunge input_signals
        if(first_ix+len(input_ports_param) > self.number_of_inputs):
            n:int = first_ix+len(input_ports_param) - self.number_of_inputs
            print("WARNING: added "+ str(n) + " input ports")
            self.number_of_inputs += n
            
        for input_port in input_ports_param:
            input_port.add_child_port(self)
            self.input_ports_dict[first_ix] = input_port
            self.input_signals_list.append(False)
            first_ix +=1

    def connect_input_signal_to_input_port(self, input_port: AbstractPort, ix:int):
        if ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        self.input_ports_dict[ix] = input_port
        input_port.add_child_port(self)

    def get_number_of_unpiloted_input_signals(self):
        '''
        res:int =0
        for ix in range(self.number_of_inputs):
            if(self.is_input_signal_piloted(ix)):
                res +=1
        '''
        return self.number_of_inputs - len(self.input_ports_dict)

    def is_input_signal_piloted(self, ix:int):
        if(ix > self.number_of_inputs):
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(ix) + " last index: " + (str(self.number_of_inputs)-1))
        return self.input_ports_dict.get(ix) != None

    def add_child_port(self, child_port:AbstractPort):
        self.child_ports_set.add(child_port)

    def compute_result(self):
        pass

    def input_ports_results_set_input_signals(self):
        for ix in range(self.number_of_inputs):
            pilot_port:AbstractPort = self.input_ports_dict.get(ix)
            if(pilot_port != None):
                self.input_signals_list[ix] = pilot_port.output_signal

    def has_output_signal_changed(self):#da chiamare dopo compute_result
        return self.has_oputput_signal_changed

    def __str__(self):
        return super().__str__() + " -> " + str(self.output_signal)
 
    def get_input_ports_dict(self):
        return self.input_ports_dict

    def get_child_ports_set(self):
        return self.child_ports_set
    
    def print_input_signal_status(self):
        for ix in range(len(self.input_signals_list)):
            pilot_port:AbstractPort = self.input_ports_dict.get(ix)
            pilot_port_info:str
            if(pilot_port == None):
                pilot_port_info = "NONE"
            else:
                pilot_port_info = pilot_port.get_name()
            print("SIGNAL IX: ", ix, " |PILOT PORT: ", pilot_port_info, " |SIGNAL STATUS: ", self.input_signals_list[ix])

    def print_output_signal_status(self):
        print(self + ", Child ports:")
        for p in self.child_ports_set:
            print(p)



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


#!funziona solo con BASIC PORT
def esegui_rete_logica(max_iterations:int = 10, considered_ports:list[BasicPort] = GLOBAL_ALL_PORTS_LIST, considered_switches:list[SwitchPort] = GLOBAL_ALL_SWITCHES_LIST):#se non passo la rete logica, eseguo tutte le porte
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
        current_port:BasicPort = current_level_ports.pop()
        current_port.compute_result()
        if(current_port.has_output_signal_changed):
            next_level_ports.update(current_port.get_child_ports_set())
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

and1 = AND([switch1], 2, "and1")
not1 = NOT(and1)
or1 = OR([], 2, "OR1")
#esegui_rete_logica()

'''#*and1 non ha più input port libera
or2 = OR([], 2, "OR1")
and1.connect_input_signal_to_input_port(or2, 1)
'''
mod:ModulePort = ModulePort([and1,not1,or1])
#*and1 non ha più input port libera
or2 = OR([], 2, "OR1")
mod.connect_input_signal_to_input_port(or2, 0)

mod1:ModulePort = ModulePort([mod, or2])

print(mod.input_ports_dict)
print("get_number_of_unpiloted_input_signals: " + str(mod.get_number_of_unpiloted_input_signals()))
print("number_of_inputs: " + str(mod.number_of_inputs))
print(mod1.input_ports_dict)
print("get_number_of_unpiloted_input_signals: " + str(mod1.get_number_of_unpiloted_input_signals()))
print("number_of_inputs: " + str(mod1.number_of_inputs))
