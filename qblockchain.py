import datetime as _dt
import hashlib as _hashlib
import json as _json
import random
import sys
import numpy as np

if sys.version_info < (3, 6):
	import sha3

# import modules for Qiskit
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, Aer, IBMQ, execute, schedule
from qiskit.compiler import transpile
from qiskit.tools.visualization import plot_histogram
from qiskit.transpiler import PassManager
from qiskit.tools.monitor import job_monitor
from qiskit.providers.aer import AerSimulator
from qiskit_ibm_provider import IBMProvider

class QBlockchain:
    def __init__(self, simulator_name):
        self.chain = list()
        initial_block = self._create_block(
            data="genesis block", proof=1, previous_hash="0", index=1
        )
        self.chain.append(initial_block)
        self.provider = IBMProvider()
        
        self.simu_name = simulator_name
        self.simulator_backend   = BasicAer.get_backend(self.simu_name)
        
    def get_simulator_backend(self):
        #backend = None
        #if self.simulator_backend == None:
        #    backend =  BasicAer.get_backend(self.simu_name)
        
        return self.simulator_backend 

    def mine_block(self, data: str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(
            previous_proof=previous_proof, index=index, data=data
        )
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )
        self.chain.append(block)
        return block

    def _create_block(
        self, data: str, proof: int, previous_hash: str, index: int
    ) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }

        return block

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def _to_digest(
        self, new_proof: int, previous_proof: int, index: int, data: str
    ) -> bytes:
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data
        # It returns an utf-8 encoded version of the string
        return to_digest.encode()

    def _proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            to_digest = self._to_digest(new_proof, previous_proof, index, data)
            hash_operation = _hashlib.sha256(to_digest).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def _hash(self, block: dict) -> str:
        """
        Hash a block and return the crytographic hash of the block
        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()

        return _hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            # Check if the previous hash of the current block is the same as the hash of it's previous block
            if block["previous_hash"] != self._hash(previous_block):
                return False

            previous_proof = previous_block["proof"]
            index, data, proof = block["index"], block["data"], block["proof"]
            hash_operation = _hashlib.sha256(
                self._to_digest(
                    new_proof=proof,
                    previous_proof=previous_proof,
                    index=index,
                    data=data,
                )
            ).hexdigest()

            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True
    
    #setting the quantum circuit:
    def quantum_circuit(self,q_par, n_qreg=3):
            qreg_q = QuantumRegister(n_qreg, 'q')
            creg_c = ClassicalRegister(n_qreg, 'c')
            circuit = QuantumCircuit(qreg_q, creg_c)

            #repetitive circuit
            #for i in range(circ_layer):
                
            #n-qubit circuit  
            k = 0 #counter for the parameter values
            for i in range(n_qreg):   
                circuit.rx(q_par[k+i] * np.pi/8, qreg_q[i])
            k+=n_qreg
            
            for i in range(n_qreg):    
                circuit.rz(q_par[k+i] * np.pi/8, qreg_q[i])
            k+=n_qreg
            
            for i in range(n_qreg):
                for j in range(n_qreg):
                    if j != i:
                        circuit.crx(q_par[k+j]*np.pi/8, qreg_q[n_qreg-1-i], qreg_q[n_qreg-1-j])
                    else:
                        k-=1
                k+=n_qreg-1
            
            for i in range(n_qreg):   
                circuit.rx(q_par[k+i]*np.pi/8, qreg_q[i])
            k+=n_qreg
            
            for i in range(n_qreg):    
                circuit.rz(q_par[k+i]*np.pi/8, qreg_q[i])

            #measurements of all qubits
            for i in range(len(qreg_q)):
                circuit.measure(qreg_q[i], creg_c[i])
            
            return circuit
        
    # converting hashIn_bin to a bit string to pass thru a quantum processor
    def break_up_4bit_values(self,hashIn_bin):

        array_4_bit_values = []
        i = 0

        while i < 64 : 
            four_bits = hashIn_bin[2+4*i:2+4*i+4]
            array_4_bit_values.append(four_bits)
            i = i + 1
            
        print("hashIn binary split into 4bit bins:", array_4_bit_values)
        return array_4_bit_values
    
    def xor(self,a, b, n): #a,b - strings, n - length of the XOR output
        ans = ""

        # Loop to iterate over the
        # Binary Strings
        for i in range(n):

            # If the Character matches
            if (a[i] == b[i]):
                ans += "0"
            else:
                ans += "1"
        return ans
    
    def sim_quantum_operation(self, hashIn, nonce):
        
        #input hashIn string
        fourbit_array = self.break_up_4bit_values(hashIn)
        q_par = [int(fourbit_array[i],2) for i in range(len(fourbit_array)-1)] #throwing away the last string element
        circuit = self.quantum_circuit(q_par)
        #print("n_qreg: "+str(n_qreg))

        backend = self.simulator_backend

        job = execute(circuit, backend, shots=20000)

        # Monitor job progress and wait until complete:
        job_monitor(job)

        # Get the job results (this method also waits for the Job to complete):
        results = job.result()
        print(results)        
        
        comp_time = results.time_taken
        counts = results.get_counts(circuit)
        status = results.status
        success = results.success
        
        #picking up the maximally probable state
        max_state = max(counts, key=counts.get)
        print ('max_state:', max_state)
        max_state256 = max_state

        for i in range(256 - len(max_state)):
            max_state256+='0'       

        return [status, success, max_state256, comp_time] #4bit vector
    
    
