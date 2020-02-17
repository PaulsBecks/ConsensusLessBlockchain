import { getAccountTransactions } from "../blockchain";

export default async function updateWalletTransactions(endpoint, wallet) {
  const transactions = await getAccountTransactions(
    endpoint,
    wallet.pem_pub_key
  );
  if (transactions) {
    wallet["transactions"] = transactions;
  }
  return wallet;
}
