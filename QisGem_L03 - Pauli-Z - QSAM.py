# Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicProvider
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# Create a circuit to show Z gate effect
qc_z = QuantumCircuit(1, 1)

# Start with |0>, apply H
qc_z.h(0)
# Apply Z
qc_z.z(0)
# Apply H again
qc_z.h(0)

# Measure
qc_z.measure(0, 0)

print("\nPauli-Z Gate Effect (H-Z-H) Circuit:")
# circuit_drawer(qc_z, output='text')
circuit_drawer(qc_z, output='mpl')
plt.show()

# Run the circuit on the simulator
provider = BasicProvider()
simulator = provider.get_backend('basic_simulator')

transpiled_circuit_z = transpile(qc_z, simulator)
job_z = simulator.run(transpiled_circuit_z, shots=1000)
result_z = job_z.result()
counts_z = result_z.get_counts(qc_z)

print("\nMeasurement Results (Counts) after H-Z-H on |0>:", counts_z)