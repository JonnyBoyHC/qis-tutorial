# import cirq
# qubits = [cirq.GridQubit(0, i) for i in range(2)]
# circuit = cirq.Circuit(cirq.H(qubits[0]), cirq.CNOT(*qubits), cirq.measure_each(*qubits))
# print(circuit)

import cirq
import numpy as np

# Define our qubit (LineQubit creates a qubit at position 0)
q = cirq.LineQubit(0)

# Create the circuit
circuit = cirq.Circuit()

# Instead of using an initialize method, we prepare the state (|0>+|1>)/sqrt(2) with a Hadamard gate.
circuit.append(cirq.H(q))

# Apply the Z gate
circuit.append(cirq.Z(q))

# Set up the simulator
simulator = cirq.Simulator()

# Simulate the circuit
result = simulator.simulate(circuit)

# Retrieve the final state vector
final_state = result.final_state_vector

# Define the initial state's coefficients (for display purposes)
alpha = 1 / np.sqrt(2)
beta = 1 / np.sqrt(2)

print("Initial state:", [alpha, beta])
print("Final state after Z gate:", np.around(final_state, 3))
