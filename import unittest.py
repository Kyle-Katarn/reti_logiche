import unittest

from reti_logiche import (
    run_simulation,
    GLOBAL_ALL_GATES_LIST,
    GLOBAL_ALL_SWITCHES_LIST,
    SwitchGate,
    AND,
    OR,
    ModuleGate
)

class TestRetiLogiche(unittest.TestCase):
    def setUp(self):
        # Clear the global lists before each test to avoid interference
        GLOBAL_ALL_GATES_LIST.clear()
        GLOBAL_ALL_SWITCHES_LIST.clear()

    def test_and_gate_behavior(self):
        # Create two switches starting with True
        s1 = SwitchGate(True)
        s2 = SwitchGate(True)
        # Create an AND gate with s1 and s2 as inputs
        and_gate = AND([(s1, 0), (s2, 0)])
        
        # Run simulation to propagate the signals
        run_simulation(max_iterations=5, considered_gates={and_gate}, considered_switches=[s1, s2])
        self.assertTrue(and_gate.get_output_signal_value(), "AND gate should output True when both inputs are True")
        
        # Toggle one switch to make it False
        s1.toggle()
        run_simulation(max_iterations=5, considered_gates={and_gate}, considered_switches=[s1, s2])
        self.assertFalse(and_gate.get_output_signal_value(), "AND gate should output False when one input is False")

    def test_module_gate_with_or_internal(self):
        # Create a switch with True value
        s = SwitchGate(True)
        # Create an OR gate with single input
        or_gate = OR([(s, 0)], n_input_signals=1)
        # Create a ModuleGate wrapping the OR gate as internal gate, with one input and one output
        mod = ModuleGate([or_gate], 1, 1)
        # Link the module's input to the internal OR gate input
        mod.set_module_gate_input_signal_to_internal_gate_input_signal((or_gate, 0), 0)
        # Link the module's output to the internal OR gate output
        mod.set_output_signal_to_llg_output_signal((or_gate, 0), 0)
        
        # Connect the module to a switch as external input
        mod.connect_input_gate_to_input_signal((or_gate, 0), 0)
        or_gate.connect_input_gate_to_input_signal((s, 0), 0)
        
        run_simulation(max_iterations=5, considered_gates={or_gate, mod}, considered_switches=[s])
        self.assertTrue(mod.get_output_signal_value(0), "Module output should be True when input switch is True")
        
        # Change the switch signal
        s.toggle()
        run_simulation(max_iterations=5, considered_gates={or_gate, mod}, considered_switches=[s])
        self.assertFalse(mod.get_output_signal_value(0), "Module output should be False when input switch is toggled to False")

if __name__ == "__main__":
    unittest.main()