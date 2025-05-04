# Try backend statevector
# Import necessary Qiskit components
from qiskit import QuantumCircuit, transpile
# Import the Aer provider from the qiskit_aer package
from qiskit_aer import Aer

# 1. Create your quantum circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

print("Quantum Circuit:")
print(qc)

# 2. Get the statevector simulator backend from Aer
#    (Make sure qiskit-aer is installed!)
simulator = Aer.get_backend('statevector_simulator')

# 3. Run the simulation
#    Note: Statevector simulator doesn't execute measurements directly,
#    it gives the final statevector *before* measurement.
#    For simulations *with* measurement outcomes, use 'qasm_simulator'.

#    Let's simulate the statevector *before* measurement:
#    Remove the measurement part for statevector simulation
qc_without_measurement = qc.remove_final_measurements(inplace=False)

# Transpile the circuit for the simulator
tqc = transpile(qc_without_measurement, simulator)

# Run and get the statevector
job = simulator.run(tqc)
result = job.result()
statevector = result.get_statevector(tqc)

print("\nFinal Statevector:")
print(statevector)

# If you wanted simulation with measurement counts, use qasm_simulator:
qasm_simulator = Aer.get_backend('qasm_simulator')
tqc_measure = transpile(qc, qasm_simulator) # Use original circuit with measurements
job_qasm = qasm_simulator.run(tqc_measure, shots=1024) # Specify number of shots
result_qasm = job_qasm.result()
counts = result_qasm.get_counts(tqc_measure)

print("\nSimulation Counts (using qasm_simulator):")
print(counts)