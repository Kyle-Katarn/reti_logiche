from CONST import *
from reti_logiche import *
from .visual_gate import *
from .visual_pin import *


class VisualConnection:
    def __init__(self):
        self.color = YELLOW
        self.is_self_in_connections_chosen_for_action_set:bool = False#Needed to determine the color
        self.start_pin:VisualPin = None
        self.end_pin:VisualPin = None
        self.start_x =0
        self.start_y =0
        self.end_x =0
        self.end_y =0
        self.hitbox_length = 5
        self.is_connection_finalized:bool = False
        #^^distingue il caso in cui ha un pin a null perchè non hai ancora selezionato il secondo con mouse
        #dal caso in cui lo start_pin (assieme alla sua VisualGate madre) viene eliminato dall'utente -> la connection deve essere eliminata a catena 
        #is_connection_finalized = TRUE, quando viene selezionato il 2^pin
    def set_coordinates(self, start = None, end = None):
        if(start != None):
            self.start_x, self.start_y = start
        if(end != None):
            self.end_x, self.end_y = end

    def set_pin(self, pin:"VisualPin"):
        if(pin.type == "out"):#todo FIX errore uscita---->entrata
            self.start_pin = pin
            self.start_pin.pin_of_visual_connections_set.add(self)
        else:#type = in
            if(pin.pin_of_visual_connections_set != set()):#todo obbligo refactoring???
                print(f"pin.pin_of_visual_connections_set: {pin.pin_of_visual_connections_set}")
                print("WARNING, rimosso una connessione per coneterne una nuova")
                old_input_pin_connection:VisualConnection = next(iter(pin.pin_of_visual_connections_set))
                old_input_pin_connection.remove_self()

            self.end_pin = pin
            self.end_pin.pin_of_visual_connections_set.add(self)
            #self.get_end_pin_visual_gate().visual_connections.add(self)#!!!
            self.connect_logic_pins()
                

    def auto_update_connection(self):
        if(self.start_pin == None and self.end_pin == None):
            raise Exception(f"@VISUAL ERROR: self.start_pin={self.start_pin} or self.end_pin={self.end_pin} is NONE")
        if(self.start_pin != None):
            self.start_x, self.start_y = self.start_pin.get_coordinates()
        if(self.end_pin != None):
            self.end_x, self.end_y= self.end_pin.get_coordinates()
        
    def draw(self, screen):
        if(self.start_pin and self.end_pin):
            self.is_connection_finalized = True
        if(self.is_connection_finalized and (not self.start_pin.father_visual_gate in GLOBAL_visual_gates)):#!MOLTO GOOFY ma non so come rimuovere la classe in altro modo
            self.remove_self()
        if(self.is_connection_finalized):
            self.auto_update_connection()
        if(self.start_pin):
            if(self.is_self_in_connections_chosen_for_action_set):
                self.color = GREEN
            elif(not self.is_connection_finalized):
                self.color = YELLOW
            else:
                self.color = self.start_pin.color
            #print(f"self.start_pin.color: {self.start_pin.color}")
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y), 2)

    def remove_self(self):
        print(f"gate: {self.get_end_pin_visual_gate().gate}")
        #self.get_end_pin_visual_gate().visual_connections.remove(self)#!!!
        self.start_pin.pin_of_visual_connections_set.remove(self)
        self.end_pin.pin_of_visual_connections_set.remove(self)#!da errore
        self.unconnect_logic_pins()

    def connect_logic_pins(self):
        #print("connect_logic_pins NON FA NULLA")
        self.end_pin.connect_logic_pin((self.start_pin.father_visual_gate.gate, self.start_pin.logic_gate_index))

    def unconnect_logic_pins(self):
        #print("unconnect_logic_pins NON FA NULLA")
        self.end_pin.unconnect_logic_pin()#rimuove l'input gate
        pass

    def get_end_pin_visual_gate(self):
        return self.end_pin.father_visual_gate

    def is_visual_connection_clicked(self, px: int, py: int):
        # Calculate the distance from the point to the line segment
        line_dx = self.end_x - self.start_x
        line_dy = self.end_y - self.start_y
        length_squared = line_dx ** 2 + line_dy ** 2

        if length_squared == 0:
            # The line segment is actually a point
            distance = sqrt((px - self.start_x) ** 2 + (py - self.start_y) ** 2)
        else:
            # Project point onto the line segment and calculate the distance
            t = max(0, min(1, ((px - self.start_x) * line_dx + (py - self.start_y) * line_dy) / length_squared))
            projection_x = self.start_x + t * line_dx
            projection_y = self.start_y + t * line_dy
            distance = sqrt((px - projection_x) ** 2 + (py - projection_y) ** 2)

        return distance <= self.hitbox_length