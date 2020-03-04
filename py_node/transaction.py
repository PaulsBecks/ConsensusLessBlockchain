import re
import json
import binascii
from .config import SEPERATOR, ARR_SEPERATOR, GENESIS_AMOUNT
from functools import reduce 
from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature

MINIMUM_STACKED = GENESIS_AMOUNT/2 +1

class Transaction:
  def __init__(self, former, sender, receiver, amount, reference=[], sig=None):
    self.sender = sender
    self.receiver = receiver
    self.amount = amount
    self.sig = sig
    self.former = former
    self.reference = reference
    self.referenced_by = []
    self.outputs = [] # is input of others
    self.valid = False

  def get_valid(self):
    return self.valid

  # checks if future is valid, this is true if enough is stacked and the money wasn't spend twice
  def future_fulfilled(self):
    amount_stacked = self.get_amount_stacked()
    if amount_stacked < MINIMUM_STACKED:
      return False

    if not self.collected_all_references():
      return False

    return True

  # returns the stack in the future
  def get_amount_stacked(self):
    return reduce(lambda x, total: x + total, map(lambda t: t.get_amount_stacked(), self.referenced_by), self.amount)

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
    former = {}
    for f in list(map(lambda x: x.split('-'),values[0].split(ARR_SEPERATOR))):
      former[f[0]] = f[1]

    references = []
    for f in list(map(lambda x: x.split('-'),values[4].split(ARR_SEPERATOR))):
      references.append(f[0])
    
    return Transaction(former, values[1], values[2], int(values[3]), references, values[5])

  def serialize_former(self):
    former = list(self.former.keys())
    return reduce(lambda former_string, f: f if former_string == "" else former_string + ARR_SEPERATOR +f,map(lambda f: f + "-"+ self.former[f],former), "")

  def serialize_references(self):
    return reduce(lambda reference_string, r: r if reference_string == "" else reference_string + ARR_SEPERATOR + r, self.reference, "")

  def serialize(self, with_sig=True):
    former = self.serialize_former()
    references = self.serialize_references()
    transaction_string = "frm:%s%ssnd:%s%srcv:%s%samt:%d%sref:%s%s" % (former, SEPERATOR, self.sender, SEPERATOR, self.receiver, SEPERATOR, self.amount, SEPERATOR, references, SEPERATOR)
    if self.sig and with_sig:
       transaction_string += "sig:%s" % self.sig
    return transaction_string

  def set_sig(self, sig):
    self.sig = sig

  def set_valid(self):
    self.valid = True
  
  def validate_sig(self):
    try:
        key = crypto_serialization.load_pem_public_key(self.sender.encode(), crypto_default_backend())
        key.verify(
            signature=bytes.fromhex(self.sig),
            data=self.serialize(with_sig=False).encode("utf-16-le"),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    return False

  def toJSON(self):
    frm = self.former
    ref = self.reference
    d = {'amt':self.amount, 'frm': self.former, 'ref': self.reference, 'snd': str(self.sender), 'rcv': str(self.receiver), 'sig': self.sig, 'val':self.valid}
    return d