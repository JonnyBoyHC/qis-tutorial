# 1. Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicProvider
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# 2. Create a quantum circuit
# We need 2 qubits and 2 classical bits for measurements
qc_bell = QuantumCircuit(2, 2)

# 3. Apply gates to create the Bell state
# Apply Hadamard to the first qubit (qubit 0)
qc_bell.h(0)

# Apply CNOT gate with qubit 0 as control and qubit 1 as target
qc_bell.cx(0, 1) # cx is the method for CNOT

# 4. Add measurements
# Measure qubit 0 into classical bit 0
qc_bell.measure(0, 0)
# Measure qubit 1 into classical bit 1
qc_bell.measure(1, 1)

# 5. Visualize the circuit
print("Bell State Circuit:")
circuit_drawer(qc_bell, output='mpl', idle_wires=False) # idle_wires=False hides unused lines
plt.show()

# 6. Run the circuit on a simulator
provider = BasicProvider()
simulator = provider.get_backend('basic_simulator')

# Transpile the circuit
transpiled_circuit_bell = transpile(qc_bell, simulator)

# Run the circuit (e.g., 1000 shots)
job_bell = simulator.run(transpiled_circuit_bell, shots=1000)

# Get the results
result_bell = job_bell.result()
counts_bell = result_bell.get_counts(qc_bell)

# Print the results
print("\nMeasurement Results (Counts):", counts_bell)