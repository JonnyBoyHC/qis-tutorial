# 1. Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer # Use Aer provider

# Get the qasm simulator backend from Aer
simulator_qasm = Aer.get_backend('qasm_simulator')

# --- Example 1: Toffoli gate on |110> ---
# Controls are |1>, Target is |0>. Target should flip to |1>.
qc_toffoli110 = QuantumCircuit(3, 3) # 3 qubits, 3 classical bits

# Set control qubits to |1> state
qc_toffoli110.x(0) # Qubit 0 to |1>
qc_toffoli110.x(1) # Qubit 1 to |1>
# Qubit 2 starts at |0>, which is our target

qc_toffoli110.barrier() # Optional: Visual separator

# Apply Toffoli gate: controls on 0 and 1, target on 2
qc_toffoli110.ccx(0, 1, 2)

qc_toffoli110.barrier()

# Measure all qubits
qc_toffoli110.measure([0, 1, 2], [0, 1, 2])

print("Toffoli Gate Circuit on |110>:")
print(qc_toffoli110.draw(output='text'))

# Transpile and run
transpiled_toffoli110 = transpile(qc_toffoli110, simulator_qasm)
job_toffoli110 = simulator_qasm.run(transpiled_toffoli110, shots=1000)
result_toffoli110 = job_toffoli110.result()
counts_toffoli110 = result_toffoli110.get_counts(qc_toffoli110)

print("\nMeasurement Results (Counts) for |110> input:", counts_toffoli110)
# Expected: {'111': 1000}

# --- Example 2: Toffoli gate on |010> ---
# Control 0 is |0|, Control 1 is |1|, Target is |0>. Target should NOT flip.
qc_toffoli010 = QuantumCircuit(3, 3)

# Set initial state |010>
# Qubit 0 starts at |0>
qc_toffoli010.x(1) # Qubit 1 to |1>
# Qubit 2 starts at |0> (target)

qc_toffoli010.barrier()

# Apply Toffoli gate
qc_toffoli010.ccx(0, 1, 2)

qc_toffoli010.barrier()

# Measure all qubits
qc_toffoli010.measure([0, 1, 2], [0, 1, 2])

print("\nToffoli Gate Circuit on |010>:")
print(qc_toffoli010.draw(output='text'))

# Transpile and run
transpiled_toffoli010 = transpile(qc_toffoli010, simulator_qasm)
job_toffoli010 = simulator_qasm.run(transpiled_toffoli010, shots=1000)
result_toffoli010 = job_toffoli010.result()
counts_toffoli010 = result_toffoli010.get_counts(qc_toffoli010)

print("\nMeasurement Results (Counts) for |010> input:", counts_toffoli010)
# Expected: {'010': 1000}