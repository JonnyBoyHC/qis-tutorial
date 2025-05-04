# 1. Import necessary components
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np

# 2. Create the Bell state circuit (no classical bits for statevector)
qc_bell_sv = QuantumCircuit(2)

qc_bell_sv.h(0)
qc_bell_sv.cx(0, 1)

# 3. Visualize the circuit
print("\nBell State Circuit (for Statevector Simulator):")
print(qc_bell_sv.draw(output='text'))

# 4. Get the statevector simulator backend from Aer
simulator_sv = Aer.get_backend('statevector_simulator')

# 5. Run on the statevector simulator
job_bell_sv = simulator_sv.run(qc_bell_sv) # Using the same simulator instance
result_bell_sv = job_bell_sv.result()
statevector_bell = result_bell_sv.get_statevector(qc_bell_sv)

# 6. Print and interpret the statevector
print("\nStatevector for Bell State:", statevector_bell)

# Interpret the statevector for 2 qubits
# The basis states are |00>, |01>, |10>, |11>
# The statevector is [amp_00, amp_01, amp_10, amp_11]

amplitude_00 = statevector_bell[0]
amplitude_01 = statevector_bell[1]
amplitude_10 = statevector_bell[2]
amplitude_11 = statevector_bell[3]

print(f"Amplitude of |00> state: {amplitude_00}")
print(f"Amplitude of |01> state: {amplitude_01}")
print(f"Amplitude of |10> state: {amplitude_10}")
print(f"Amplitude of |11> state: {amplitude_11}")

prob_00 = np.abs(amplitude_00)**2
prob_01 = np.abs(amplitude_01)**2
prob_10 = np.abs(amplitude_10)**2
prob_11 = np.abs(amplitude_11)**2

print(f"Probability of measuring 00: {prob_00:.4f}")
print(f"Probability of measuring 01: {prob_01:.4f}")
print(f"Probability of measuring 10: {prob_10:.4f}")
print(f"Probability of measuring 11: {prob_11:.4f}")


# ======================== OLD ======================== #
# # 1. Import necessary components
# from qiskit import QuantumCircuit, transpile
# from qiskit.providers.basic_provider import BasicProvider
# from qiskit.visualization import circuit_drawer
# import matplotlib.pyplot as plt

# # 2. Create a quantum circuit
# # We need 2 qubits and 2 classical bits for measurements
# qc_bell = QuantumCircuit(2, 2)

# # 3. Apply gates to create the Bell state
# # Apply Hadamard to the first qubit (qubit 0)
# qc_bell.h(0)

# # Apply CNOT gate with qubit 0 as control and qubit 1 as target
# qc_bell.cx(0, 1) # cx is the method for CNOT

# # 4. Add measurements
# # Measure qubit 0 into classical bit 0
# qc_bell.measure(0, 0)
# # Measure qubit 1 into classical bit 1
# qc_bell.measure(1, 1)

# # 5. Visualize the circuit
# print("Bell State Circuit:")
# circuit_drawer(qc_bell, output='mpl', idle_wires=False) # idle_wires=False hides unused lines
# plt.show()

# # 6. Run the circuit on a simulator
# provider = BasicProvider()
# simulator = provider.get_backend('basic_simulator')

# # Transpile the circuit
# transpiled_circuit_bell = transpile(qc_bell, simulator)

# # Run the circuit (e.g., 1000 shots)
# job_bell = simulator.run(transpiled_circuit_bell, shots=1000)

# # Get the results
# result_bell = job_bell.result()
# counts_bell = result_bell.get_counts(qc_bell)

# # Print the results
# print("\nMeasurement Results (Counts):", counts_bell)