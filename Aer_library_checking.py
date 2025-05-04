# checking for Aer library
# Import the Aer provider from qiskit_aer
from qiskit_aer import Aer

# Try to get the statevector_simulator backend
try:
    simulator_backend = Aer.get_backend('statevector_simulator')
    print("Successfully found the statevector_simulator backend!")
except Exception as e:
    print(f"Error finding backend: {e}")

# You can also list all available Aer backends
print("\nAvailable Aer backends:")
print(Aer.backends())