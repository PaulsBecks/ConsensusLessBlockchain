import sign from "./sign";
import { ab2str } from "../strAb";
import postTransaction from "../blockchain/postTransaction";
import { SEPERATOR } from "../../config";
import findFormer from "./findFormer";

function buildTransactionString({ sender, receiver, amount, former, refered }) {
  return (
    "frm:" +
    former +
    SEPERATOR +
    "snd:" +
    sender +
    SEPERATOR +
    "rcv:" +
    receiver +
    SEPERATOR +
    "amt:" +
    amount +
    SEPERATOR +
    "ref:" +
    refered +
    SEPERATOR
  );
}

function addSig(transactionString, sig) {
  return transactionString + "sig:" + ab2str(sig);
}

export default async function(amount, receiver, wallet) {
  const former = findFormer(wallet, amount);
  if (!former) {
    console.log("Not enough balance apparently!");
    return null;
  }

  let transactionString = buildTransactionString({
    amount,
    receiver,
    sender: wallet.pem_pub_key
  });
  const sig = await sign(transactionString, wallet);
  transactionString = addSig(transactionString, sig);
  console.log("Create Transaction", amount, receiver, transactionString);
  return transactionString;
}
