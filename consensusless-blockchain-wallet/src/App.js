import React, { useState } from "react";
import useLocalStorage from "./hooks/useLocalStorage";
import { createWallet } from "./services";
import "./App.css";
import { Button, Input } from "semantic-ui-react";
import { Transaction, Wallet } from "./components";

function App() {
  const [wallet, setWallet] = useLocalStorage("wallet");
  const [transaction, setTransaction] = useState();
  const [endpoint, setEndpoint] = useState("http://localhost:5000");

  return (
    <div className="clbc-container">
      <h1>Consensusless Blockchain</h1>
      {wallet ? (
        transaction ? (
          <Transaction
            transaction={transaction}
            setTransaction={setTransaction}
          />
        ) : (
          <Wallet
            wallet={wallet}
            setTransaction={setTransaction}
            endpoint={endpoint}
            setWallet={setWallet}
          />
        )
      ) : (
        <div className="clbc-no-wallet-container">
          <h2>>No wallet found</h2>
          <p>To interact with the blockchain you need to create a wallet.</p>
          <Button primary onClick={async () => setWallet(await createWallet())}>
            Create New Wallet
          </Button>
        </div>
      )}
      <div>
        <h2>Use Node</h2>
        <Input value={endpoint} onChange={e => setEndpoint(e.target.value)} />
      </div>
    </div>
  );
}

export default App;
