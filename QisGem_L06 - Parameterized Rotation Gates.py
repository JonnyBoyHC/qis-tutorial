# 1. Import necessary components
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np # For using pi (np.pi)

# Get the statevector simulator
simulator_sv = Aer.get_backend('statevector_simulator')

# --- Example 1: Ry(pi/2) on |0> ---
# This rotation around the Y axis by pi/2 (90 degrees) takes |0> to |+>
qc_ry = QuantumCircuit(1)
qc_ry.ry(np.pi/2, 0) # Apply Ry(pi/2) gate to qubit 0

# Get state vector and plot
job_ry = simulator_sv.run(qc_ry)
result_ry = job_ry.result()
statevector_ry = result_ry.get_statevector(qc_ry)

print("Bloch Sphere after Ry(pi/2) on |0>:")
plot_bloch_multivector(statevector_ry)
plt.show() # Should look like the |+> state (arrow on positive X axis)


# --- Example 2: Rz(pi/2) on |+> ---
# We first create the |+> state using H or Ry(pi/2), then apply Rz
qc_rz = QuantumCircuit(1)
qc_rz.h(0) # Create |+> state
qc_rz.rz(np.pi/2, 0) # Apply Rz(pi/2) gate to qubit 0

# Get state vector and plot
job_rz = simulator_sv.run(qc_rz)
result_rz = job_rz.result()
statevector_rz = result_rz.get_statevector(qc_rz)

print("\nBloch Sphere after H and Rz(pi/2) on |0>:")
plot_bloch_multivector(statevector_rz)
plt.show() # Should look like a state on the equator rotated by 90 deg from positive X


# --- Example 3: Rx(pi) on |0> ---
# A rotation by pi (180 degrees) around X axis is equivalent to the X gate
qc_rx = QuantumCircuit(1)
qc_rx.rx(np.pi, 0) # Apply Rx(pi) gate to qubit 0

# Get state vector and plot
job_rx = simulator_sv.run(qc_rx)
result_rx = job_rx.result()
statevector_rx = result_rx.get_statevector(qc_rx)

print("\nBloch Sphere after Rx(pi) on |0>:")
plot_bloch_multivector(statevector_rx)
plt.show() # Should look like the |1> state (arrow pointing down)