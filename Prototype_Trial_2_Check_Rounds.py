import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from collections import Counter

class QMPCNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.measured_bits_for_sum = []
        self.chosen_basis_for_check = None # 'Z' or 'X'
        self.outcome_for_check = None    # 0 or 1

    def record_sum_bit(self, bit):
        self.measured_bits_for_sum.append(str(bit)) # Ensure bits are stored as strings

    def choose_random_basis(self):
        self.chosen_basis_for_check = random.choice(['Z', 'X'])
        return self.chosen_basis_for_check

    def calculate_sum(self):
        if not self.measured_bits_for_sum:
            return 0
        binary_sum_string = "".join(self.measured_bits_for_sum)
        if not binary_sum_string: # Handle case where no bits were recorded
            return 0
        return int(binary_sum_string, 2)

    def reset(self):
        self.measured_bits_for_sum = []
        self.chosen_basis_for_check = None
        self.outcome_for_check = None

class SumOfColumnsSimulator:
    def __init__(self, num_nodes, num_ghz_states_for_sum, check_round_frequency=3):
        self.num_nodes = num_nodes
        self.num_total_rounds = num_ghz_states_for_sum # This will now be total rounds, some are checks
        self.check_round_frequency = check_round_frequency # Run a check round every K rounds
        self.actual_sum_bits_collected = 0

        self.nodes = [QMPCNode(node_id=i) for i in range(num_nodes)]
        self.q_simulator = AerSimulator()
        self.last_circuit_diagram = None
        self.eavesdropper_detected_by_check = False


    def _prepare_ghz_circuit_for_one_round(self, round_name="GHZ_Round"):
        qc = QuantumCircuit(self.num_nodes, self.num_nodes, name=round_name)
        qc.h(0)
        for i in range(self.num_nodes - 1):
            qc.cx(i, i + 1)
        qc.barrier(label="GHZ_Prepared")
        return qc

    def _apply_measurement_gates(self, qc, node_bases_choices):
        """Applies measurement gates based on nodes' chosen bases."""
        for i in range(self.num_nodes):
            if node_bases_choices[i] == 'X':
                qc.h(i) # Apply Hadamard for X-basis measurement
            qc.measure(i, i) # Measure qubit i into classical bit i

    def _run_quantum_part(self, qc, eavesdrop_this_round=False, eavesdropped_qubit=0, eavesdropper_basis='Z'):
        """Handles eavesdropping and runs the quantum circuit."""
        if eavesdrop_this_round:
            print(f"    EAVESDROPPER: Measuring qubit {eavesdropped_qubit} in {eavesdropper_basis}-basis before legitimate nodes.")
            if eavesdropper_basis == 'X':
                qc.h(eavesdropped_qubit)
            qc.measure(eavesdropped_qubit, eavesdropped_qubit) # Eavesdropper's measurement
            # Note: This measurement outcome isn't explicitly used by eavesdropper in this simple sim,
            # but the act of measuring disturbs the state.
            qc.barrier(label=f"Eavesdrop_Q{eavesdropped_qubit}")
        
        self.last_circuit_diagram = qc.draw(output='text')
        compiled_circuit = transpile(qc, self.q_simulator)
        job = self.q_simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts(qc)
        outcome_str_qiskit_ordered = list(counts.keys())[0]
        # Standardize outcome string to match node order (Node0, Node1, ...)
        return outcome_str_qiskit_ordered[::-1]


    def _perform_sum_round(self, eavesdrop_this_round=False, eavesdropped_qubit=0, eavesdropper_basis='Z'):
        print("  Type: Sum Bit Generation Round")
        qc = self._prepare_ghz_circuit_for_one_round(round_name="SumRound")
        
        # For sum rounds, all nodes measure in Z basis implicitly by standard measurement
        node_bases_choices = ['Z'] * self.num_nodes 
        # Apply Z-measurements (standard measure operation)
        for i in range(self.num_nodes):
            qc.measure(i,i) # Standard measurement is Z-basis

        measurement_outcomes_str = self._run_quantum_part(qc, eavesdrop_this_round, eavesdropped_qubit, eavesdropper_basis)
        print(f"    Circuit:\n{self.last_circuit_diagram}")
        print(f"    Raw Z-measurement outcomes (N0,N1,...): '{measurement_outcomes_str}'")

        # Check for consistency among legitimate nodes for this sum bit
        shared_bit_candidate = measurement_outcomes_str[0]
        bits_consistent_for_sum = all(bit == shared_bit_candidate for bit in measurement_outcomes_str)

        if bits_consistent_for_sum:
            print(f"    Z-Outcomes consistent. Shared bit candidate for sum: '{shared_bit_candidate}'")
            for node in self.nodes:
                node.record_sum_bit(shared_bit_candidate) # All get the same agreed bit
            self.actual_sum_bits_collected += 1
        else:
            # This implies a very noisy channel or an attack that broke Z-basis correlation badly
            print(f"    ERROR/SEVERE TAMPERING: Z-Outcomes inconsistent for sum bit round: {measurement_outcomes_str}. Sum bit discarded.")
            # No bit is added to the sum if they can't agree on the Z-measurement.
            # This is a basic form of detection even in sum rounds.
        print("-" * 40)


    def _perform_check_round(self, eavesdrop_this_round=False, eavesdropped_qubit=0, eavesdropper_basis='Z'):
        print("  Type: Quantum Disturbance Check Round")
        self.eavesdropper_detected_by_check = False # Reset for this round's check

        qc = self._prepare_ghz_circuit_for_one_round(round_name="CheckRound")
        
        node_bases_choices = [node.choose_random_basis() for node in self.nodes]
        print(f"    Nodes' chosen bases: {[(f'N{i}', basis) for i, basis in enumerate(node_bases_choices)]}")

        # Eavesdropper acts *before* legitimate nodes apply their basis choices and measure.
        # The quantum state passed to _apply_measurement_gates will already be (potentially) disturbed.
        # First, simulate eavesdropper if active
        if eavesdrop_this_round:
            print(f"    EAVESDROPPER: Measuring qubit {eavesdropped_qubit} in {eavesdropper_basis}-basis.")
            temp_qc_for_eavesdrop = qc.copy(name="eavesdrop_temp") # Eavesdropper acts on the GHZ state
            if eavesdropper_basis == 'X':
                temp_qc_for_eavesdrop.h(eavesdropped_qubit)
            temp_qc_for_eavesdrop.measure(eavesdropped_qubit, eavesdropped_qubit) # Eavesdropper measures
            temp_qc_for_eavesdrop.barrier(label=f"Eavesdrop_Q{eavesdropped_qubit}")
            # The state of 'qc' is implicitly affected by this measurement on the shared quantum state
            # For simulation, Qiskit executes sequentially. So, we apply eavesdropper ops to the main qc.
            if eavesdropper_basis == 'X':
                qc.h(eavesdropped_qubit)
            qc.measure(eavesdropped_qubit, 0) # Eavesdropper measures (e.g. into classical bit 0, it will be overwritten)
            # This is a simplification: the key is the disturbance. For a more accurate sim of eavesdropper's info,
            # they'd have their own classical bit. Here, we focus on state disturbance.
            # Let's simply say the disturbance happened. More accurate would be to run the eavesdropper's part first.
            # For a simpler flow here, let's assume the _run_quantum_part handles this:
            # The eavesdropper's measurement is added to the circuit *before* legitimate nodes' measurements.
            
        # Legitimate nodes apply their chosen basis gates and measure
        self._apply_measurement_gates(qc, node_bases_choices)
        
        measurement_outcomes_str = self._run_quantum_part(qc, eavesdrop_this_round, eavesdropped_qubit, eavesdropper_basis)
        # Note: if eavesdropping is enabled in _run_quantum_part, it applies *another* eavesdrop op.
        # This needs to be structured carefully. Let's refine _run_quantum_part to take a fully formed qc.
        # For now, let's assume eavesdropping for check round is handled before _apply_measurement_gates.
        # The current _run_quantum_part adds its own eavesdrop logic. Let's simplify.

        # Re-simplifying the eavesdropping for check rounds:
        # The GHZ state is prepared.
        # If eavesdropping: eavesdropper measures. The state of qc is now collapsed/disturbed.
        # Then, legitimate nodes apply their basis choices and measure this (potentially) disturbed state.

        qc_check = self._prepare_ghz_circuit_for_one_round(round_name="CheckRound_Internal") # Fresh circuit for clarity
        # Simulate eavesdropper's action on this circuit state
        eavesdropper_outcome_for_check = None
        if eavesdrop_this_round:
            print(f"    EAVESDROPPER (Check Round): Measuring qubit {eavesdropped_qubit} in {eavesdropper_basis}-basis.")
            if eavesdropper_basis == 'X':
                qc_check.h(eavesdropped_qubit)
            # Eavesdropper measures into a dummy classical bit (e.g. the first one, it will be overwritten by node 0)
            # This is just to enact the measurement and state collapse.
            qc_check.measure(eavesdropped_qubit, 0) 
            qc_check.barrier(label=f"E_Q{eavesdropped_qubit}")
            # We don't run this sub-circuit, its purpose is to modify qc_check for the legitimate nodes.

        # Nodes choose bases and apply gates to qc_check
        for i in range(self.num_nodes):
            if node_bases_choices[i] == 'X':
                qc_check.h(i)
            qc_check.measure(i, i)

        # Now run the modified qc_check
        self.last_circuit_diagram = qc_check.draw(output='text') # Save for printing
        compiled_circuit_check = transpile(qc_check, self.q_simulator)
        job_check = self.q_simulator.run(compiled_circuit_check, shots=1)
        result_check = job_check.result()
        counts_check = result_check.get_counts(qc_check)
        outcome_str_qiskit_ordered_check = list(counts_check.keys())[0]
        measurement_outcomes_str = outcome_str_qiskit_ordered_check[::-1] # (N0,N1,...)

        print(f"    Circuit (Check Round):\n{self.last_circuit_diagram}")
        print(f"    Measured outcomes (N0,N1,...): {measurement_outcomes_str} for bases {node_bases_choices}")

        # Store outcomes for nodes
        for i, node in enumerate(self.nodes):
            node.outcome_for_check = int(measurement_outcomes_str[i])
            node.chosen_basis_for_check = node_bases_choices[i]

        # Verification logic
        # 1. Z-basis checks: nodes that chose 'Z' should have identical outcomes
        z_basis_nodes_outcomes = [(i, node.outcome_for_check) for i, node in enumerate(self.nodes) if node.chosen_basis_for_check == 'Z']
        if len(z_basis_nodes_outcomes) > 1:
            first_z_outcome = z_basis_nodes_outcomes[0][1]
            if not all(outcome == first_z_outcome for _, outcome in z_basis_nodes_outcomes):
                print(f"    TAMPERING DETECTED (Check Round): Z-basis outcomes inconsistent: {z_basis_nodes_outcomes}")
                self.eavesdropper_detected_by_check = True
        
        # 2. X-basis checks: for nodes that chose 'X', parity of outcomes should be even
        x_basis_nodes_outcomes = [node.outcome_for_check for node in self.nodes if node.chosen_basis_for_check == 'X']
        if len(x_basis_nodes_outcomes) >= 1: # For GHZ, even one X measurement provides info if others are Z
                                            # For simplicity: if 2+ nodes pick X, check their joint parity
            if len(x_basis_nodes_outcomes) >= 2: # Stronger check with more X-basis measurements
                parity = sum(x_basis_nodes_outcomes) % 2
                if parity != 0: # For GHZ: N0+N1+...+Nk = 0 (mod 2) if all measure in X
                                # If a subset measure in X, this rule is more complex.
                                # Simplified: if all participating in X-check have non-zero parity sum
                    print(f"    TAMPERING DETECTED (Check Round): X-basis outcomes parity is ODD: {x_basis_nodes_outcomes} -> Sum = {sum(x_basis_nodes_outcomes)}")
                    self.eavesdropper_detected_by_check = True
        
        if not self.eavesdropper_detected_by_check:
            print("    Check Round: No inconsistencies detected in chosen bases.")
        print("-" * 40)
        return not self.eavesdropper_detected_by_check


    def generate_shared_sum(self, total_rounds, enable_eavesdropping_overall=False, eavesdropper_basis='Z', eavesdropped_qubit_idx=0):
        print(f"\n--- Starting Protocol: {total_rounds} total rounds ---")
        print(f"--- Check rounds will occur approx every {self.check_round_frequency} sum rounds ---")
        if enable_eavesdropping_overall:
            print(f"WARNING: Eavesdropping enabled. E-basis: {eavesdropper_basis}, E-qubit target: Q{eavesdropped_qubit_idx}")

        # Reset nodes and simulator state
        for node in self.nodes:
            node.reset()
        self.eavesdropper_detected_by_check = False
        self.actual_sum_bits_collected = 0
        
        sum_round_counter = 0
        for r_idx in range(total_rounds + 1):
            print(f"\nOverall Round {r_idx + 1}/{total_rounds}:")
            
            # Decide if this is a check round
            is_check_this_round = (sum_round_counter > 0 and sum_round_counter % self.check_round_frequency == 0)
            
            eavesdrop_attempt_this_round = enable_eavesdropping_overall # Eavesdropper tries every round if enabled

            if is_check_this_round:
                if not self._perform_check_round(eavesdrop_attempt_this_round, eavesdropped_qubit_idx, eavesdropper_basis):
                    # Eavesdropper was detected by the check round
                    print("    PROTOCOL ABORT SUGGESTED: Eavesdropper detected by check round.")
                    # Depending on policy, might halt or just note detection and continue cautiously
                    break # For this simulation, let's halt if a check fails
                sum_round_counter = 0 # Reset counter after a check
            else:
                if self.eavesdropper_detected_by_check: # If detected in a *previous* check round
                    print("    Skipping sum bit generation: Eavesdropper previously detected by a check round.")
                    # Optionally, could break here too or run dummy rounds
                else:
                    self._perform_sum_round(eavesdrop_attempt_this_round, eavesdropped_qubit_idx, eavesdropper_basis)
                    sum_round_counter += 1
            
            if self.actual_sum_bits_collected >= self.num_total_rounds: # Target number of sum bits achieved
                 print(f"Target number of {self.num_total_rounds} sum bits collected.")
                 break


        # Final Sum Calculation and Leader Election (only if no eavesdropper detected by checks)
        final_sums = []
        print("\n--- Final Sum Calculation ---")
        if self.eavesdropper_detected_by_check:
            print("Sums not calculated/trusted due to earlier eavesdropper detection by check round.")
            return None, None

        for node in self.nodes:
            s = node.calculate_sum()
            final_sums.append(s)
            print(f"Node {node.node_id}: Measured sum bits: {node.measured_bits_for_sum}, Calculated Sum: {s}")

        if not final_sums: # e.g. if protocol aborted early
            print("No sum bits were successfully collected by nodes.")
            return None, None

        # Verify if all sums are identical (they should be if sum bits were recorded consistently)
        if len(set(final_sums)) == 1:
            final_agreed_sum = final_sums[0]
            print(f"\nSUCCESS: All nodes calculated the same sum: {final_agreed_sum}")
            leader_node_index = final_agreed_sum % self.num_nodes
            print(f"Leader selected (0-indexed): Node {leader_node_index}")
            return final_agreed_sum, leader_node_index
        else:
            print(f"\nERROR/INCONSISTENCY: Node sums are different: {final_sums}")
            print("This might be due to an undetected issue or severe noise during sum bit rounds.")
            return None, None


