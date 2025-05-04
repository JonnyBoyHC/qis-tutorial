# 1. Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicProvider
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# 2. Create a circuit with 1 qubit and 1 classical bit
qc_x = QuantumCircuit(1, 1)

# 3. Apply the X gate to qubit 0
qc_x.x(0) # Apply Pauli-X gate to qubit 0

# 4. Measure the qubit
qc_x.measure(0, 0)

# 5. Visualize the circuit
print("Pauli-X Gate Circuit:")
# circuit_drawer(qc_x, output='text')
circuit_drawer(qc_x, output='mpl')
plt.show()

# 6. Run the circuit on the simulator
provider = BasicProvider()
simulator = provider.get_backend('basic_simulator')

# Transpile and run
transpiled_circuit_x = transpile(qc_x, simulator)
job_x = simulator.run(transpiled_circuit_x, shots=1000)
result_x = job_x.result()
counts_x = result_x.get_counts(qc_x)

# Print results
print("\nMeasurement Results (Counts) after X on |0>:", counts_x)

print("============================================================")

# Create a circuit starting with |1> state
qc_x_on_1 = QuantumCircuit(1, 1)
qc_x_on_1.x(0) # First X gate changes |0> to |1>
qc_x_on_1.barrier() # Optional: Adds a visual separator in the circuit drawing
qc_x_on_1.x(0) # Second X gate changes |1> back to |0>
qc_x_on_1.measure(0, 0)

print("\nPauli-X Gate on |1> Circuit:")
circuit_drawer(qc_x_on_1, output='text')

transpiled_circuit_x_on_1 = transpile(qc_x_on_1, simulator)
job_x_on_1 = simulator.run(transpiled_circuit_x_on_1, shots=1000)
result_x_on_1 = job_x_on_1.result()
counts_x_on_1 = result_x_on_1.get_counts(qc_x_on_1)

print("\nMeasurement Results (Counts) after X on |1>:", counts_x_on_1)