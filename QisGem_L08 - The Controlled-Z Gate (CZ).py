# 1. Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer # Use Aer provider

# Get the qasm simulator backend from Aer
simulator_qasm = Aer.get_backend('qasm_simulator')

# --- Example: H-CZ-H vs CNOT ---
# We expect the final counts to be the same for both circuits

# Circuit 1: CNOT (control=0, target=1) - Creates a Bell state from |00>
qc_cnot = QuantumCircuit(2, 2)
qc_cnot.h(0)
qc_cnot.cx(0, 1)
qc_cnot.measure([0, 1], [0, 1])

print("CNOT Circuit:")
print(qc_cnot.draw(output='text'))

# Transpile and run CNOT
transpiled_cnot = transpile(qc_cnot, simulator_qasm)
job_cnot = simulator_qasm.run(transpiled_cnot, shots=1000)
result_cnot = job_cnot.result()
counts_cnot = result_cnot.get_counts(qc_cnot)
print("\nMeasurement Results (Counts) for CNOT:", counts_cnot)
# Expected: roughly 500x '00', 500x '11' (Bell state |00>+|11>)


# Circuit 2: H on target, CZ, H on target (Equivalent to CNOT, control=0, target=1)
qc_hczh = QuantumCircuit(2, 2)
qc_hczh.h(0)   # Apply H to control (qubit 0) - creates superposition
qc_hczh.cz(0, 1) # Apply CZ gate (control=0, target=1)
qc_hczh.h(1)   # Apply H to target (qubit 1) - undoes the basis change for measurement
qc_hczh.measure([0, 1], [0, 1])

print("\nH-CZ-H Circuit:")
print(qc_hczh.draw(output='text'))

# Transpile and run H-CZ-H
transpiled_hczh = transpile(qc_hczh, simulator_qasm)
job_hczh = simulator_qasm.run(transpiled_hczh, shots=1000)
result_hczh = job_hczh.result()
counts_hczh = result_hczh.get_counts(qc_hczh)
print("\nMeasurement Results (Counts) for H-CZ-H:", counts_hczh)
# Expected: should be very similar to CNOT counts