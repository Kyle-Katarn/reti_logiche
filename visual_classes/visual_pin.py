import GLOBAL_VARIABLES as GV
from reti_logiche import *
import pygame
from typing import TYPE_CHECKING
from math import sqrt
if TYPE_CHECKING:
    from .visual_gate import VisualGate
    from .visual_connection import VisualConnection


class VisualPin:
    CONST_hitbox_scaling:int = 2
    def __init__(self, father_visual_gate:"VisualGate", logic_gate_index:int, offset_x:int, offset_y:int, rad:int, type:str):
        self.type:str = type
        self.pin_of_visual_connections_set:set[VisualConnection] = set()
        self.logic_gate_index:int = logic_gate_index
        self.father_visual_gate:"VisualGate" = father_visual_gate
        #^^Avere una reference serve a evitare di dover riassegnare manualmente le coordinate ogni volta che sposto la VisualGate, forse era meglio avere una ref al padre? si era meglio
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.radious = rad
        self.color = GV.BLACK

    def visual_pin_conains_point(self, px: int, py: int):
        Dx:int = px-(self.father_visual_gate.x+self.offset_x)
        Dy:int = py-(self.father_visual_gate.y+self.offset_y)
        return sqrt(Dx**2 + Dy**2) <= self.radious * self.CONST_hitbox_scaling

    def draw(self, screen):
        if(self.type == "in"):
            self.color = GV.RED if self.father_visual_gate.gate.get_input_signal_value(self.logic_gate_index) else GV.BLACK
        else:
            self.color = GV.RED if self.father_visual_gate.gate.get_output_signal_value(self.logic_gate_index) else GV.BLACK
        pygame.draw.circle(screen, self.color, (self.father_visual_gate.x+self.offset_x, self.father_visual_gate.y+self.offset_y), self.radious)

    def get_coordinates(self):
        return (self.father_visual_gate.x+self.offset_x, self.father_visual_gate.y+self.offset_y)
    
    def unconnect_logic_pin(self):
        if(self.type == "in"):
            self.father_visual_gate.gate.remove_input_gate(self.logic_gate_index)
        else:
            print("self.type == out, non ho considerato il caso in cui si elimina un output MANUALMENTE")

    def connect_logic_pin(self, input_gate_tup:tuple[LogicClass, int]):
        if(self.type == "in"):
            self.father_visual_gate.gate.connect_input_gate_to_input_signal(input_gate_tup, self.logic_gate_index)
        else:
            print("self.type == out, non ho considerato il caso in cui si aggiunge un output MANUALMENTE")