import sys, os
#sys.path.append("/Users/kalleolumets/asiaat/python_qblockchain")
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from  qblockchain import QBlockchain

def test_hello():
    assert 1 + 1 == 2
    
def test_valid_chain():
    bc = QBlockchain()
    bc.mine_block("Valid block")
    assert bc.is_chain_valid() == True

