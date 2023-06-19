from qblockchain import QBlockchain
from qiskit.primitives import Sampler
from qiskit.circuit.random import random_circuit
import random
from qiskit_ibm_runtime import Options, QiskitRuntimeService


class SessionBlockchain(QBlockchain):
    def __init__(self, simulator_name,  session_count):      
        super().__init__(simulator_name)    
        self.sampler = Sampler()
        self.session_count = session_count
        
    def test_random_circuit(self):
        transfBit = self.string_to_bitlist("uhti")
        circ1 = self.quantum_circuit(transfBit,3)
        #circ1.draw("mpl")
        print(str(circ1.num_qubits))
        
        
        job = self.sampler.run(circ1)
        result = job.result()
        print(result)
        
    def run_circuits_session(self,circuits):
        
        circuits = []         
        for i in range(self.session_count):
            #    random.seed(i)
            nonce = random.randint(0, self.MAX_NONCE)
            print('created  nonce:', nonce)
            #text = str(block_number) + transactions + previous_hash + str(nonce) #hash input
            text = "nakamo"+str(nonce)
            circuits.append(bc.quantum_circuit(bc.string_to_bitlist(text),3)) 

        job = self.sampler.run(circuits)
        results = job.result()
        
        print("==================================")
        print(results)
        
        return results


bc = SessionBlockchain("qasm_simulator", session_count=3)
bc.mine_block("any str")
#bc.mine_using_simu(1)
#bc.test_random_circuit()
results = bc.run_circuits_session(None)
print(results.quasi_dists)
#for result in results.quasi_dists:
#    print(result)