# --- Simulation Parameters ---
N_NODES = 4
TARGET_SUM_BITS = 4  # Desired number of bits for the final sum
CHECK_FREQUENCY = 2 # Run a check round after every 2 sum rounds
TOTAL_ROUNDS_TO_RUN = TARGET_SUM_BITS + (TARGET_SUM_BITS // CHECK_FREQUENCY) # Approximate total rounds

# --- Run Ideal Scenario (No Eavesdropping) ---
print("*********************************************")
print("* IDEAL SCENARIO (with Check Rounds)        *")
print("*********************************************")
simulator_ideal = SumOfColumnsSimulator(num_nodes=N_NODES, num_ghz_states_for_sum=TARGET_SUM_BITS, check_round_frequency=CHECK_FREQUENCY)
simulator_ideal.generate_shared_sum(total_rounds=TOTAL_ROUNDS_TO_RUN, enable_eavesdropping_overall=False)

# --- Run Tampering Scenario (Eavesdropper Present) ---
print("\n\n*****************************************************")
print("* TAMPERING SCENARIO (Eavesdropper, with Check Rounds) *")
print("*****************************************************")
# Eavesdropper always tries to measure qubit 0 in Z-basis
simulator_tampered = SumOfColumnsSimulator(num_nodes=N_NODES, num_ghz_states_for_sum=TARGET_SUM_BITS, check_round_frequency=CHECK_FREQUENCY)
simulator_tampered.generate_shared_sum(total_rounds=TOTAL_ROUNDS_TO_RUN, enable_eavesdropping_overall=True, eavesdropper_basis='Z', eavesdropped_qubit_idx=0)

print("\n\n*****************************************************")
print("* TAMPERING SCENARIO (Eavesdropper X, with Check Rounds) *")
print("*****************************************************")
# Eavesdropper always tries to measure qubit 0 in X-basis
simulator_tampered_X = SumOfColumnsSimulator(num_nodes=N_NODES, num_ghz_states_for_sum=TARGET_SUM_BITS, check_round_frequency=CHECK_FREQUENCY)
simulator_tampered_X.generate_shared_sum(total_rounds=TOTAL_ROUNDS_TO_RUN, enable_eavesdropping_overall=True, eavesdropper_basis='X', eavesdropped_qubit_idx=0)