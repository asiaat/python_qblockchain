import datetime as _dt
import hashlib as _hashlib
import json as _json
import random
import sys
import numpy as np
import time

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
        self.MAX_NONCE = 2**32
        
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
        #print("RESULTS: \n"+str(results))        
        
        comp_time   = results.time_taken
        counts      = results.get_counts(circuit)
        print("COUNTS: \n"+str(counts))  
        
        status      = results.status
        success     = results.success
        
        #picking up the maximally probable state
        max_state = max(counts, key=counts.get)
        print ('max_state:', max_state)
        max_state256 = max_state

        for i in range(256 - len(max_state)):
            max_state256+='0'       

        return [status, success, max_state256, comp_time] #4bit vector
    
    
    def qPoW(self,text, QC_switch, nonce):
    
        hashIn = _hashlib.sha3_256(text.encode("ascii")).hexdigest() # hashing the 'text' input
        #string-type output
        
        print ('hashIn-hex:', hashIn, 'length:', len(hashIn))

        # convert hashIn(hex) to hashIn_bin(binary)
        scale = 16 #hex base
        hashIn_bin = bin(int(hashIn, scale))[2:].zfill(len(hashIn)*4)
        print ('hashIn-binary:', str(hashIn_bin), 'length:', len(hashIn_bin))
        
        #switch to enable quantum simulator or quantum computer
        if QC_switch == 0:
            [status, success,qstate_bin, comp_time] = self.sim_quantum_operation(hashIn_bin, nonce)
            #print("Circuit: number of qubits: "+quantum_circuit.num_qubits())
        if QC_switch == 1: 
            pass

        print('qblock-output:', str(qstate_bin), 'length:', len(qstate_bin))

        xor_bin = self.xor(str(hashIn_bin), str(qstate_bin), 256)
        hashOut = _hashlib.sha3_256(xor_bin.encode("ascii")).hexdigest()

        print('XOR:', str(xor_bin), 'length:', len(xor_bin))        
        print('hashOut-hex:', str(hashOut), 'length:', len(hashOut), '\n\n')

        return [hashOut, comp_time]
    
    def verify(self,text, nonce, prefix_zeros):
        prefix_str = '0'*prefix_zeros

        print('verify::nonce:', nonce)
        #text = "Quantamoto"
        #text = str(block_number) + transactions + previous_hash + str(nonce)
        print('verify::text:', text)
        [new_hash, ver_time] = self.qPoW(text, QC_switch=0, nonce=1)
        
        print("verify::new_hash: "+new_hash)

        if new_hash.startswith(prefix_str):
            print(f"verify:: Verified: nonce {nonce}\n") 
            
            return [True, new_hash, ver_time]
        else:
            print(f"verify:: False:{nonce}\n")
            
            return [False, None, ver_time]
        
    def mine_using_simu(self, prefix_zeros):
        
        prefix_str = '0'*prefix_zeros #sets the difficulty, in hex format, bin: multiply by 4
        
        start = time.time()
        comp_time_block = 0
        routine_n_times = 0
        
        for i in range(self.MAX_NONCE):
#             random.seed(i)
            nonce = random.randint(0, self.MAX_NONCE)
            print('created  nonce:', nonce)
            #text = str(block_number) + transactions + previous_hash + str(nonce) #hash input
            text = "nakamo"+str(nonce)
            print ('text:', text, '\n'  )
            [new_hash, comp_time] = self.qPoW(text=text,QC_switch=0,nonce=nonce)

            
            comp_time_block+=comp_time
            routine_n_times = i
            
            if new_hash.startswith(prefix_str):
                print('PROOF founded! : hash:', new_hash)
                break
            
        print("===========================================================================")
        
        total_time = str((time.time() - start))
        print(f"mining ended. mining time: {total_time} seconds")
        print('final hash:', new_hash)
        print('suitable nonce:', nonce)
        print(f"routine {routine_n_times} times")
        
        return [new_hash, nonce, comp_time]
    

    def string_to_bitlist(self,inpt_str):

        hashIn = _hashlib.sha3_256(inpt_str.encode("ascii")).hexdigest() # hashing the 'text' input
        #string-type output
            
        print ('hashIn-hex:', hashIn, 'length:', len(hashIn))
        

        # convert hashIn(hex) to hashIn_bin(binary)
        scale = 16 #hex base
        hashIn_bin = bin(int(hashIn, scale))[2:].zfill(len(hashIn)*4)
        print ('hashIn-binary:', str(hashIn_bin), 'length:', len(hashIn_bin))
    
        #input hashIn string
        fourbit_array = self.break_up_4bit_values(hashIn_bin)
        assert len(fourbit_array) == 64
        
        q_par = [int(fourbit_array[i],2) for i in range(len(fourbit_array)-1)] #throwing away the last string element
        print(q_par)
        
        return [q_par,hashIn,hashIn_bin]
