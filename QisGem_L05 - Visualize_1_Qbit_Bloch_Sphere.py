# 1. Import necessary components
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt # Needed to display the plot

# We'll use the statevector simulator to get the state vector
simulator_sv = Aer.get_backend('statevector_simulator')

# --- Example 1: Initial State |0> ---
qc0 = QuantumCircuit(1) # Start with |0>

# Get the state vector
job0 = simulator_sv.run(qc0)
result0 = job0.result()
statevector0 = result0.get_statevector(qc0)

# Plot the state vector on the Bloch Sphere
print("Bloch Sphere for state |0>:")
plot_bloch_multivector(statevector0)
plt.show() # Display the plot

# --- Example 2: State after Hadamard Gate (H|0> = |+>) ---
qc_h = QuantumCircuit(1)
qc_h.h(0) # Apply Hadamard

# Get the state vector
job_h = simulator_sv.run(qc_h)
result_h = job_h.result()
statevector_h = result_h.get_statevector(qc_h)

# Plot the state vector
print("\nBloch Sphere for state H|0> (|+>):")
plot_bloch_multivector(statevector_h)
plt.show() # Display the plot

# --- Example 3: State after X Gate (X|0> = |1>) ---
qc_x = QuantumCircuit(1)
qc_x.x(0) # Apply Pauli-X

# Get the state vector
job_x = simulator_sv.run(qc_x)
result_x = job_x.result()
statevector_x = result_x.get_statevector(qc_x)

# Plot the state vector
print("\nBloch Sphere for state X|0> (|1>):")
plot_bloch_multivector(statevector_x)
plt.show() # Display the plot

# --- Example 4: State after HZ Gates (HZ|0> = H|0>-|1> = |->) ---
qc_hz = QuantumCircuit(1)
qc_hz.h(0) # Apply H
qc_hz.z(0) # Apply Z

# Get the state vector
job_hz = simulator_sv.run(qc_hz)
result_hz = job_hz.result()
statevector_hz = result_hz.get_statevector(qc_hz)

# Plot the state vector
print("\nBloch Sphere for state HZ|0> (|->):")
plot_bloch_multivector(statevector_hz)
plt.show() # Display the plot