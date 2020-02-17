import getOpenTransactionBalance from "./getOpenTransactionBalance";

export default function findFormer(wallet, amount) {
  const transactions = Object.values(wallet.transactions);
  console.log(transactions);
  let rest = amount;
  let former = {};
  for (let i in transactions) {
    let t = transactions[i];
    console.log(t);
    const openTransactionBalance = getOpenTransactionBalance(transactions, t);
    console.log(openTransactionBalance);
    if (openTransactionBalance > 0) {
      let val = Math.min(rest, openTransactionBalance);
      former[t.sig] = val;
      rest -= val;
    }
    if (rest <= 0) {
      return former;
    }
    console.log(former, rest);
  }
  return null;
}
