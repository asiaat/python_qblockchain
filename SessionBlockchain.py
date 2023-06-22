from qblockchain import QBlockchain
from qiskit.primitives import Sampler
from qiskit.circuit.random import random_circuit
import random
from qiskit_ibm_runtime import Options, QiskitRuntimeService
import datetime as _dt
import hashlib as _hashlib

STATE_BIN = ['']

class SessionBlockchain(QBlockchain):
    def __init__(self, simulator_name,  session_count):      
        super().__init__(simulator_name)    
        self.sampler = Sampler()
        self.session_count = session_count
        self.circuits = []
        self.data_circuits = []
        
    def test_random_circuit(self):
        transfBit = self.string_to_bitlist("uhti")
        circ1 = self.quantum_circuit(transfBit,3)
        #circ1.draw("mpl")
        print(str(circ1.num_qubits))
        
        
        job = self.sampler.run(circ1)
        result = job.result()
        print(result)
        
    def run_circuits_session(self,circuits):
        
        #circuits = []         
        for i in range(self.session_count):
            #    random.seed(i)
            nonce = random.randint(0, self.MAX_NONCE)
            print('----------------------\ncreated  nonce:', nonce)
            
            #text = str(block_number) + transactions + previous_hash + str(nonce) #hash input
            text = "nakamo"+str(nonce)
            bitlist = bc.string_to_bitlist(text)
            quantum_cirquit = bc.quantum_circuit(bitlist[0],3)
            self.circuits.append(quantum_cirquit) 
            self.data_circuits.append(bitlist)
            

        job = self.sampler.run(self.circuits)
        results = job.result()
        
        print("==================================")
        print(results)
        
        return results
    
    def maxstate_to_hexhashout(self,hashIn_bin,results):
        #picking up the maximally probable state
        max_state = format(max(results, key=results.get),'03b')
        print ('max_state:', max_state)
        max_state256 = max_state

        for i in range(256 - len(max_state)):
            max_state256+='0' 
            
        
        xor_bin = self.xor(str(hashIn_bin), str(max_state256), 256)
        hashOut = _hashlib.sha3_256(xor_bin.encode("ascii")).hexdigest()

        print('XOR:', str(xor_bin), 'length:', len(xor_bin))        
        print('hashOut-hex:', str(hashOut), 'length:', len(hashOut), '\n\n')
            
        
            
        return [max_state256,hashOut]


bc = SessionBlockchain("qasm_simulator", session_count=40000)
bc.mine_block("any str")
results = bc.run_circuits_session(None)
print(results.quasi_dists)
indx = 0
prefix_str = '0'*3 

for result in results.quasi_dists:

    [xorRes,hexRes] = bc.maxstate_to_hexhashout(bc.data_circuits[indx][2],result)
    print(hexRes)
    
    indx += 1 
    
    if hexRes.startswith(prefix_str):
        print('\n ====================================\nPROOF founded! : hash:', hexRes)
        break
    


