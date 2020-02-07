from functools import reduce
#process


START_BALANCE = 10

class Process:
  def __init__(self, id, port, neighbors):
    self.my_history=[]
    self.pending_transactions=[]
    self.validated_transactions=[]
    self.balance=START_BALANCE
    self.id = id
    self.port = port
    self.neighbors = neighbors
    return 

  def send_message(self, transaction, neighbor):
    #tcp send to port
    neighbor.add_transaction(transaction)

  def transfer(self, receiver, amount):
    transaction = (self, receiver, amount, self.my_history.copy())
    #append transaction to history
    #broadcast transaction
    for neighbor in self.neighbors:
      self.send_message(transaction, neighbor)
    self.my_history.append(transaction)
    self.balance -= amount
    print(self)
    return

  def is_valid(self, transaction):
    # is already valid
    if(transaction in self.validated_transactions):
      return True
    
    # has only valid dependencies
    for t in transaction[3]:
      if not self.is_valid(t):
        return False
    
    # and after the transaction the balance would be positive
    b = reduce(
      lambda t, total: t+total, 
      map(
        lambda t: -transaction[2] if t[0] == transaction[0] else transaction[2],
        filter(
          lambda t: t[0] == transaction[0] or t[1] == transaction[0], 
          transaction[3]
        )
      ),
      START_BALANCE
    )

    if b >= 0:
      self.validated_transactions.append(transaction)
      return True

    return False

  def get_balance(self):
    #read balance from history
    return self.balance

  def add_neighbor(self, neighbor):
    self.neighbors.append(neighbor)

  def add_transaction(self, transaction):
    if(transaction[1] == self):
      valid = self.is_valid(transaction)
      if valid:
        self.my_history.append(transaction)
        self.balance += transaction[2]
        print(self)
      else:
        print("this transaction was malisios!")
    else:
      self.pending_transactions.append(transaction)

  def __str__(self):
    return "Process %d has balance %d and runs on port %d" %  (self.id, self.balance, self.port)
  