import sys, os
#sys.path.append("/Users/kalleolumets/asiaat/python_qblockchain")
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import hashlib
import datetime as _dt

from  qblockchain import QBlockchain
from qiskit_ibm_provider import IBMProvider

bc = QBlockchain("qasm_simulator")
    
def test_valid_chain():
    #bc = QBlockchain("ibmq_qasm_simulator")
    bc.mine_block("Valid block")
    assert bc.is_chain_valid() == True
    

def test_backend():
    #bc = QBlockchain("ibmq_qasm_simulator")
    assert bc.get_simulator_backend().name() == bc.simu_name
    

    
def circuit():
    #bc = QBlockchain("ibmq_qasm_simulator")
    bc.mine_block("Valid block")
    text = "0000000"
    
    hashIn = hashlib.sha3_256(text.encode("ascii")).hexdigest() # hashing the 'text' input
    #string-type output
        
    print ('hashIn-hex:', hashIn, 'length:', len(hashIn))
    

    # convert hashIn(hex) to hashIn_bin(binary)
    scale = 16 #hex base
    hashIn_bin = bin(int(hashIn, scale))[2:].zfill(len(hashIn)*4)
    print ('hashIn-binary:', str(hashIn_bin), 'length:', len(hashIn_bin))
 
    #input hashIn string
    fourbit_array = bc.break_up_4bit_values(hashIn_bin)
    assert len(fourbit_array) == 64
    
    q_par = [int(fourbit_array[i],2) for i in range(len(fourbit_array)-1)] #throwing away the last string element
    print(q_par)
    
    assert type(q_par) == list
    circuit = bc.quantum_circuit(q_par=q_par)
    
    assert circuit.num_qubits == 3
    
def quantum_simulation():
    hashIn = hashlib.sha3_256("00000".encode("ascii")).hexdigest() # hashing the 'text' input

    print ('hashIn-hex:', hashIn, 'length:', len(hashIn))

    # convert hashIn(hex) to hashIn_bin(binary)
    scale = 16 #hex base
    hashIn_bin = bin(int(hashIn, scale))[2:].zfill(len(hashIn)*4)
    print ('hashIn-binary:', str(hashIn_bin), 'length:', len(hashIn_bin))
    
    assert len(hashIn_bin) > 0
    [status, success, max_state256, comp_time] = bc.sim_quantum_operation(hashIn_bin,1)
    
    assert status == "COMPLETED"
    assert success == True
    
def qpow():
    text = "1234"
    res = bc.qPoW(text=text,QC_switch=0,nonce=1)
    assert res != None
    
def test_run_simulation():
    
    hashIn = hashlib.sha3_256("shatoshi nakamoto".encode("ascii")).hexdigest() # hashing the 'text' input

    print ('hashIn-hex:', hashIn, 'length:', len(hashIn))

    # convert hashIn(hex) to hashIn_bin(binary)
    scale = 16 #hex base
    hashIn_bin = bin(int(hashIn, scale))[2:].zfill(len(hashIn)*4)
    print ('hashIn-binary:', str(hashIn_bin), 'length:', len(hashIn_bin))
    
    assert len(hashIn_bin) > 0
    [status, success, max_state256, comp_time] = bc.sim_quantum_operation(hashIn_bin,1)
    
    assert status == "COMPLETED"
    assert success == True
    
def verify():
    text = "1234"
    [check, hash, ver_time] = bc.verify(text=text,nonce=2,prefix_zeros=3)
    print("hash: "+str(hash))
    assert check == False
    
def mine_using_simu():
    [new_hash, nonce, comp_time] = bc.mine_using_simu(2)
    assert 1 == 1
    
def test_text_to_bitlist():
    bitit_list = bc.string_to_bitlist("0000")
    assert bitit_list == [9, 10, 11, 13, 12, 2, 13, 14, 11, 12, 15, 13, 0, 8, 13, 4, 11, 5, 14, 0, 15, 10, 2, 12, 1, 13, 4, 5, 7, 9, 0, 12, 15, 0, 15, 5, 1, 5, 9, 10, 7, 5, 3, 11, 15, 11, 9, 9, 12, 1, 4, 5, 9, 12, 9, 12, 6, 4, 14, 12, 10, 4, 6]

    bc.quantum_circuit(bitit_list,3)
    
    
    
    


