# Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicProvider
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# Create a circuit with Y gate
qc_y = QuantumCircuit(1, 1)
qc_y.y(0) # Apply Pauli-Y gate to qubit 0
qc_y.measure(0, 0)

print("\nPauli-Y Gate Circuit:")
# circuit_drawer(qc_y, output='text')
circuit_drawer(qc_y, output='mpl')
plt.show()

provider = BasicProvider()
simulator = provider.get_backend("basic_simulator")

transpiled_circuit_y = transpile(qc_y, simulator)
job_y = simulator.run(transpiled_circuit_y, shots=1000)
result_y = job_y.result()
counts_y = result_y.get_counts(qc_y)

print("\nMeasurement Results (Counts) after Y on |0>:", counts_y)