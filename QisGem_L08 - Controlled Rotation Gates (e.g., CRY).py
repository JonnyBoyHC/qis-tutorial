# 1. Import necessary components
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

# Get the statevector simulator
simulator_sv = Aer.get_backend('statevector_simulator')

# --- Example: CRY(pi/2) with control in superposition ---
# Start with |00>
# Apply H to qubit 0 (control) -> state is (|0>+|1>)/sqrt(2) tensored with |0> = (|00> + |10>)/sqrt(2)
# Apply CRY(pi/2) with control 0, target 1
# If control is |0>, target remains |0> -> term |00>
# If control is |1>, target gets Ry(pi/2) -> |1> tensored with Ry(pi/2)|0> = |1> tensored with (|0> + i|1>)/sqrt(2)
# Resulting state is (|00> + |1>tensored with (|0> + i|1>)/sqrt(2))/sqrt(2) = (|00> + |10> + i|11>)/sqrt(2) -- Wait, math check.

# Let's re-calculate the state after CRY(pi/2)
# Initial state: |00>
# After H on qubit 0: (|0> + |1>)/sqrt(2) |0> = ( |00> + |10> ) / sqrt(2)

# Apply CRY(pi/2) (control=0, target=1):
# The |00> part: Control is |0>, target is |0>. CRY does nothing. Stays |00>.
# The |10> part: Control is |1>, target is |0>. CRY applies Ry(pi/2) to target.
# Ry(pi/2) on |0> gives (|0> + i|1>)/sqrt(2).
# So |10> becomes |1> tensored with (|0> + i|1>)/sqrt(2) = (|10> + i|11>)/sqrt(2).

# Combining the parts:
# ( |00> + (|10> + i|11>)/sqrt(2) ) / sqrt(2)
# = ( |00|*sqrt(2) + |10> + i|11> ) / 2

# Let's try Ry(pi) instead, which is simpler and equivalent to CNOT when applied conditionally.
# CRY(pi) with control 0, target 1
# Initial state: |00>
# After H on qubit 0: (|00> + |10>)/sqrt(2)
# Apply CRY(pi) (control 0, target 1):
# |00> part: Control is |0>, stays |00>.
# |10> part: Control is |1>, apply Ry(pi) to target |0>. Ry(pi)|0> = -i|1>.
# So |10> becomes |1> tensored with (-i|1>) = -i|11>.
# Combined state: (|00> - i|11>)/sqrt(2). This is another type of entangled Bell state!

# Let's code the CRY(pi) example
qc_cry = QuantumCircuit(2) # 2 qubits, no classical bits needed

qc_cry.h(0)      # Put control in superposition
qc_cry.cry(np.pi, 0, 1) # Apply CRY(pi) with control 0, target 1

print("\nCRY(pi) Circuit with control in superposition:")
print(qc_cry.draw(output='text'))

# Get state vector and plot (plot_bloch_multivector can show 2 qubits but is harder to interpret)
job_cry = simulator_sv.run(qc_cry)
result_cry = job_cry.result()
statevector_cry = result_cry.get_statevector(qc_cry)

print("\nStatevector after CRY(pi) on |00> with H on qubit 0:", statevector_cry)
# Expected statevector: [1/sqrt(2), 0, 0, -i/sqrt(2)] which is approx [0.707, 0, 0, -0.707j]

# Let's also try visualizing the statevector. For 2 qubits, it's not a single point on a sphere,
# plot_bloch_multivector shows the state of each qubit *individually*, ignoring entanglement,
# but it can still be somewhat illustrative.
print("\nBloch Sphere visualization (per qubit) for entangled state after CRY(pi):")
plot_bloch_multivector(statevector_cry)
plt.show() # Note: This visualization doesn't show entanglement!

# --- Example: CRZ(pi/2) on |+0> ---
# Similar to Rz(pi/2) on |+>, but controlled.
# Initial state |00>
# H on qubit 0 -> (|00> + |10>)/sqrt(2)
# CRZ(pi/2) control 0, target 1
# |00> part: Control is |0>, target is |0>. CRZ does nothing. Stays |00>.
# |10> part: Control is |1>, target is |0>. Apply Rz(pi/2) to target |0>. Rz(pi/2)|0> = |0>.
# Hmm, Rz on |0> doesn't change it. Let's try CRZ(pi/2) on |+> and |1>.
# Initial state |01>
# H on qubit 0 -> (|01> + |11>)/sqrt(2)
# CRZ(pi/2) control 0, target 1
# |01> part: Control is |0>, target is |1>. CRZ does nothing. Stays |01>.
# |11> part: Control is |1>, target is |1>. Apply Rz(pi/2) to target |1>. Rz(pi/2)|1> = i|1>.
# So |11> becomes |1> tensored with i|1> = i|11>.
# Combined state: (|01> + i|11>)/sqrt(2). This is another entangled state.

# Let's code the CRZ(pi/2) example
qc_crz = QuantumCircuit(2) # 2 qubits

qc_crz.x(1)      # Set target qubit 1 to |1>
qc_crz.h(0)      # Put control qubit 0 in superposition (|0> -> |+>)
qc_crz.crz(np.pi/2, 0, 1) # Apply CRZ(pi/2) with control 0, target 1

print("\nCRZ(pi/2) Circuit with control in superposition and target in |1>:")
print(qc_crz.draw(output='text'))

# Get state vector
job_crz = simulator_sv.run(qc_crz)
result_crz = job_crz.result()
statevector_crz = result_crz.get_statevector(qc_crz)

print("\nStatevector after CRZ(pi/2) on |01> with H on qubit 0:", statevector_crz)
# Expected statevector: [0, 1/sqrt(2), 0, i/sqrt(2)] which is approx [0, 0.707, 0, 0.707j]