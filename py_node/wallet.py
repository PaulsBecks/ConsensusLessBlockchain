import hashlib
from functools import reduce

from .config import SEPERATOR
from .transaction import Transaction
from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.exceptions import InvalidSignature
from .ledger import Ledger
from .account import Account

class Wallet:
  def __init__(self):
    self.account = Account()
    self.my_transactions = []
    self.ledger = Ledger()
    self.nodes = []

  def get_balance(self):
    return reduce(
      lambda x, total: x+total,
      map(lambda t: -t.amount if t.sender == self.get_public_key() else t.amount, 
      filter(lambda t: t.sender == self.get_public_key() or self.ledger.is_valid_transaction(t), self.my_transactions)), 
    0)
  
  
  def sign(self, transaction):
    self.account.sign(transaction)

  def create_transaction(self, receiver, amount):
    former = self.get_former(amount)
    if not former:
      print("No fitting transaction found, abort.")
      return None

    reference = self.ledger.get_open_transaction()
    if not reference:
      reference = former

    transaction = Transaction(former.sig, self.get_public_key(), receiver, amount, reference.sig, None)
    self.sign(transaction)
    self.add_transaction(transaction)
    return transaction

  def get_former(self, amount):
    for transaction in self.my_transactions:
      if transaction.receiver == self.get_public_key() and transaction.get_available_amount() >= amount:
        return transaction
    return None

  def get_public_key(self):
    return self.account.get_public_key()
    
  def add_node(self, node):
    self.nodes.append(node)

  def add_transaction(self, transaction):
    self.ledger.add_transaction(transaction)
    if self.is_my_transaction(transaction):
      self.my_transactions.append(transaction)

  def is_my_transaction(self, transaction):
    pk = self.get_public_key()
    return transaction.sender == pk or transaction.receiver == pk

  def send_transaction(self, transaction):
    for node in self.nodes:
      node.add_transaction(node)

  def get_ledger(self):
    return self.ledger
  
  def get_my_transactions(self):
    return self.my_transactions

  def toJSON(self):
    return self.account.toJSON()
