import axios from "axios";

export default async function getAccountTransactions(endpoint, account_key) {
  const url = endpoint + "/accounts/transactions";
  const response = await axios.post(url, {
    account_key
  });
  return response.data;
}
