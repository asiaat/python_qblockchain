from  qblockchain import QBlockchain

def main():
    qbc = QBlockchain()
    qbc.mine_block("First block 1")
    print(qbc.is_chain_valid())
    

if __name__ == "__main__":
    main()