from CONST import *
from reti_logiche import *
from .visual_connection import *
from .visual_pin import *

class VisualGate:
    def __init__(self, gate: BasicGate, x: int, y: int):
        #self.visual_connections: set[VisualConnection] = set()#!!!
        self.visual_input_pins: list[VisualPin] = []
        self.visual_output_pins: list[VisualPin] = []
        self.gate = gate
        self.x = x 
        self.y = y
        self.color = LIGHTBLUE
        self.width = 100
        # Height based on max between inputs and outputs
        max_pins = max(gate.number_of_inputs, gate.number_of_outputs)
        self.height = max(60, max_pins * 30)
        self.pin_radius = 5
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        #* ISTANZIA CLASSI PIN / input
        if self.gate.number_of_inputs > 0:
            spacing = self.height // (self.gate.number_of_inputs + 1)
            for i in range(self.gate.number_of_inputs):
                y_offset = spacing * (i + 1)
                visual_pin:VisualPin = VisualPin(self, i, 0, y_offset, self.pin_radius, "in")#!maybe coo obj? no just pass the reference of father_class
                self.visual_input_pins.append(visual_pin)
                
        #* / output
        spacing = self.height // (self.gate.number_of_outputs + 1)
        for i in range(self.gate.number_of_outputs):
            y_offset = spacing * (i + 1)
            visual_pin:VisualPin = VisualPin(self, i, self.width, y_offset, self.pin_radius, "out")
            self.visual_output_pins.append(visual_pin)

    #*Gestione SPOSTAMENTO RETTANGOLO
    def visual_gate_contains_point(self, x: int, y: int) -> bool:
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)

    def visual_gate_start_drag(self, mouse_x: int, mouse_y: int):
        self.is_dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y

    def visual_gate_end_drag(self):
        self.is_dragging = False

    def visual_gate_update_position(self, mouse_x: int, mouse_y: int):
        if self.is_dragging:
            self.x = mouse_x - self.drag_offset_x
            self.y = mouse_y - self.drag_offset_y

    #*Gestione SELEZIONE PIN (PIN)
    def check_if_a_visual_pin_is_cicked(self, x: int, y: int):
        selected_pin:VisualPin = None
        all_pins = []
        all_pins.extend(self.visual_input_pins)
        all_pins.extend(self.visual_output_pins)
        for pin in all_pins:
            if pin.visual_pin_conains_point(x,y):
                selected_pin = pin
                break
        return selected_pin
    
    #*Gestione SELEZIONE CONNESSIONE (CONNESSIONE)
    def get_all_visual_connections(self):
        all_connections = set()
        for pin in self.visual_input_pins:
            all_connections.update(pin.pin_of_visual_connections_set)
        return all_connections

    def check_if_a_visual_connection_is_cicked(self, x: int, y: int):
        selected_connection:VisualConnection = None
        for connection in self.get_all_visual_connections():
            if(connection.is_visual_connection_clicked(x,y)):
                selected_connection = connection
                break
        return selected_connection
    
    #*ELIMINAZIONE
    def delete_internal_logic_gate(self):
        try:
            considered_gates.remove(self.gate)
        except:
            print("it is dumb you cant?? remove swithces")#???
        print("MAYBE WORKS, THIS SHOULD REMOVE LOGIC GATE FROM SIM")

    def draw(self, screen):
        # Draw gate body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw gate name
        font = pygame.font.Font(None, 24)
        text = font.render(self.gate.name, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, text_rect)
            
        #* Draw PINS
        for input_pin_ix in range(self.gate.number_of_inputs):
            self.visual_input_pins[input_pin_ix].draw()
        for output_pin_ix in range(self.gate.number_of_outputs):
            self.visual_output_pins[output_pin_ix].draw()

        #* Draw Connections
        for vc in self.get_all_visual_connections():
            vc.draw(screen)