from typing import Dict

ports_to_execute:"Port" =  []
set_child_ports_pins: list[callable] = [] 
'''
the pins of the ports that are children of the "ports_to_execute" of a level of the BFS are set ath the END of the level
(when all ports of ports_to_execute have been executed)
'''

all_ports_list:"Port" = []

class Port:
    def __init__(self, name: str = "Port"):
        all_ports_list.append(self)
        self.name: str = name
        self.result: bool = False
        self.output_to_ports: set[Port] = set()
        
    def execute(self):
        print("Executing port: ", self.name, " |result: ", self.result)
        for child_port in self.output_to_ports:
            ports_to_execute.append(child_port) #aggiungi la porta figlia alla lista delle porte da eseguire al livello N+1
            set_child_ports_pins.append(child_port.set_pin_values) #self.pin_1 = self.pin_1_Port.result
    
    def set_pin_values(self):
        pass

    def __str__(self):
        return f"{self.name} (result: {self.result})"
    


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
        pin_1_Port.output_to_ports.add(self)
        pin_2_Port.output_to_ports.add(self)
        
    def execute(self):
        self.result = self.pin_1 and self.pin_2 #Calcola il risultato -> setta pin1 e pin2 delle porte della list output_to_ports
        super().execute()

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
        pin_1_Port.output_to_ports.add(self)
        pin_2_Port.output_to_ports.add(self)
        
    def execute(self):
        self.result = self.pin_1 or self.pin_2
        super().execute()

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
        pin_1_Port.output_to_ports.add(self)
        pin_2_Port.output_to_ports.add(self)
        
    def execute(self):
        self.result = not (self.pin_1 and self.pin_2)
        super().execute()

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
        pin_1_Port.output_to_ports.add(self)
        pin_2_Port.output_to_ports.add(self)
        
    def execute(self):
        self.result = not (self.pin_1 or self.pin_2)
        super().execute()

    def set_pin_values(self):
        self.pin_1 = self.pin_1_Port.result
        self.pin_2 = self.pin_2_Port.result

class NOT(Port):
    def __init__(self, pin_1_Port:Port, name: str = "NOT"):
        super().__init__()
        self.name = name
        self.pin: bool = False
        self.pin_1_Port:Port = pin_1_Port
        pin_1_Port.output_to_ports.add(self)
        
    def execute(self):
        self.result = not self.pin
        super().execute()

    def set_pin_values(self):
        self.pin = self.pin_1_Port.result

#setti la porta in input ad un pin di B, A contiene B nella lista delle porte di output


dict_port_to_BFS_level: Dict[Port, int] = {} #porta è il suo livello nella BFS, True e False sono al livello 0

true_obj = PortTrue()
false_obj = PortFalse()
ports_to_execute.append(true_obj)
ports_to_execute.append(false_obj)

not1 = NOT(true_obj)
not2 = NOT(false_obj)

print("////////////////////////////////////////////////////////////////////////")

number_of_ports_in_a_level:int = len(ports_to_execute)
level:int = 0
print("Level: ", level)

while(not len(ports_to_execute) == 0):
    current_port:Port = ports_to_execute.pop(0)
    current_port.execute()
    dict_port_to_BFS_level[current_port] = level
    number_of_ports_in_a_level -= 1

    if number_of_ports_in_a_level == 0:
        level += 1
        print("Level: ", level)
        for set_pins in set_child_ports_pins:
            set_pins()
        number_of_ports_in_a_level = len(ports_to_execute)

print("all ports list", all_ports_list)




