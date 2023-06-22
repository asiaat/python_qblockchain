from qiskit_ibm_provider import IBMProvider
provider = IBMProvider()

# display current supported backends
print(provider.backends())

#simulator_backend = provider.get_backend('ibmq_qasm_simulator')
#print(simulator_backend.name)
