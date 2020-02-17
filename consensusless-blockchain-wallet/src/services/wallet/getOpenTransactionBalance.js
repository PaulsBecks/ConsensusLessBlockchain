export default function getOpenTransactionBalance(transactions, transaction) {
  console.log(transaction);
  return (
    transaction.amt -
    transactions
      .filter(t => {
        console.log(!!t.frm[transaction.sig]);
        return !!t.frm[transaction.sig];
      })
      .map(t => t.amount)
      .reduce((total, x) => x + total, 0)
  );
}
