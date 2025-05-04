# 1. Import necessary components
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt # Needed to display the plot

# We'll use the statevector simulator to get the state vector
simulator_sv = Aer.get_backend('statevector_simulator')

# --- Example 1: Initial State HH|0> ---
qc_hh = QuantumCircuit(1) # Start with |0>
qc_hh.h(0)
qc_hh.h(0)

# Get the state vector
job_hh = simulator_sv.run(qc_hh)
result_hh = job_hh.result()
statevector_hh = result_hh.get_statevector(qc_hh)

# Plot the state vector on the Bloch Sphere
print("Bloch Sphere for state HH|0>:")
plot_bloch_multivector(statevector_hh)
plt.show() # Display the plot

# --- Example 2: Initial State HZH|0> ---
qc_hzh = QuantumCircuit(1) # Start with |0>
qc_hzh.h(0)
qc_hzh.z(0)
qc_hzh.h(0)

# Get the state vector
job_hzh = simulator_sv.run(qc_hzh)
result_hzh = job_hzh.result()
statevector_hzh = result_hzh.get_statevector(qc_hzh)

# Plot the state vector on the Bloch Sphere
print("Bloch Sphere for state HZH|0>:")
plot_bloch_multivector(statevector_hzh)
plt.show() # Display the plot

# --- Example 3: Initial State XYZ|0> ---
qc_xyz = QuantumCircuit(1) # Start with |0>
qc_xyz.x(0)
qc_xyz.y(0)
qc_xyz.z(0)


# Get the state vector
job_xyz = simulator_sv.run(qc_xyz)
result_xyz = job_xyz.result()
statevector_xyz = result_xyz.get_statevector(qc_xyz)

# Plot the state vector on the Bloch Sphere
print("Bloch Sphere for state XYZ|0>:")
plot_bloch_multivector(statevector_xyz)
plt.show() # Display the plot