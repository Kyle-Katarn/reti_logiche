def add_input_ports(self, input_ports_param:list[AbstractPort]):
        #!se ci sono più porte di input che input_signals, aggiunge input_signals
        #len_input_ports_dict:int = len(self.input_ports_dict)#indcice del primo input_signal non pilotato
        number_of_unconnected_input_signals:int = self.number_of_inputs - self.number_of_piloted_input_signals
        number_of_extra_input_ports:int = len(input_ports_param) - number_of_unconnected_input_signals
        self.number_of_inputs += max(0, number_of_extra_input_ports)#se passi meno porte di input di quelle necessarie

        
        for input_port in input_ports_param:
            input_port.add_child_port(self)
            self.input_ports_dict[number_of_unconnected_input_signals] = input_port
            number_of_unconnected_input_signals += 1

    def connect_multiple_input_signals_to_input_ports(self, input_ports_param: list[AbstractPort]):
        #!connette le input ports SOLO alle porte già presenti

        #first unpiloated input_signal index
        if(self.number_of_piloted_input_signals + len(input_ports_param) > self.number_of_inputs):
            raise ValueError("ERRORE: porte di input in eccesso, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        if(self.number_of_piloted_input_signals + len(input_ports_param) < self.number_of_inputs):
            print("WARNING: porte di input insufficienti, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        
        param_ix:int =0
        input_signal_ix:int =0
        while(param_ix < len(input_ports_param) and input_signal_ix < self.get_number_of_inputs()):
            if self.input_ports_dict.get(input_signal_ix) == None:
                self.input_ports_dict[input_signal_ix] = input_ports_param[param_ix]
                param_ix +=1
            input_signal_ix +=1


    def connect_input_signal_to_input_port(self, input_port: AbstractPort, input_signal_ix: int):
        if input_signal_ix >= self.number_of_inputs:
            raise IndexError("ERRORE: Input signal index out of range, your index: " + str(input_signal_ix) + " last index: " + (str(self.number_of_inputs)-1))
        self.input_ports_dict[input_signal_ix] = input_port
        input_port.add_child_port(self)



    def connect_multiple_input_signals_to_input_ports(self, input_ports_param: list[AbstractPort]):
        #!connette le input ports SOLO alle porte già presenti
        #first unpiloated input_signal index
        if(self.number_of_piloted_input_signals + len(input_ports_param) > self.number_of_inputs):
            raise ValueError("ERRORE: porte di input in eccesso, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        if(self.number_of_piloted_input_signals + len(input_ports_param) < self.number_of_inputs):
            print("WARNING: porte di input insufficienti, porte di input: " + str(self.number_of_inputs) + " porte di input necessarie: " + str(ix + len(input_ports_param)))
        
        for p in input_ports_param:
            self.input_ports_dict[self.number_of_piloted_input_signals] = p
            self.number_of_piloted_input_signals +=1