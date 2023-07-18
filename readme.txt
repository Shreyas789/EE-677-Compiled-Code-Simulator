The simulator works for any number of inputs and outputs, and any combination of gates. Each gate can have two or more inputs.

Write the netlist file (netlist.txt) according to format:
gate_type:gate_variable input1 input2 input3 and so on
(note the spaces)

The gate output gets stored in gate_variable for each gate
The gate types allowed are "IN", "AND", "OR, "NAND", "NOR", "XOR"
Output gates will be inferred by the code and need not have explicit mention. Just write them as normal gates. Please make sure that an undefined gate variable is not used as input to a gate.

Write inputs.txt with all test vectors which you want to simulate with the circuit, basically a Tracefile

Open Terminal, navigate to the project folder using cd command
run the command: python simulator.py

outputs.txt file will be generated

The ipynb notebook for the entire code (functions) is also added to the folder. The functions for simulation are written in my_functions.py and are imported at the beginning of the simulator.py run.
