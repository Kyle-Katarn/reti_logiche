from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_PORTS_LIST:list['AbstractPort'] = []

class AbstractPort:
    def __init__(self, name: str = "AbstractPort"):
        GLOBAL_ALL_PORTS_LIST.append(self)
        self.name: str = name
        self.result: bool = False
        self.child_ports_list: set['AbstractPort'] = set()
        self.input_ports_list:list['AbstractPort'] = []
        self.input_values:list[bool] = []
        self.number_of_inputs:int = 0

    def add_child_port(self, child_port:'AbstractPort'):
        self.child_ports_list.add(child_port)
    
    def compute_result(self):
        pass

    def __str__(self):
        return "Name: "+ self.name + " -> " + str(self.result)
    
    def set_pin_values(self):
        pass

    def get_child_ports_list(self):
        return self.child_ports_list
    
    def get_number_of_inputs(self):
        return self.number_of_inputs


class PortTrue(AbstractPort):
    def __init__(self, name: str = "TRUE"):
        super().__init__(name)
        self.result = True


class PortFalse(AbstractPort):
    def __init__(self, name: str = "FALSE"):
        super().__init__(name)
        self.result = False


class PortWithInputs(AbstractPort):
    def __init__(self, name:str = "PortWithInput"):
        super().__init__(name)
        self.number_of_inputs:int = 0
    
    def get_input_ports_list(self):
        return self.input_ports_list


class ModulePort(AbstractPort):
    def __init__(self, internal_ports_list:list[PortWithInputs], input_ports_list:list[AbstractPort], name = "ModulePort"):
        super().__init__(name)
        self.internal_ports_list = internal_ports_list
        self.input_ports_list = input_ports_list
        self.link_internal_ports_and_input_ports()

        self.output_internal_ports_list = [] #porte interne che mandano il segnale all'esterno
        for port in self.internal_ports_list:
            if port.get_child_ports_list() == []:
                self.output_internal_ports_list.append(port)
        

    def print_first_level_internal_ports(self):
        print("First level internal ports:")
        for port in self.internal_ports_list:
            if port.get_input_ports_list() == []:
                print(port)
    
    def print_last_level_internal_ports(self):
        print("Last level internal ports:")
        for ix, port in enumerate(self.internal_ports_list):
            if port.get_child_ports_list() == []:
                print(f"Index: {ix}, Port: {port}")

    def link_internal_ports_and_input_ports(self):
        input_ports_ix:int = 0
        for port in self.internal_ports_list:
            if port.get_input_ports_list() == []:
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

    def out(self, ix:int):
        return self.output_internal_ports_list_copy[ix]


class BasicPort(AbstractPort):
    def __init__(self, input_ports_list:list['AbstractPort'], name: str = "BasicPort"):
        super().__init__(name)
        self.add_input_ports(input_ports_list)

    def add_input_ports(self, input_ports_list:list['AbstractPort']):
        for port in input_ports_list:
            port.add_child_port(self)
        self.input_ports_list.extend(input_ports_list)
        self.number_of_inputs += len(input_ports_list)
        self.input_values.extend([False for _ in range(len(input_ports_list))])

    def set_pin_values(self):
        for i, port in enumerate(self.input_ports_list):
            self.input_values[i] = port.result

    def get_input_ports_list(self):
        return self.input_ports_list
    

class AND(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort], name: str = "AND"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = True
        for value in self.input_values:
            self.result = self.result and value

class OR(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort], name: str = "OR"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = False
        for value in self.input_values:
            self.result = self.result or value

class NAND(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort], name: str = "NAND"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = True
        for value in self.input_values:
            self.result = self.result and value
        self.result = not self.result

class NOR(BasicPort):
    def __init__(self, input_ports_list:list[AbstractPort], name: str = "NOR"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = False
        for value in self.input_values:
            self.result = self.result or value
        self.result = not self.result

class NOT(BasicPort):
    def __init__(self, input_port:AbstractPort, name: str = "NOT"):
        super().__init__([input_port], name)
        
    def compute_result(self):
        self.result = not self.input_values[0]

#setti la porta in input ad un pin di B, A contiene B nella lista delle porte di output

def esegui_rete_logica(max_iterations:int = 10, rete_logica:list[AbstractPort] = None):#se non passo la rete logica, eseguo tutte le porte
    current_level_ports:set[AbstractPort] = set()
    next_level_ports:set[AbstractPort] = set()
    current_level_ports.add(GlOBAL_TRUE)
    current_level_ports.add(GlOBAL_FALSE)
    current_level_ports_copy = current_level_ports.copy()
    level:int = 0
    iterations:int = 0  
    print("Level: ", level)

    while len(current_level_ports) >0 and iterations < max_iterations:
        iterations += 1
        current_port = current_level_ports.pop()
        next_level_ports.update(current_port.get_child_ports_list())
        current_port.compute_result()
        print(current_port)

        if len(current_level_ports) == 0:
            level += 1
            if(len(next_level_ports) > 0):
                print("Level: ", level)
            current_level_ports = next_level_ports.copy()
            next_level_ports.clear()
            while len(current_level_ports_copy) > 0:
                current_port = current_level_ports_copy.pop()
                current_port.set_pin_values()

GlOBAL_TRUE = PortTrue()
GlOBAL_FALSE = PortFalse()

and1 = AND([GlOBAL_TRUE, GlOBAL_FALSE, GlOBAL_TRUE], "AND1")
or1 = OR([], "OR1")

esegui_rete_logica()




