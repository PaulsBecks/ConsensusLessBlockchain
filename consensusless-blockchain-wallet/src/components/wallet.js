import React, { useState } from "react";
import { postTransaction } from "../services/blockchain";
import {
  calculateBalance,
  updateWalletTransactions,
  createTransaction,
  stringToHex
} from "../services";
import { Button, Form, TextArea } from "semantic-ui-react";

export default function Wallet({
  wallet,
  setTransaction,
  setWallet,
  endpoint
}) {
  const [loadingTransactions, setLoadingTransactions] = useState(false);
  const [amount, setAmount] = useState("");
  const [receiver, setReceiver] = useState("");
  const loadTransactions = async () => {
    setLoadingTransactions(true);
    setWallet(await updateWalletTransactions(endpoint, wallet));
    setLoadingTransactions(false);
  };

  return (
    <div>
      <div className="clbc-wallet-container">
        <div>
          <div className="clbc-balance-wrapper">
            <h3>Balance</h3>
            <p>{calculateBalance(wallet)}</p>
          </div>
          <div className="clbc-public-key-wrapper">
            <h3>Public Key</h3>
            <p>
              {wallet.pem_pub_key.split("\n").map(p => (
                <>
                  {p}
                  <br />
                </>
              ))}
            </p>
          </div>
        </div>
        <div>
          <div className="clbc-create-transaction-wrapper">
            <h3>Send</h3>
            <Form>
              <Form.Field>
                <label>Amount</label>
                <input
                  placeholder="Amount"
                  value={amount}
                  onChange={e => setAmount(e.target.value)}
                />
              </Form.Field>
              <Form.Field>
                <label>Receiver Key</label>
                <TextArea
                  placeholder="Receiver Key"
                  value={receiver}
                  onChange={e => {
                    setReceiver(e.target.value);
                  }}
                />
              </Form.Field>
              <Button
                type="button"
                primary
                onClick={async () => {
                  await postTransaction(
                    endpoint,
                    await createTransaction(amount, receiver, wallet)
                  );
                  loadTransactions();
                  setReceiver("");
                  setAmount("");
                }}
              >
                Submit
              </Button>
            </Form>
          </div>
          <div className="clbc-create-transaction-history-wrapper">
            <h3>History</h3>
            <Button primary onClick={loadTransactions}>
              Reload
            </Button>
            <ul>
              {Object.values(wallet.transactions).map(t => (
                <li onClick={() => setTransaction(t)}>
                  {stringToHex(t.sig.slice(0, 30)) + "..."}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
