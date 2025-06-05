from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QMPCNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.measured_bits_for_sum = [] # Bits this node measures/derives for the sum

    def record_shared_bit(self, bit):
        self.measured_bits_for_sum.append(bit)

    def calculate_sum(self):
        if not self.measured_bits_for_sum:
            return 0
        binary_sum_string = "".join(self.measured_bits_for_sum)
        return int(binary_sum_string, 2)

    def reset(self):
        self.measured_bits_for_sum = []

class SumOfColumnsSimulator:
    def __init__(self, num_nodes, num_ghz_states_for_sum):
        self.num_nodes = num_nodes
        self.num_ghz_states_for_sum = num_ghz_states_for_sum
        self.nodes = [QMPCNode(node_id=i) for i in range(num_nodes)]
        self.q_simulator = AerSimulator()
        self.last_circuit_diagram = None # For inspection

    def _prepare_ghz_circuit_for_one_round(self):
        # N qubits for N nodes, N classical bits for their measurements
        qc = QuantumCircuit(self.num_nodes, self.num_nodes, name=f"GHZ_Round")
        qc.h(0)
        for i in range(self.num_nodes - 1):
            qc.cx(i, i + 1)
        qc.barrier(label="GHZ_Prepared")
        return qc

    def _run_simulation_round(self, qc, eavesdrop_qubit_index=None):
        """
        Runs one round of GHZ distribution and measurement.
        If eavesdrop_qubit_index is specified, an eavesdropper measures that qubit
        before legitimate nodes measure.
        """
        if eavesdrop_qubit_index is not None and 0 <= eavesdrop_qubit_index < self.num_nodes:
            # Eavesdropper measures one qubit before others
            # We need a separate classical bit for the eavesdropper if we want to record its outcome
            # For simplicity, we just add the measurement operation.
            # Note: Qiskit might reorder qubits if classical bits aren't mapped carefully.
            # For this demo, we'll just insert the measurement.
            # A more robust way would be to add an extra classical bit for the eavesdropper.
            qc.measure(eavesdrop_qubit_index, eavesdrop_qubit_index) # Eavesdropper measures into its "own" bit line for simplicity
            qc.barrier(label=f"Eavesdrop_Q{eavesdrop_qubit_index}")

        # All legitimate nodes measure their respective qubits
        qc.measure(range(self.num_nodes), range(self.num_nodes))
        self.last_circuit_diagram = qc.draw(output='text') # Save for printing

        compiled_circuit = transpile(qc, self.q_simulator)
        job = self.q_simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Outcome is a string like '0000' or '1111' (if no tampering and ideal GHZ)
        # In Qiskit, classical bits are typically ordered from right to left in the string.
        # So, classical_bit[0] is the rightmost char.
        outcome_str_qiskit_ordered = list(counts.keys())[0]
        # Let's reverse it to match qubit index order (qubit 0 = node 0)
        outcome_str = outcome_str_qiskit_ordered[::-1]

        return outcome_str

    def generate_shared_sum(self, enable_eavesdropping_on_round=None, eavesdropped_qubit=0):
        """
        enable_eavesdropping_on_round: 0-indexed round number for tampering.
        eavesdropped_qubit: The qubit index the eavesdropper targets.
        """
        print(f"\n--- Starting Sum Generation ({self.num_ghz_states_for_sum} rounds) ---")
        if enable_eavesdropping_on_round is not None:
            print(f"WARNING: Eavesdropping enabled on round {enable_eavesdropping_on_round+1} on qubit {eavesdropped_qubit}")

        # Reset nodes for a new sum generation
        for node in self.nodes:
            node.reset()

        all_nodes_agree_on_all_bits = True
        generated_shared_bits = [] # For conceptual global view of what the bits *should* be

        for m_round in range(self.num_ghz_states_for_sum):
            print(f"\nRound {m_round + 1}/{self.num_ghz_states_for_sum}:")
            qc = self._prepare_ghz_circuit_for_one_round()
            
            eavesdrop_this_round = True if m_round == enable_eavesdropping_on_round else False
            
            measurement_outcomes_str = self._run_simulation_round(
                qc, 
                eavesdrop_qubit_index=eavesdropped_qubit if eavesdrop_this_round else None
            )
            print(f"Circuit for Round {m_round+1}:\n{self.last_circuit_diagram}")
            print(f"Raw measurement outcome string (Node0,Node1,...): '{measurement_outcomes_str}'")

            # In an ideal untampered GHZ state, all bits in measurement_outcomes_str are the same.
            # This is the "shared bit" for this round.
            # If tampered, they might not be!
            
            current_round_shared_bit_candidate = measurement_outcomes_str[0] # Tentative shared bit from Node 0's measurement
            round_bits_consistent = True
            for i in range(self.num_nodes):
                if measurement_outcomes_str[i] != current_round_shared_bit_candidate:
                    round_bits_consistent = False
                    break
            
            if not round_bits_consistent:
                all_nodes_agree_on_all_bits = False
                print(f"TAMPERING/ERROR DETECTED in round {m_round+1}: Node measurements are inconsistent: {measurement_outcomes_str}")
                # In a real protocol, nodes might abort or trigger a different procedure here.
                # For simulation, we'll still have them record their *own* bit.
                # The fact their final sums won't match is the "detection."
            else:
                print(f"Bits consistent this round. Shared bit: '{current_round_shared_bit_candidate}'")

            generated_shared_bits.append(current_round_shared_bit_candidate) # Ideal shared bit

            # Each node records its own measured bit from the outcome string
            for i, node in enumerate(self.nodes):
                node.record_shared_bit(measurement_outcomes_str[i])
        
        # Calculate and display sums for each node
        final_sums = []
        print("\n--- Final Sum Calculation ---")
        for node in self.nodes:
            s = node.calculate_sum()
            final_sums.append(s)
            print(f"Node {node.node_id}: Measured bits: {node.measured_bits_for_sum}, Calculated Sum: {s}")

        # Verify if all sums are identical
        if len(set(final_sums)) == 1:
            print(f"\nSUCCESS: All nodes calculated the same sum: {final_sums[0]}")
            final_agreed_sum = final_sums[0]
            # Leader Election
            leader_node_index = final_agreed_sum % self.num_nodes
            print(f"Leader selected (0-indexed): Node {leader_node_index}")
            return final_agreed_sum, leader_node_index
        else:
            print(f"\nFAILURE/TAMPERING DETECTED: Node sums are different: {final_sums}")
            print("This indicates that the entanglement was likely disturbed or an error occurred.")
            return None, None

# --- Simulation Parameters ---
N_NODES = 4
M_GHZ_STATES = 4 # 4 bits for the sum

# --- Run Ideal Scenario ---
print("*************************")
print("* IDEAL SCENARIO      *")
print("*************************")
simulator_ideal = SumOfColumnsSimulator(num_nodes=N_NODES, num_ghz_states_for_sum=M_GHZ_STATES)
ideal_sum, ideal_leader = simulator_ideal.generate_shared_sum()

# --- Run Tampering Scenario ---
print("\n\n*************************")
print("* TAMPERING SCENARIO   *")
print("*************************")
simulator_tampered = SumOfColumnsSimulator(num_nodes=N_NODES, num_ghz_states_for_sum=M_GHZ_STATES)
# Eavesdrop on the 2nd round (index 1), targeting the first node's qubit (index 0)
tampered_sum, tampered_leader = simulator_tampered.generate_shared_sum(enable_eavesdropping_on_round=1, eavesdropped_qubit=2)