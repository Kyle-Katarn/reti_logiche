from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from reti_logiche import *

class Assembler:
    def __init__(self):
        self.text_to_binary_instruction_dict: dict[str, str] = {}
        self.binary_instructions_list: list[list[str]] = []
        self.next_instruction_ix: int = 0

    def process_text_to_binary_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                line = line.strip()
                if '>' in line:
                    before, after = line.split('>', 1)
                    print("Before:", before, "| After:", after)
                    self.text_to_binary_instruction_dict[before] = after
                else:
                    print("Line doesn't contain '>':", line)

    def process_instructions_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as infile:
            index: int = 0
            for line in infile:
                line = line.strip()
                self.binary_instructions_list[index].extend(line.split(' ', -1))
                index += 1

    def execute_next_instruction(self, gate:LogicClass):
        #gate.set_signals(..)
        self.next_instruction_ix +=1
    
