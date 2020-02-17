import json
from flask import Flask, request
from py_node.ledger import Ledger
from py_node.transaction import Transaction
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

ledger = Ledger()

def dumper(obj):
  if hasattr(obj, 'toJSON'):
    print(obj)
    return obj.toJSON()

@app.route('/')
def hello_world():
    return 'Hello there!'

@app.route('/genesis', methods=["POST"])
def genesis():
  receiver = json.loads(request.data).get('receiver', None)
  if not receiver:
    return "400 no receiver!"
  ledger.genesis(receiver)
  return 'Genesis activated'

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
  if request.method == "POST":
    transaction = json.loads(request.data).get("transaction", None)
    if not transaction:
      return 
    print(transaction)
    return json.dumps(ledger.add_transaction(Transaction.decerialize(transaction)), default=dumper)

@app.route('/transactions/open')
def transactions_open():
  if request.method == "GET":
    transactions = ledger.get_open_transactions()
    return json.dumps(transactions, default=dumper, ensure_ascii=False).encode('utf-8')


@app.route('/transactions/valid')
def transactions_valid():
  if request.method == "GET":
    transactions = ledger.get_valid_transactions()
    return json.dumps(transactions, default=dumper)

@app.route('/accounts/transactions', methods=["POST"])
def accounts_transactions():
  account_key = json.loads(request.data).get('account_key', None)
  print(account_key)
  if not account_key:
    return json.dumps([])
  transactions = ledger.get_account_transactions(account_key)
  print(transactions)
  return json.dumps(transactions, default=dumper, indent=3, ensure_ascii=False)

@app.route('/accounts')
def accounts():
  return json.dumps(ledger.get_accounts(), default=dumper, ensure_ascii=False);
