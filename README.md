# ConsensusLessBlockchain

Implementation of a blockchain that works without consensus. 

First a group of scientiests (Rachid Guerraoui, Petr Kuznetsov, Matteo Monti, Matej Pavlovič, Dragos-Adrian Seredinschi) figured out we don't need consensus for solving the double spending problem. https://arxiv.org/pdf/1906.05574.pdf

And then more in detail Jakub Sliwinski and Roger Wattenhofer proofed an algorithm that implements this. https://arxiv.org/pdf/1909.10926.pdf

In this project I will try to implement as a proof of concept the consensus less blockchain, write a node and a wallet that can be used to interact with the chain as well as a block inspector.

In the following I try to explain in simple words what happens here. And why this is good idea.

# What is this

This is a distributed ledger. It records transactions of coins between different parties. The important thing is to make sure no one is creating any coins out of thin air. This is called double spending. If I have 50 coins and could send you 50 and my grandma 50 I could create coins that are not available. 

Traditionaly, like with Bitcoin, the participating nodes need to coordinate which transactions to write in the ledger to handle this doublespending problem. To do this a consensus algorithm is used. But as Guerraoui et al. showed this is not needed. 

Instead of communicating the whole time with everyone we say a transaction is valid when more then 50% of the total money available references this transaction and it's not a double spend. This is maybe a bit hard to grasp so I drew a little sketch.



# Wallet

The wallet I build.

\[!important\] It is not secure, it saves your private key in the browser without any security.

# Start the node

Start the python node

```
python install -r requirements.txt
export FLASK_APP=node.py
flask run
```

Start the browser wallet

```
cd consensusless-blockchain-wallet
yarn install
yarn start
```
