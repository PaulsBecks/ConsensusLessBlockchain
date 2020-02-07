from process import Process

# This is an implementation of the algorithm proposed by the paper "The Consensus Number of a Cryptocurrency" by Guerraoui et al.

processes = []

def main():
  print("Amount of processes:\n")
  amount = int(input())
  for i in range(amount):
    process = Process(i, 2000, processes)
    processes.append(process)
  
  print(processes)

  while(1):
    print("Who sends? [0-%d]" % amount)
    sender = processes[int(input())]
    print("To whom? [0-%d]" % amount)
    receiver = processes[int(input())]
    print("How much? [0 - %d]" % sender.get_balance())
    m = int(input())
    sender.transfer(receiver, m)

  return 0

if __name__ == "__main__":
  main()