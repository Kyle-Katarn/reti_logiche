import unittest
from reti_logiche import SwitchGate, XOR, AND, ModuleGate, run_simulation, GLOBAL_ALL_GATES_LIST, GLOBAL_ALL_SWITCHES_LIST

class TestHalfAdder(unittest.TestCase):
    def setUp(self):
        GLOBAL_ALL_GATES_LIST.clear()
        GLOBAL_ALL_SWITCHES_LIST.clear()

    def test_half_adder(self):
        # Create inputs
        a = SwitchGate(False, "A")
        b = SwitchGate(False, "B")
        # Internal gates: XOR for sum, AND for carry
        xor_gate = XOR([(a, 0), (b, 0)], n_input_signals=2, name="XOR")
        and_gate = AND([(a, 0), (b, 0)], n_input_signals=2, name="AND")
        # Create the half-adder module with two inputs and two outputs
        half_adder = ModuleGate([xor_gate, and_gate], number_of_inputs=2, number_of_outputs=2, name="HalfAdder")
        # Link module inputs to internal gates:
        half_adder.set_module_gate_input_signal_to_internal_gate_input_signal((xor_gate, 0), 0, "in0")
        half_adder.set_module_gate_input_signal_to_internal_gate_input_signal((and_gate, 0), 0, "in1")
        half_adder.set_module_gate_input_signal_to_internal_gate_input_signal((xor_gate, 1), 1, "in0")
        half_adder.set_module_gate_input_signal_to_internal_gate_input_signal((and_gate, 1), 1, "in1")
        # Link module outputs:
        half_adder.set_module_gate_output_signal_to_internal_gate_output_signal((xor_gate, 0), 0, "sum")
        half_adder.set_module_gate_output_signal_to_internal_gate_output_signal((and_gate, 0), 1, "carry")

        half_adder.connect_input_gate_to_input_signal((a,0),0)
        half_adder.connect_input_gate_to_input_signal((b,0),1)
        
        # Combination 0: A=False, B=False => sum=False, carry=False
        run_simulation(max_iterations=5, considered_gates={half_adder}, considered_switches=[a, b])
        self.assertFalse(half_adder.get_output_signal_value(0), "Sum should be False for A=False, B=False")
        self.assertFalse(half_adder.get_output_signal_value(1), "Carry should be False for A=False, B=False")
        
        # Combination 1: A=True, B=False => sum=True, carry=False
        a.toggle()
        run_simulation(max_iterations=5, considered_gates={half_adder}, considered_switches=[a, b])
        self.assertTrue(half_adder.get_output_signal_value(0), "Sum should be True for A=True, B=False")
        self.assertFalse(half_adder.get_output_signal_value(1), "Carry should be False for A=True, B=False")
        
        # Combination 2: A=False, B=True => sum=True, carry=False
        a.toggle()  # Set A False
        b.toggle()  # Set B True
        run_simulation(max_iterations=5, considered_gates={half_adder}, considered_switches=[a, b])
        self.assertTrue(half_adder.get_output_signal_value(0), "Sum should be True for A=False, B=True")
        self.assertFalse(half_adder.get_output_signal_value(1), "Carry should be False for A=False, B=True")
        
        # Combination 3: A=True, B=True => sum=False, carry=True
        a.toggle()  # Now A becomes True (B remains True)
        run_simulation(max_iterations=5, considered_gates={half_adder}, considered_switches=[a, b])
        self.assertFalse(half_adder.get_output_signal_value(0), "Sum should be False for A=True, B=True")
        self.assertTrue(half_adder.get_output_signal_value(1), "Carry should be True for A=True, B=True")

if __name__ == "__main__":
    unittest.main()
