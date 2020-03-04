from functools import reduce
from ledger import Ledger
from transaction import Transaction
from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend as crypto_default_backend


# This will become a client / node
class Process:
  transactions = []
  
  def __init__(self, wallet, neighbors=[]):
    self.ledger = Ledger(self)
    self.id = id
    self.neighbors = neighbors

  # create a transaction
  def create_transaction(self, receiver, amount):
    if amount > self.get_balance():
      print("You want to send %d but your balance is %d" % (amount, self.get_balance()))
      return 
    inp = self.ledger.get_input(amount)
    if not inp:
      print("No transaction available you need to split")
      return

    transaction = Transaction(inp, self, receiver, amount, self.ledger.get_open_transaction())
    self.ledger.add_transaction(transaction)
    self.send_transaction(transaction)


  def add_neighbor(self, neighbor):
    self.neighbors.append(neighbor)

  # send transaction to others
  def send_transaction(self, transaction):
    for neighbor in self.neighbors:
      neighbor.add_transaction(transaction)

  def add_transaction(self, transaction):
    self.ledger.add_transaction(transaction)

  # check balance
  def get_balance(self):
    return self.ledger.get_balance()

  def get_id(self):
    return self.id

  def __str__(self):
    return "Process %d has balance %d" % (self.id, self.get_balance())

def main():
  key = rsa.generate_private_key(
    backend=crypto_default_backend(),
    public_exponent=65537,
    key_size=2048
  )
  private_key = key.private_bytes(
      crypto_serialization.Encoding.PEM,
      crypto_serialization.PrivateFormat.PKCS8,
      crypto_serialization.NoEncryption())
  public_key = key.public_key().public_bytes(
      crypto_serialization.Encoding.OpenSSH,
      crypto_serialization.PublicFormat.OpenSSH
  )
  
  process1 = Process(1)
  process2 = Process(2, [process1])
  process1.add_neighbor(process2)
  process1.create_transaction(process2, 10)
  process2.create_transaction(process1, 10)
  process1.create_transaction(process2, 10)
  process2.create_transaction(process1, 10)

  
if __name__ == "__main__":
  main()