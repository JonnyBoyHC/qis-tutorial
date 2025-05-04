# 1. Import necessary components
from qiskit import QuantumCircuit
# Import the Aer provider from the qiskit_aer package
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np # Often useful when working with statevectors

# 2. Create the circuit
qc_sv = QuantumCircuit(1) # No classical bits needed for statevector simulation

# 3. Apply the Hadamard gate
qc_sv.h(0)

# 4. Visualize the circuit
print("Statevector Simulator Example Circuit (Hadamard):")
print(qc_sv.draw(output='text'))

# 5. Get the statevector simulator backend from Aer
simulator_sv = Aer.get_backend('statevector_simulator')

# 6. Run the circuit on the statevector simulator
# The statevector simulator doesn't use transpile in the same way for this basic case
# and doesn't need shots.
job_sv = simulator_sv.run(qc_sv)

# 7. Get the result, which is the statevector
result_sv = job_sv.result()
statevector = result_sv.get_statevector(qc_sv)

# 8. Print and interpret the statevector
print("\nStatevector:", statevector)

# For 1 qubit, the basis states are |0> and |1>
# The statevector is [amplitude_of_0, amplitude_of_1]

amplitude_0 = statevector[0]
amplitude_1 = statevector[1]

print(f"Amplitude of |0> state: {amplitude_0}")
print(f"Amplitude of |1> state: {amplitude_1}")

# Probability of measuring 0 is |amplitude_0|^2
prob_0 = np.abs(amplitude_0)**2
# Probability of measuring 1 is |amplitude_1|^2
prob_1 = np.abs(amplitude_1)**2

print(f"Probability of measuring 0: {prob_0:.4f}")
print(f"Probability of measuring 1: {prob_1:.4f}")



# ======================== OLD ======================== #
# # 1. Import necessary components
# from qiskit import QuantumCircuit
# from qiskit.providers.basic_provider import BasicProvider
# from qiskit.quantum_info import Statevector
# import numpy as np # Often useful when working with statevectors

# # 2. Create the circuit
# qc_sv = QuantumCircuit(1) # No classical bits needed for statevector simulation

# # 3. Apply the Hadamard gate
# qc_sv.h(0)

# # 4. Visualize the circuit
# print("Statevector Simulator Example Circuit (Hadamard):")
# print(qc_sv.draw(output='text'))

# # 5. Run the circuit on the statevector simulator
# provider = BasicProvider()
# # Note: We use 'statevector_simulator' backend
# simulator_sv = provider.get_backend('statevector_simulator')

# # The statevector simulator doesn't use transpile in the same way or need shots
# job_sv = simulator_sv.run(qc_sv)

# # Get the result, which is the statevector
# result_sv = job_sv.result()
# statevector = result_sv.get_statevector(qc_sv)

# # Print the statevector
# print("\nStatevector:", statevector)

# # We can interpret the statevector
# # For 1 qubit, the basis states are |0> and |1>
# # The statevector is [amplitude_of_0, amplitude_of_1]

# amplitude_0 = statevector[0]
# amplitude_1 = statevector[1]

# print(f"Amplitude of |0> state: {amplitude_0}")
# print(f"Amplitude of |1> state: {amplitude_1}")

# # Probability of measuring 0 is |amplitude_0|^2
# prob_0 = np.abs(amplitude_0)**2
# # Probability of measuring 1 is |amplitude_1|^2
# prob_1 = np.abs(amplitude_1)**2

# print(f"Probability of measuring 0: {prob_0:.4f}")
# print(f"Probability of measuring 1: {prob_1:.4f}")