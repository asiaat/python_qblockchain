from  qblockchain import QBlockchain
import hashlib

def main():
    qbc = QBlockchain()
    qbc.mine_block("First block 1")
    print(qbc.is_chain_valid())
    
    #qbc.break_up_4bit_values([0000])
    #qbc.xor(["23ab0","12ab0"],4)
    xor_bin = qbc.xor(str("1234"), str("abc0"), 4)
    hashOut = hashlib.sha3_256(xor_bin.encode("ascii")).hexdigest()
    print(hashOut)
    
    text = "0000000"
    hashIn = hashlib.sha3_256(text.encode("ascii")).hexdigest() # hashing the 'text' input
    #string-type output
        
    print ('hashIn-hex:', hashIn, 'length:', len(hashIn))
    

    # convert hashIn(hex) to hashIn_bin(binary)
    scale = 16 #hex base
    hashIn_bin = bin(int(hashIn, scale))[2:].zfill(len(hashIn)*4)
    print ('hashIn-binary:', str(hashIn_bin), 'length:', len(hashIn_bin))
 
    #input hashIn string
    fourbit_array = qbc.break_up_4bit_values(hashIn_bin)
    print(len(fourbit_array))
    q_par = [int(fourbit_array[i],2) for i in range(len(fourbit_array)-1)] #throwing away the last string element
    #circuit = qbc.quantum_circuit(q_par, 1)
    
def mine():
    bc = QBlockchain("qasm_simulator")
    bc.mine_block("any str")
    bc.mine_using_simu(4)
    
def starts_with(new_hash, starts):
    res = new_hash.startswith(starts)
    print(res)
    return res
                
    
    

if __name__ == "__main__":
    #main()
    mine()
    starts_with("Hello wello","Hello")
    starts_with("b502d86bf9ed32cfcc64414bb0d129718ba0961144083c2f26358edbd312040d","00")