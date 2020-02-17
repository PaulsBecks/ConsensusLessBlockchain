export default function isReceivingTransaction(wallet, transaction) {
  return wallet.pem_pub_key === transaction.rcv;
}
