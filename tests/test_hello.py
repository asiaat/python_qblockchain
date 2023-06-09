import sys, os
#sys.path.append("/Users/kalleolumets/asiaat/python_qblockchain")
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import hashlib

from  qblockchain import QBlockchain

def test_hello():
    assert 1 + 1 == 2
    
def test_valid_chain():
    bc = QBlockchain()
    bc.mine_block("Valid block")
    assert bc.is_chain_valid() == True
    
def test_circuit():
    assert 2 + 1 == 3
    
def test_4_bit():
    bc = QBlockchain()
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

