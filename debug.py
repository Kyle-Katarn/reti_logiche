from __future__ import annotations
import inspect
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui import *
    from reti_logiche import *


def print_stack():
    stack_length:int = len(inspect.stack())

    print(f"\n@@@PRINT STACK of function: {inspect.stack()[1].function}")
    for ix in range(2, stack_length):
        caller = inspect.stack()[ix]  # Get the caller's stack frame
        caller_function = caller.function  # Get the function name
        caller_filename = caller.filename  # Get the filename
        caller_line = caller.lineno  # Get the line number
        print(f"Called by function: {caller_function}, in file: {caller_filename}, at line: {caller_line}")
    print()


def connection_debugger(logic_gate:LogicClass):
    print("")
    input_visual_gate:VisualGate = dict_logic_to_visual_gates[logic_gate]
    visual_connections_set:set[VisualConnection] = input_visual_gate.get_all_visual_connections()

    if(len(visual_gate.visual_input_pins) != 0):
        print(f"Input pins of {visual_gate.gate.name}")
        for ivp in visual_gate.visual_input_pins:
            print(f"input pin {ivp}")

    if(len(visual_connections_set) == 0):
        print(f"NO connections point to {logic_gate.name}")
    for vc in visual_connections_set:
        print(f"#@visual connection: {vc}")
        start_pin:VisualPin = vc.start_pin
        end_pin:VisualPin = vc.end_pin
        print(f"start_pin: {start_pin}")
        print(f"    start_pin father: {start_pin.father_visual_gate.gate.name} | start_pin_type: {start_pin.type} | start_pin_ix: {start_pin.logic_gate_index} | start_pin_color: {start_pin.color}")
        print(f"end_pin: {end_pin}")
        print(f"    end_pin father: {end_pin.father_visual_gate.gate.name} | end_pin_type: {end_pin.type} | end_pin_ix: {end_pin.logic_gate_index} | end_pin_color: {end_pin.color}")
        print("")