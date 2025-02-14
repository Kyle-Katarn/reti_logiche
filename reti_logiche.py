from typing import Dict
'''
Una porta sia aggiunge al livello N se uno dei suoi pin dipende da una porta al livello N-1
NON è necessario che tutti i pin dipendano da porte al livello N-1
'''

GLOBAL_ALL_PORTS_LIST:"Port" = []

class Port:
    def __init__(self, name: str = "Port"):
        GLOBAL_ALL_PORTS_LIST.append(self)
        self.name: str = name
        self.result: bool = False
        self.child_ports_list: set[Port] = set()
        
    def get_child_ports_list(self):
        return self.child_ports_list
    
    def compute_result(self):
        pass

    def set_pin_values(self):
        pass

    def __str__(self):
        return "Name: "+ self.name + " -> " + str(self.result)

    


class PortTrue(Port):
    def __init__(self, name: str = "TRUE"):
        super().__init__()
        self.name = name
        self.result = True

class PortFalse(Port):
    def __init__(self, name: str = "FALSE"):
        super().__init__()
        self.name = name
        self.result = False


class AND(Port):
    def __init__(self, pin_1_Port:Port, pin_2_Port:Port, name: str = "AND"): #le porte di input
        super().__init__()
        self.name = name
        self.pin_1: bool = False
        self.pin_2: bool = False
        self.pin_1_Port:Port = pin_1_Port
        self.pin_2_Port:Port = pin_2_Port
        pin_1_Port.child_ports_list.add(self)
        pin_2_Port.child_ports_list.add(self)
        
    def compute_result(self):
        self.result = self.pin_1 and self.pin_2 #Calcola il risultato -> setta pin1 e pin2 delle porte della list child_ports_list

    def set_pin_values(self):
        self.pin_1 = self.pin_1_Port.result
        self.pin_2 = self.pin_2_Port.result

class OR(Port):
    def __init__(self, pin_1_Port:Port, pin_2_Port:Port, name: str = "OR"):
        super().__init__()
        self.name = name
        self.pin_1: bool = False
        self.pin_2: bool = False
        self.pin_1_Port:Port = pin_1_Port
        self.pin_2_Port:Port = pin_2_Port
        pin_1_Port.child_ports_list.add(self)
        pin_2_Port.child_ports_list.add(self)
        
    def compute_result(self):
        self.result = self.pin_1 or self.pin_2

    def set_pin_values(self):
        self.pin_1 = self.pin_1_Port.result
        self.pin_2 = self.pin_2_Port.result

class NAND(Port):
    def __init__(self, pin_1_Port:Port, pin_2_Port:Port, name: str = "NAND"):
        super().__init__()
        self.name = name
        self.pin_1: bool = False
        self.pin_2: bool = False
        self.pin_1_Port:Port = pin_1_Port
        self.pin_2_Port:Port = pin_2_Port
        pin_1_Port.child_ports_list.add(self)
        pin_2_Port.child_ports_list.add(self)
        
    def compute_result(self):
        self.result = not (self.pin_1 and self.pin_2)

    def set_pin_values(self):
        self.pin_1 = self.pin_1_Port.result
        self.pin_2 = self.pin_2_Port.result

class NOR(Port):
    def __init__(self, pin_1_Port:Port, pin_2_Port:Port, name: str = "NOR"):
        super().__init__()
        self.name = name
        self.pin_1: bool = False
        self.pin_2: bool = False
        self.pin_1_Port:Port = pin_1_Port
        self.pin_2_Port:Port = pin_2_Port
        pin_1_Port.child_ports_list.add(self)
        pin_2_Port.child_ports_list.add(self)
        
    def compute_result(self):
        self.result = not (self.pin_1 or self.pin_2)

    def set_pin_values(self):
        self.pin_1 = self.pin_1_Port.result
        self.pin_2 = self.pin_2_Port.result

class NOT(Port):
    def __init__(self, pin_Port:Port, name: str = "NOT"):
        super().__init__()
        self.name = name
        self.pin: bool = False
        self.pin_Port:Port = pin_Port
        pin_Port.child_ports_list.add(self)
        
    def compute_result(self):
        self.result = not self.pin

    def set_pin_values(self):
        self.pin = self.pin_Port.result

#setti la porta in input ad un pin di B, A contiene B nella lista delle porte di output


dict_port_to_BFS_level: Dict[Port, int] = {} #porta è il suo livello nella BFS, True e False sono al livello 0

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
            if(len(next_level_ports) > 0):
                print("Level: ", level)
            current_level_ports = next_level_ports.copy()
            next_level_ports.clear()
            while len(current_level_ports_copy) > 0:
                current_port = current_level_ports_copy.pop()
                current_port.set_pin_values()




GlOBAL_TRUE = PortTrue()
GlOBAL_FALSE = PortFalse()

and1 = AND(GlOBAL_TRUE, GlOBAL_FALSE, "AND1")
esegui_rete_logica()




