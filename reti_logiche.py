from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_PORTS_LIST:"Port" = []

class Port:
    def __init__(self, input_ports_list:list['Port'], name: str = "Port"):
        GLOBAL_ALL_PORTS_LIST.append(self)
        self.name: str = name
        self.result: bool = False
        self.child_ports_list: set[Port] = set()
        self.input_ports_list:list[Port] = input_ports_list
        self.input_values:list[bool] = [False for _ in range(len(input_ports_list))]

        for port in input_ports_list:
            port.child_ports_list.add(self)

    def add_input_ports(self, input_ports_list:list['Port']):
        for port in input_ports_list:
            port.child_ports_list.add(self)
        self.input_ports_list.extend(input_ports_list)
        self.input_values.extend([False for _ in range(len(input_ports_list))])

    def get_child_ports_list(self):
        return self.child_ports_list
    
    def compute_result(self):
        pass

    def set_pin_values(self):
        ix:int = 0
        for port in self.input_ports_list:
            self.input_values[ix] = port.result
            ix += 1

    def __str__(self):
        return "Name: "+ self.name + " -> " + str(self.result)

    


class PortTrue(Port):
    def __init__(self, name: str = "TRUE"):
        super().__init__([], name)
        self.result = True

class PortFalse(Port):
    def __init__(self, name: str = "FALSE"):
        super().__init__([], name)
        self.result = False


class AND(Port):
    def __init__(self, input_ports_list:list[Port], name: str = "AND"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = True
        for value in self.input_values:
            self.result = self.result and value



class OR(Port):
    def __init__(self, input_ports_list:list[Port], name: str = "OR"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = False
        for value in self.input_values:
            self.result = self.result or value

class NAND(Port):
    def __init__(self, input_ports_list:list[Port], name: str = "NAND"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = True
        for value in self.input_values:
            self.result = self.result and value
        self.result = not self.result

class NOR(Port):
    def __init__(self, input_ports_list:list[Port], name: str = "NOR"):
        super().__init__(input_ports_list, name)
        
    def compute_result(self):
        self.result = False
        for value in self.input_values:
            self.result = self.result or value
        self.result = not self.result

class NOT(Port):
    def __init__(self, input_port:Port, name: str = "NOT"):
        super().__init__([input_port], name)
        
    def compute_result(self):
        self.result = not self.input_values[0]

#setti la porta in input ad un pin di B, A contiene B nella lista delle porte di output

def esegui_rete_logica(max_iterations:int = 10, rete_logica:list[Port] = None):#se non passo la rete logica, eseguo tutte le porte
    current_level_ports:set[Port] = set()
    next_level_ports:set[Port] = set()
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
esegui_rete_logica()




