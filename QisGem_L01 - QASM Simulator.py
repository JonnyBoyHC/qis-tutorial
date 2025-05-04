# Corrected Single Hadamard Circuit (QASM Simulator)
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer # Use Aer provider
from qiskit.visualization import circuit_drawer

# Create circuit
qc_h_qasm = QuantumCircuit(1, 1)
qc_h_qasm.h(0)
qc_h_qasm.measure(0, 0)

print("\nCorrected Hadamard Circuit (QASM Simulator):")
circuit_drawer(qc_h_qasm, output='text')

# Get the qasm simulator backend from Aer
simulator_qasm = Aer.get_backend('qasm_simulator')

# Transpile and run
transpiled_circuit_h_qasm = transpile(qc_h_qasm, simulator_qasm)
job_h_qasm = simulator_qasm.run(transpiled_circuit_h_qasm, shots=1000)
result_h_qasm = job_h_qasm.result()
counts_h_qasm = result_h_qasm.get_counts(qc_h_qasm)

print("\nMeasurement Results (Counts) after H on |0> (QASM Simulator):", counts_h_qasm)

# Corrected Bell State Circuit (QASM Simulator)
qc_bell_qasm = QuantumCircuit(2, 2)
qc_bell_qasm.h(0)
qc_bell_qasm.cx(0, 1)
qc_bell_qasm.measure(0, 0)
qc_bell_qasm.measure(1, 1)

print("\nCorrected Bell State Circuit (QASM Simulator):")
circuit_drawer(qc_bell_qasm, output='text', idle_wires=False)

# Get the qasm simulator backend from Aer
# simulator_qasm is already defined above

# Transpile and run
transpiled_circuit_bell_qasm = transpile(qc_bell_qasm, simulator_qasm)
job_bell_qasm = simulator_qasm.run(transpiled_circuit_bell_qasm, shots=1000)
result_bell_qasm = job_bell_qasm.result()
counts_bell_qasm = result_bell_qasm.get_counts(qc_bell_qasm)

print("\nMeasurement Results (Counts) for Bell State (QASM Simulator):", counts_bell_qasm)




# ======================== OLD ======================== #
# # 1. Import necessary components from Qiskit
# from qiskit import QuantumCircuit, transpile
# from qiskit.providers.basic_provider import BasicProvider
# from qiskit.visualization import circuit_drawer
# import matplotlib.pyplot as plt

# # 2. Create a quantum circuit
# # We need 1 qubit and 1 classical bit to store the measurement result
# qc = QuantumCircuit(1, 1)

# # 3. Apply a quantum gate
# # The Hadamard gate (H) puts the qubit in a superposition state
# qc.h(0) # Apply Hadamard gate to qubit 0

# # 4. Add a measurement
# # Measure qubit 0 and store the result in classical bit 0
# qc.measure(0, 0)

# # 5. Visualize the circuit (Optional but helpful!)
# # This will draw the circuit diagram
# circuit_drawer(qc, output='mpl') # You can try 'mpl' for a graphical output if you have matplotlib installed
# plt.show()

# # Now let's run the circuit!
# # We'll use a basic simulator for now.3
# provider = BasicProvider()
# simulator = provider.get_backend('basic_simulator')

# # Transpile the circuit for the simulator
# # This step optimizes the circuit for the specific backend
# transpiled_circuit = transpile(qc, simulator)

# # Run the circuit on the simulator
# # We run it multiple times (shots) to see the probabilities
# job = simulator.run(transpiled_circuit, shots=1000)

# # Get the results
# result = job.result()
# counts = result.get_counts(qc)

# # Print the results
# print("\nMeasurement Results (Counts):", counts)
# print("==========================================")
# print(result)