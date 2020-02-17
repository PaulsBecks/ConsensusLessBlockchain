from functools import reduce
from .transaction import Transaction
from .account import Account
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

class Ledger:
  
  def __init__(self):
    self.account_transactions = {} 
    self.valid_transactions = {}
    self.open_transactions = {}
    #self.add_transaction(Transaction(None, None, account, 10, []))

  def add_to_account_transactions(self, account, transaction):
    transactions = self.account_transactions.get(account, {})
    transactions[transaction.sig] = transaction
    self.account_transactions[account] = transactions

  # add transaction
  def add_transaction(self, transaction):
    #if not transaction.validate_sig():
    #  print("sig not valid")
    #  return 
    self.open_transactions[transaction.sig] = transaction
    self.add_to_account_transactions(transaction.sender, transaction)
    self.add_to_account_transactions(transaction.receiver, transaction)
    r = self.get_transaction(transaction.reference)
    f = self.get_transaction(transaction.former)
    if r:
      r.add_referenced_by(transaction)
    if f:
      f.add_output(transaction)

  def is_valid_transaction(self, transaction):
    if transaction.sender == self.genesis_account.get_public_key(): #TODO replace this with proper Genisis check
      return True

    if self.get_valid_transaction(transaction):
      return True
    
    if not self.is_valid_transaction(transaction.former):
      return False

    if not transaction.future_fulfilled():
      return False
    
    if not transaction.valid_sig():
      return False

    self.valid_transactions[transaction.sig] = transaction
    del self.open_transactions[transaction.sig]
    return True

  def get_accounts(self):
    return list(self.account_transactions.keys())

  # find not yet validated transaction
  def get_open_transaction(self):
    ts = list(self.open_transactions.keys())
    return self.open_transactions[ts[0]] if len(ts) > 0 else None

  def get_valid_transaction(self, transaction):
    try:
      t = self.open_transactions[sig]
      return t
    except:
      return None

  def get_transaction(self, sig):
    try:
      t = self.open_transactions[sig]
      if not t:
        t = self.valid_transactions[sig]
      return t
    except:
      return None 

  def get_transaction_balance(self, sig):
    t = self.get_transaction(sig)
    return t.get_available_amount()
  
  def get_input(self, amount):
    for transaction in self.account_transactions:
      if transaction.sender == self.account: # only consider received tokens
        continue
      avlb = transaction.get_available_amount()
      if avlb < amount:
        print(transaction)
      else:
        return transaction
    return None

  def get_valid_transactions(self):
    return self.valid_transactions
  
  def get_open_transactions(self):
    return self.open_transactions
  
  def get_account_transactions(self, account_key):
    return self.account_transactions.get(account_key, {})

  def genesis(self, receiver, amount=100):
    self.genesis_account = Account()
    transaction = Transaction(None, self.genesis_account.get_public_key(), receiver, amount, None, None)
    transaction.valid = True
    self.genesis_account.sign(transaction)
    self.valid_transactions[transaction.sig] = transaction
    self.add_to_account_transactions(self.genesis_account.get_public_key(), transaction)
    self.add_to_account_transactions(receiver, transaction)

  def __str__(self):
    return "Open Transactions: %d - Valid Transactions: %d " % (len(list(self.open_transactions.keys())), len(list(self.valid_transactions.keys())))