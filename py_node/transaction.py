import re
import json
from .config import SEPERATOR
from functools import reduce 
from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature

MINIMUM_STACKED = 5

class Transaction:
  def __init__(self, former, sender, receiver, amount, reference, sig):
    self.former = former
    self.sender = sender
    self.receiver = receiver
    self.amount = amount
    self.reference = reference
    self.sig = sig
    self.referenced_by = []
    self.outputs = [] # is input of others
    self.valid = False
    #if inp:
      #print("Add inp")
    #  inp.add_output(self)
    #if reference:
    #  reference.add_referenced_by(reference)

  def get_valid(self):
    self.validate()
    return self.valid

  # checks if future is valid, this is true if enough is stacked and the money wasn't spend twice
  def future_fullfilled(self):
    amount_stacked = self.get_amount_stacked()
    if amount_stacked < MINIMUM_STACKED:
      #print("Not stacked enough %d < %d" % (amount_stacked,MINIMUM_STACKED))
      return False

    if not self.collected_all_references():
      #print("Collect missing references")
      return False

    if self.inp.double_spending():
      #print("Double spending")
      return False

    return True

  # returns the stack in the future
  def get_amount_stacked(self):
    #print(self.referenced_by)
    return reduce(lambda x, total: x + total, map(lambda t: t.amount, self.referenced_by), 0)

  # checks if all references are locally available
  def collected_all_references(self):
    #print("Not implemented yet")
    return True
  
  def double_spending(self):
    #TODO check that output sender is current receiver
    available_amount = self.get_available_amount()
    return  available_amount < 0 

  def add_output(self, output):
    self.outputs.append(output)

  def add_referenced_by(self, reference):
    self.referenced_by.append(reference)

  def get_available_amount(self):
    return self.amount - reduce(lambda x, total: total + x, map(lambda t: t.amount, self.outputs), 0)

  def __str__(self):
    #s = self.sender.get_id() if self.sender else 0
    #r = self.receiver.get_id()
    #v = "valid" if self.get_valid() else "invalid"
    return self.serialize()

  @staticmethod
  def decerialize(transaction_string):
    values = list(map(lambda x: x.split(':')[1],transaction_string.split(SEPERATOR)))
    return Transaction(values[0], values[1], values[2], int(values[3]), values[4], values[5])

  def serialize(self, with_sig=True):
    transaction_string = "frm:%s%ssnd:%s%srcv:%s%samt:%d%sref:%s%s" % (self.former, SEPERATOR, self.sender, SEPERATOR, self.receiver, SEPERATOR, self.amount, SEPERATOR, self.reference, SEPERATOR)
    if self.sig and with_sig:
       transaction_string += "sig:%s" % self.sig
    return transaction_string

  def set_sig(self, sig):
    self.sig = sig
  
  def validate_sig(self):
    is_signature_correct = False
    print(self.sender.encode(), self.sig.encode())
    with open('sig', "w") as s:
      s.write(self.sig)
    try:
        print(self.serialize(with_sig=False).encode())
        key = crypto_serialization.load_pem_public_key(self.sender.encode(), crypto_default_backend())
        key.verify(
            signature=self.sig.encode(),
            data=self.serialize(with_sig=False).encode(),
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=64
            ),
            algorithm=hashes.SHA256()
        )
        is_signature_correct = True
    except InvalidSignature:
        is_signature_correct = False
    return is_signature_correct

  def toJSON(self):
    frm = self.former
    ref = self.reference
    d = {'amt':self.amount, 'frm': {}, 'ref': {}, 'snd': str(self.sender), 'rcv': str(self.receiver), 'sig': self.sig, 'val':self.valid}
    print(d)
    return d