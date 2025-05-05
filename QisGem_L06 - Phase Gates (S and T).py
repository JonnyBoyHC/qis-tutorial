# 1. Import necessary components
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np # For using pi (np.pi)

# Get the statevector simulator
simulator_sv = Aer.get_backend('statevector_simulator')

# --- Example 4: S Gate on |+> ---
qc_s = QuantumCircuit(1)
qc_s.h(0) # Create |+> state
qc_s.s(0) # Apply S gate (equivalent to Rz(pi/2))

# Get state vector and plot
job_s = simulator_sv.run(qc_s)
result_s = job_s.result()
statevector_s = result_s.get_statevector(qc_s)

print("\nBloch Sphere after H and S on |0>:")
plot_bloch_multivector(statevector_s)
plt.show() # Should be the same as the Rz(pi/2) example


# --- Example 5: T Gate on |+> ---
qc_t = QuantumCircuit(1)
qc_t.h(0) # Create |+> state
qc_t.t(0) # Apply T gate (equivalent to Rz(pi/4))

# Get state vector and plot
job_t = simulator_sv.run(qc_t)
result_t = job_t.result()
statevector_t = result_t.get_statevector(qc_t)

print("\nBloch Sphere after H and T on |0>:")
plot_bloch_multivector(statevector_t)
plt.show() # Should be a rotation by 45 deg from positive X on the equator