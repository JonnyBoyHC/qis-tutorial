from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator # Using AerSimulator

# --- Parameters ---
N_NODES = 4
M_GHZ_STATES = 4 # e.g., for a 3-bit sum

# --- Qiskit Backend ---
simulator = AerSimulator()

# --- Storing outcomes ---
# Each node will conceptually get these bits.
# In a real system, they'd measure their own qubit from each GHZ
# and find it's the same as others.
# Here, we simulate generating that common bit for each round.
list_of_shared_bits = []

print(f"Simulating QMPC Sum Generation for {N_NODES} nodes, using {M_GHZ_STATES} GHZ states for the sum.")

# --- Main Loop for Sum Bit Generation ---
for m_round in range(M_GHZ_STATES):
    qc = QuantumCircuit(N_NODES, N_NODES)

    # Prepare GHZ state
    qc.h(0)
    for i in range(N_NODES - 1):
        qc.cx(i, i + 1)
    qc.barrier()

    # All nodes measure their qubit
    qc.measure(range(N_NODES), range(N_NODES))

    # Transpile and run
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Outcome is a string like '0000' or '1111'
    outcome_str = list(counts.keys())[0] 
    
    # All nodes would observe the same outcome for their respective bit.
    # We take the outcome of the first qubit as the shared bit for this round.
    shared_bit_for_this_round = outcome_str[0] 
    list_of_shared_bits.append(shared_bit_for_this_round)
    
    print(f"GHZ Round {m_round+1}: Circuit:\n{qc.draw(output='text')}")
    print(f"GHZ Round {m_round+1}: All nodes measured (e.g., Node 1 got '{outcome_str[0]}', Node 2 got '{outcome_str[1]}', ...). Shared bit: {shared_bit_for_this_round}")
    print("-" * 30)

# --- Calculate "Sum" (assuming concatenation and conversion to int) ---
# All nodes would perform this calculation independently using the shared bits.
binary_sum_string = "".join(list_of_shared_bits)
final_sum_value = int(binary_sum_string, 2)

print(f"\nShared bits for sum: {list_of_shared_bits}")
print(f"Binary string for sum: {binary_sum_string}")
print(f"Final 'Sum' (identical for all nodes): {final_sum_value}")

# --- Leader Election Example ---
leader_node_index = final_sum_value % N_NODES # 0-indexed
print(f"Leader selected (0-indexed): Node {leader_node_index}")